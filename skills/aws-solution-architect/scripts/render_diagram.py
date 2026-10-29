#!/usr/bin/env python3
"""Render one architecture spec (JSON) into Mermaid, draw.io, PlantUML or Python `diagrams`.

Why one spec: the design is described once (services, groups, flows) and every format
is generated from it, so the diagrams never drift apart and icon names come from a
catalog verified against upstream sources (see verify_catalog.py).

Usage:
  render_diagram.py spec.json --format mermaid|drawio|plantuml|python|all [-o OUTDIR]
  render_diagram.py spec.json --validate-only

Spec (JSON):
  {
    "title": "Three-tier web app",
    "direction": "LR",                        # LR | TB
    "groups": [{"id": "vpc", "label": "VPC 10.0.0.0/16", "type": "vpc", "parent": "region"}],
    "nodes":  [{"id": "web", "service": "alb", "label": "Public ALB", "group": "pub"}],
    "edges":  [{"from": "user", "to": "web", "label": "HTTPS", "style": "dashed", "bidirectional": false}]
  }
Group types: cloud, region, account, vpc, az, public-subnet, private-subnet, onprem, generic.
Services: keys of service_catalog.json (use "generic" for anything without an icon).
Standard library only. Pure text output, no network.
"""
import argparse
import difflib
import json
import math
import os
import re
import sys
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
CATALOG = json.load(open(os.path.join(HERE, "service_catalog.json"), encoding="utf-8"))
SERVICES = CATALOG["services"]
COLORS = CATALOG["category_colors"]
GROUP_TYPES = ["cloud", "region", "account", "vpc", "az", "public-subnet", "private-subnet", "onprem", "generic"]
PUML_VERSION = "v23.1"  # aws-icons-for-plantuml tag the catalog was verified against


# --------------------------------------------------------------------------- spec
class SpecError(Exception):
    pass


def load_spec(path):
    try:
        spec = json.load(open(path, encoding="utf-8"))
    except (OSError, ValueError) as e:
        raise SpecError(f"cannot read spec: {e}")
    return validate(spec)


def validate(spec):
    errs = []
    spec.setdefault("title", "AWS architecture")
    spec.setdefault("direction", "LR")
    spec.setdefault("groups", [])
    spec.setdefault("nodes", [])
    spec.setdefault("edges", [])
    if spec["direction"] not in ("LR", "TB"):
        errs.append("direction must be LR or TB")
    ids = {}
    for kind in ("groups", "nodes"):
        for it in spec[kind]:
            i = it.get("id")
            if not i or not re.fullmatch(r"[A-Za-z0-9_-]+", i):
                errs.append(f"{kind[:-1]} id {i!r} must match [A-Za-z0-9_-]+")
            elif i in ids:
                errs.append(f"duplicate id {i!r}")
            ids[i] = kind
    gids = {g["id"] for g in spec["groups"] if "id" in g}
    for g in spec["groups"]:
        g.setdefault("type", "generic")
        g.setdefault("label", g.get("id", ""))
        if g["type"] not in GROUP_TYPES:
            errs.append(f"group {g.get('id')!r}: type {g['type']!r} not in {GROUP_TYPES}")
        if g.get("parent") and g["parent"] not in gids:
            errs.append(f"group {g['id']!r}: unknown parent {g['parent']!r}")
    for g in spec["groups"]:  # parent cycles
        seen, cur = set(), g.get("id")
        while cur:
            if cur in seen:
                errs.append(f"group parent cycle at {cur!r}")
                break
            seen.add(cur)
            cur = next((x.get("parent") for x in spec["groups"] if x.get("id") == cur), None)
    nids = set()
    for n in spec["nodes"]:
        nids.add(n.get("id"))
        s = n.get("service")
        if s not in SERVICES:
            hint = difflib.get_close_matches(str(s), SERVICES.keys(), n=3)
            errs.append(f"node {n.get('id')!r}: unknown service {s!r}" + (f" (did you mean {hint}?)" if hint else ""))
        if n.get("group") and n["group"] not in gids:
            errs.append(f"node {n.get('id')!r}: unknown group {n['group']!r}")
    for e in spec["edges"]:
        for end in ("from", "to"):
            if e.get(end) not in nids:
                errs.append(f"edge {e}: {end} {e.get(end)!r} is not a node id")
    if errs:
        raise SpecError("\n".join(errs))
    return spec


def node_label(n):
    return n.get("label") or SERVICES[n["service"]]["label"]


