#!/usr/bin/env python3
"""Verify service_catalog.json icon identifiers against the upstream icon sources.

Maintainer tool (needs network). Run it whenever the catalog changes or AWS ships
new icon releases, so diagrams never reference an icon that does not exist.

Sources:
  draw.io   jgraph/drawio  Sidebar-AWS4.js          (resIcon / shape names)
  PlantUML  awslabs/aws-icons-for-plantuml  dist/    (<Category>/<Name>.puml)
  diagrams  PyPI package `diagrams`                  (diagrams.aws.<module>.<Class>)

Usage: python3 verify_catalog.py [--puml-dir PATH] [--drawio-js PATH]
Exit code 1 if any identifier is missing.
"""
import argparse
import importlib
import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DRAWIO_URL = "https://raw.githubusercontent.com/jgraph/drawio/dev/src/main/webapp/js/diagramly/sidebar/Sidebar-AWS4.js"
PUML_REPO = "https://github.com/awslabs/aws-icons-for-plantuml.git"


def drawio_names(path):
    js = open(path, encoding="utf-8").read() if path else urllib.request.urlopen(DRAWIO_URL, timeout=60).read().decode()
    res = set(re.findall(r"resIcon=' \+ gn \+ '\.(\w+)", js))
    shp = set(re.findall(r"n\d? \+ '(\w+);", js))
    return res, shp


def puml_files(path):
    if not path:
        path = os.path.join(tempfile.mkdtemp(), "puml")
        subprocess.run(["git", "clone", "-q", "--depth", "1", PUML_REPO, path], check=True)
    dist = os.path.join(path, "dist")
    out = set()
    for cat in os.listdir(dist):
        d = os.path.join(dist, cat)
        if os.path.isdir(d):
            out.update(f"{cat}/{f[:-5]}" for f in os.listdir(d) if f.endswith(".puml"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--puml-dir")
    ap.add_argument("--drawio-js")
    a = ap.parse_args()
    cat = json.load(open(os.path.join(HERE, "service_catalog.json")))["services"]
    res, shp = drawio_names(a.drawio_js)
    puml = puml_files(a.puml_dir)
    bad = []
    for key, s in cat.items():
        d = s["drawio"]
        if d:
            kind, name = d.split(":", 1)
            if name not in (res if kind == "res" else shp):
                bad.append((key, "drawio", d))
        if s["plantuml"]:
            if s["plantuml"] not in puml:
                bad.append((key, "plantuml", s["plantuml"]))
            elif a.puml_dir:
                # the include's macro must carry the file's basename (used by render_diagram.py)
                macro = s["plantuml"].split("/")[1]
                src = open(os.path.join(a.puml_dir, "dist", s["plantuml"] + ".puml"), encoding="utf-8").read()
                if f"!define {macro}(" not in src:
                    bad.append((key, "plantuml-macro", macro))
        if s["diagrams"]:
            mod, cls = s["diagrams"].rsplit(".", 1)
            try:
                m = importlib.import_module(f"diagrams.aws.{mod}") if not mod.startswith("onprem") else importlib.import_module(f"diagrams.{mod}")
                if not hasattr(m, cls):
                    bad.append((key, "diagrams", s["diagrams"]))
            except ImportError as e:
                bad.append((key, "diagrams", f"{s['diagrams']} ({e})"))
    for b in bad:
        print("MISSING", *b)
    print(f"{len(cat)} services checked, {len(bad)} problems")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