def children(spec, gid):
    """(subgroups, nodes) directly inside group gid (None = top level)."""
    return ([g for g in spec["groups"] if (g.get("parent") or None) == gid],
            [n for n in spec["nodes"] if (n.get("group") or None) == gid])


def ranks(spec):
    """Longest-path rank per node (left-to-right flow order); back edges ignored."""
    adj = {n["id"]: [] for n in spec["nodes"]}
    for e in spec["edges"]:
        adj[e["from"]].append(e["to"])
    state, back = {}, set()

    def dfs(u):
        state[u] = 1
        for v in adj[u]:
            if state.get(v) == 1:
                back.add((u, v))
            elif v not in state:
                dfs(v)
        state[u] = 2

    sys.setrecursionlimit(10000)
    for u in adj:
        if u not in state:
            dfs(u)
    r = {u: 0 for u in adj}
    for _ in range(len(adj)):
        changed = False
        for u in adj:
            for v in adj[u]:
                if (u, v) not in back and r[v] < r[u] + 1:
                    r[v] = r[u] + 1
                    changed = True
        if not changed:
            break
    return r


def group_rank(spec, gid, r):
    subs, nodes = children(spec, gid)
    vals = [r[n["id"]] for n in nodes] + [group_rank(spec, g["id"], r) for g in subs]
    return min(vals) if vals else 0


# --------------------------------------------------------------------------- mermaid
def mm_id(prefix, i):
    return prefix + re.sub(r"[^A-Za-z0-9_]", "_", i)


def mm_text(t):
    return str(t).replace('"', "#quot;")


def render_mermaid(spec):
    out = [f"%% {spec['title']}", f"flowchart {spec['direction']}"]

    def emit(gid, depth):
        ind = "  " * (depth + 1)
        subs, nodes = children(spec, gid)
        for n in nodes:
            out.append(f'{ind}{mm_id("n_", n["id"])}["{mm_text(node_label(n))}"]:::{SERVICES[n["service"]]["category"]}')
        for g in subs:
            out.append(f'{ind}subgraph {mm_id("g_", g["id"])}["{mm_text(g["label"])}"]')
            emit(g["id"], depth + 1)
            out.append(f"{ind}end")

    emit(None, 0)
    for e in spec["edges"]:
        arrow = "<-->" if e.get("bidirectional") else ("-.->" if e.get("style") == "dashed" else "-->")
        if e.get("bidirectional") and e.get("style") == "dashed":
            arrow = "<-.->"
        lab = f'|"{mm_text(e["label"])}"|' if e.get("label") else ""
        out.append(f'  {mm_id("n_", e["from"])} {arrow}{lab} {mm_id("n_", e["to"])}')
    used = {SERVICES[n["service"]]["category"] for n in spec["nodes"]}
    for c in sorted(used):
        out.append(f"  classDef {c} fill:#fff,stroke:{COLORS[c]},stroke-width:2px,color:#232F3E")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- draw.io
NODE_W, NODE_H, ICON, GAP, PAD, HEAD, MAX_STACK = 120, 110, 60, 40, 20, 40, 5
BASE = ("sketch=0;outlineConnect=0;fontColor=#232F3E;gradientColor=none;html=1;fontSize=12;fontStyle=0;"
        "aspect=fixed;verticalLabelPosition=bottom;verticalAlign=top;align=center;")
GR = ("points=[[0,0,0],[0.25,0,0],[0.5,0,0],[0.75,0,0],[1,0,0],[1,0.25,0],[1,0.5,0],[1,0.75,0],[1,1,0],"
      "[0.75,1,0],[0.5,1,0],[0.25,1,0],[0,1,0],[0,0.75,0],[0,0.5,0],[0,0.25,0]];outlineConnect=0;gradientColor=none;"
      "html=1;whiteSpace=wrap;fontSize=12;fontStyle=0;container=1;pointerEvents=0;collapsible=0;recursiveResize=0;")
GROUP_STYLE = {
    "cloud": GR + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_aws_cloud_alt;strokeColor=#232F3E;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#232F3E;dashed=0;",
    "region": GR + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_region;strokeColor=#00A4A6;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=1;",
    "account": GR + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_account;strokeColor=#CD2264;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#CD2264;dashed=0;",
    "vpc": GR + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_vpc2;strokeColor=#8C4FFF;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#AAB7B8;dashed=0;",
    "public-subnet": GR + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;grStroke=0;strokeColor=#7AA116;fillColor=#F2F6E8;verticalAlign=top;align=left;spacingLeft=30;fontColor=#248814;dashed=0;",
    "private-subnet": GR + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_security_group;grStroke=0;strokeColor=#00A4A6;fillColor=#E6F6F7;verticalAlign=top;align=left;spacingLeft=30;fontColor=#147EBA;dashed=0;",
    "az": "fillColor=none;strokeColor=#147EBA;dashed=1;verticalAlign=top;fontStyle=0;fontColor=#147EBA;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;",
    "onprem": GR + "shape=mxgraph.aws4.group;grIcon=mxgraph.aws4.group_corporate_data_center;strokeColor=#7D8998;fillColor=none;verticalAlign=top;align=left;spacingLeft=30;fontColor=#5A6C86;dashed=0;",
    "generic": "fillColor=none;strokeColor=#5A6C86;dashed=1;verticalAlign=top;fontStyle=0;fontColor=#5A6C86;whiteSpace=wrap;html=1;container=1;collapsible=0;recursiveResize=0;",
}


def node_style(n):
    s = SERVICES[n["service"]]
    color = COLORS[s["category"]]
    d = s["drawio"]
    if not d:
        return "rounded=1;whiteSpace=wrap;html=1;fillColor=#FFFFFF;strokeColor=#232F3E;fontColor=#232F3E;fontSize=12;", 80, 50
    kind, name = d.split(":", 1)
    if kind == "res":
        return (BASE + f"fillColor={color};strokeColor=#ffffff;shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.{name};"), ICON, ICON
    return (BASE + f"fillColor={color};strokeColor=none;pointerEvents=1;shape=mxgraph.aws4.{name};"), ICON, ICON


def render_drawio(spec):
    r = ranks(spec)
    horizontal = spec["direction"] == "LR"
    pos = {}  # id -> (x, y, w, h) relative to parent

    def layout(gid):
        """Return (w, h) of the content of container gid and fill pos for its children."""
        subs, nodes = children(spec, gid)
        items = []
        for g in subs:
            items.append((group_rank(spec, g["id"], r), "g", g))
        for n in nodes:
            items.append((r[n["id"]], "n", n))
        items.sort(key=lambda t: t[0])
        sized = []
        for rk, kind, it in items:
            if kind == "g":
                w, h = layout(it["id"])
                w, h = w + 2 * PAD, h + HEAD + PAD
            else:
                w, h = NODE_W, NODE_H
            sized.append((rk, it["id"], w, h))
        if not sized:
            return NODE_W, NODE_H // 2
        # Columns (LR) or rows (TB) follow the flow rank; same-rank items stack on the other axis.
        # Very tall stacks wrap into extra columns so the picture stays roughly landscape.
        by_rank = {}
        for rk, i, w, h in sized:
            by_rank.setdefault(rk, []).append((i, w, h))
        flow = 0  # position along the flow axis
        span = 0  # extent across the flow axis
        columns = []  # (ids, extent) per column, to centre them on the span afterwards
        for rk in sorted(by_rank):
            stack = by_rank[rk]
            for k in range(0, len(stack), MAX_STACK):
                chunk = stack[k:k + MAX_STACK]
                if horizontal:
                    cw = max(w for _, w, _ in chunk)
                    y = 0
                    for i, w, h in chunk:
                        pos[i] = (flow + (cw - w) // 2, y, w, h)
                        y += h + GAP
                    span = max(span, y - GAP)
                    columns.append(([i for i, _, _ in chunk], y - GAP))
                    flow += cw + GAP
                else:
                    rh = max(h for _, _, h in chunk)
                    x = 0
                    for i, w, h in chunk:
                        pos[i] = (x, flow + (rh - h) // 2, w, h)
                        x += w + GAP
                    span = max(span, x - GAP)
                    columns.append(([i for i, _, _ in chunk], x - GAP))
                    flow += rh + GAP
        for ids, extent in columns:
            shift = (span - extent) // 2
            for i in ids:
                x, y, w, h = pos[i]
                pos[i] = (x, y + shift, w, h) if horizontal else (x + shift, y, w, h)
        flow -= GAP
        return (flow, span) if horizontal else (span, flow)

    tw, th = layout(None)
    mxfile = ET.Element("mxfile", host="app.diagrams.net")
    diagram = ET.SubElement(mxfile, "diagram", name=spec["title"], id="aws-sa-diagram")
    model = ET.SubElement(diagram, "mxGraphModel", dx="1000", dy="600", grid="1", gridSize="10", guides="1",
                          tooltips="1", connect="1", arrows="1", fold="1", page="1", pageScale="1",
                          pageWidth=str(max(1169, tw + 100)), pageHeight=str(max(827, th + 100)), math="0", shadow="0")
    root = ET.SubElement(model, "root")
    ET.SubElement(root, "mxCell", id="0")
    ET.SubElement(root, "mxCell", id="1", parent="0")

    def cid(i):
        return "c_" + i

    def emit(gid):
        subs, nodes = children(spec, gid)
        parent = cid(gid) if gid else "1"
        for g in subs:
            x, y, w, h = pos[g["id"]]
            if gid is None:
                x, y = x + 40, y + 40
            else:
                x, y = x + PAD, y + HEAD
            c = ET.SubElement(root, "mxCell", id=cid(g["id"]), value=g["label"], style=GROUP_STYLE[g["type"]],
                              vertex="1", parent=parent)
            ET.SubElement(c, "mxGeometry", {"x": str(x), "y": str(y), "width": str(w), "height": str(h), "as": "geometry"})
            emit(g["id"])
        for n in nodes:
            x, y, w, h = pos[n["id"]]
            style, iw, ih = node_style(n)
            if gid is None:
                x, y = x + 40, y + 40
            else:
                x, y = x + PAD, y + HEAD
            x += (w - iw) // 2
            c = ET.SubElement(root, "mxCell", id=cid(n["id"]), value=node_label(n), style=style, vertex="1", parent=parent)
            ET.SubElement(c, "mxGeometry", {"x": str(x), "y": str(y), "width": str(iw), "height": str(ih), "as": "geometry"})

    emit(None)
    for k, e in enumerate(spec["edges"]):
        style = "edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=block;endFill=1;strokeColor=#232F3E;fontSize=11;"
        if e.get("style") == "dashed":
            style += "dashed=1;"
        if e.get("bidirectional"):
            style += "startArrow=block;startFill=1;"
        c = ET.SubElement(root, "mxCell", id=f"e_{k}", value=e.get("label", ""), style=style, edge="1", parent="1",
                          source=cid(e["from"]), target=cid(e["to"]))
        ET.SubElement(c, "mxGeometry", {"relative": "1", "as": "geometry"})
    ET.indent(mxfile)
    return ET.tostring(mxfile, encoding="unicode") + "\n"


# --------------------------------------------------------------------------- PlantUML
PUML_GROUPS = {
    "cloud": ("Groups/AWSCloud", "AWSCloudGroup"), "region": ("Groups/Region", "RegionGroup"),
    "account": ("Groups/AWSAccount", "AWSAccountGroup"), "vpc": ("Groups/VPC", "VPCGroup"),
    "az": ("Groups/AvailabilityZone", "AvailabilityZoneGroup"),
    "public-subnet": ("Groups/PublicSubnet", "PublicSubnetGroup"),
    "private-subnet": ("Groups/PrivateSubnet", "PrivateSubnetGroup"),
    "onprem": ("Groups/CorporateDataCenter", "CorporateDataCenterGroup"),
    "generic": ("Groups/Generic", "GenericGroup"),
}


def alias(i):
    return re.sub(r"\W", "_", i)


def pu_text(t):
    return str(t).replace('"', "'")


def render_plantuml(spec):
    base = f"https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/{PUML_VERSION}/dist"
    out = ["@startuml", f"title {pu_text(spec['title'])}", f"!define AWSPuml {base}", "!include AWSPuml/AWSCommon.puml"]
    seen = set()
    for n in spec["nodes"]:
        p = SERVICES[n["service"]]["plantuml"]
        if p and p not in seen:
            seen.add(p)
            out.append(f"!include AWSPuml/{p}.puml")
    for g in {g["type"] for g in spec["groups"]}:
        out.append(f"!include AWSPuml/{PUML_GROUPS[g][0]}.puml")
    out += ["", "hide stereotype", "skinparam linetype ortho", "left to right direction" if spec["direction"] == "LR" else "top to bottom direction", ""]

    def emit(gid, depth):
        ind = "  " * depth
        subs, nodes = children(spec, gid)
        for n in nodes:
            p = SERVICES[n["service"]]["plantuml"]
            if p:
                tech = SERVICES[n["service"]]["label"] if n.get("label") else "AWS"
                out.append(f'{ind}{p.split("/")[1]}({alias(n["id"])}, "{pu_text(node_label(n))}", "{tech}")')
            else:
                out.append(f'{ind}rectangle "{pu_text(node_label(n))}" as {alias(n["id"])}')
        for g in subs:
            out.append(f'{ind}{PUML_GROUPS[g["type"]][1]}({alias(g["id"])}, "{pu_text(g["label"])}") {{')
            emit(g["id"], depth + 1)
            out.append(f"{ind}}}")

    emit(None, 0)
    out.append("")
    for e in spec["edges"]:
        arrow = "<-->" if e.get("bidirectional") else "-->"
        if e.get("style") == "dashed":
            arrow = "<..>" if e.get("bidirectional") else "..>"
        lab = f': {pu_text(e["label"])}' if e.get("label") else ""
        out.append(f'{alias(e["from"])} {arrow} {alias(e["to"])}{lab}')
    out.append("@enduml")
    return "\n".join(out) + "\n"


# --------------------------------------------------------------------------- python diagrams
def render_python(spec):
    imports = {"from diagrams import Diagram, Cluster, Edge"}
    for n in spec["nodes"]:
        d = SERVICES[n["service"]]["diagrams"]
        if d:
            mod, cls = d.rsplit(".", 1)
            pkg = f"diagrams.{mod}" if mod.startswith("onprem") else f"diagrams.aws.{mod}"
            imports.add(f"from {pkg} import {cls} as {cls}_{mod.replace('.', '_')}")
        else:
            imports.add("from diagrams.generic.blank import Blank")
    title = spec["title"].replace('"', "'")
    slug = re.sub(r"[^a-z0-9]+", "-", spec["title"].lower()).strip("-") or "diagram"
    out = sorted(imports) + ["", f'with Diagram("{title}", filename="{slug}", direction="{spec["direction"]}", show=False):']

    def var(i):
        return "n_" + alias(i)

    def emit(gid, depth):
        ind = "    " * depth
        subs, nodes = children(spec, gid)
        for n in nodes:
            d = SERVICES[n["service"]]["diagrams"]
            cls = f"{d.rsplit('.', 1)[1]}_{d.rsplit('.', 1)[0].replace('.', '_')}" if d else "Blank"
            out.append(f'{ind}{var(n["id"])} = {cls}("{node_label(n)}")')
        for g in subs:
            out.append(f'{ind}with Cluster("{g["label"]}"):')
            before = len(out)
            emit(g["id"], depth + 1)
            if len(out) == before:
                out.append(f"{ind}    pass")

    emit(None, 1)
    for e in spec["edges"]:
        attrs = []
        if e.get("label"):
            attrs.append(f'label="{e["label"]}"')
        if e.get("style") == "dashed":
            attrs.append('style="dashed"')
        if e.get("bidirectional"):
            attrs.append('dir="both"')
        out.append(f'    {var(e["from"])} >> Edge({", ".join(attrs)}) >> {var(e["to"])}')
    return "\n".join(out) + "\n"


RENDERERS = {"mermaid": (render_mermaid, ".mmd"), "drawio": (render_drawio, ".drawio"),
             "plantuml": (render_plantuml, ".puml"), "python": (render_python, ".py")}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("spec")
    ap.add_argument("--format", choices=list(RENDERERS) + ["all"], default="mermaid")
    ap.add_argument("-o", "--outdir")
    ap.add_argument("--validate-only", action="store_true")
    a = ap.parse_args()
    try:
        spec = load_spec(a.spec)
    except SpecError as e:
        print(f"Invalid spec:\n{e}", file=sys.stderr)
        sys.exit(2)
    if a.validate_only:
        print(f"OK: {len(spec['nodes'])} nodes, {len(spec['groups'])} groups, {len(spec['edges'])} edges")
        return
    fmts = list(RENDERERS) if a.format == "all" else [a.format]
    if len(fmts) > 1 and not a.outdir:
        print("--format all needs -o OUTDIR", file=sys.stderr)
        sys.exit(2)
    stem = re.sub(r"[^a-z0-9]+", "-", spec["title"].lower()).strip("-") or "diagram"
    for f in fmts:
        text = RENDERERS[f][0](spec)
        if a.outdir:
            os.makedirs(a.outdir, exist_ok=True)
            path = os.path.join(a.outdir, stem + RENDERERS[f][1])
            open(path, "w", encoding="utf-8").write(text)
            print("wrote", path)
        else:
            sys.stdout.write(text)


if __name__ == "__main__":
    main()
