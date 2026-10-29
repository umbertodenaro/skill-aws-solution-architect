from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Fargate as Fargate_compute
from diagrams.aws.database import Aurora as Aurora_database
from diagrams.aws.general import Users as Users_general
from diagrams.aws.network import ALB as ALB_network
from diagrams.aws.network import CloudFront as CloudFront_network
from diagrams.aws.network import NATGateway as NATGateway_network
from diagrams.aws.security import WAF as WAF_security
from diagrams.aws.storage import S3 as S3_storage

with Diagram("Three-tier web app on AWS", filename="three-tier-web-app-on-aws", direction="LR", show=False):
    n_users = Users_general("Users")
    with Cluster("AWS Cloud"):
        with Cluster("eu-west-1"):
            n_cf = CloudFront_network("Amazon CloudFront")
            n_waf = WAF_security("AWS WAF")
            n_s3 = S3_storage("Static assets")
            with Cluster("VPC"):
                n_alb = ALB_network("ALB")
                n_db = Aurora_database("Aurora (Multi-AZ)")
                with Cluster("AZ a"):
                    with Cluster("Public subnet"):
                        n_nat1 = NATGateway_network("NAT Gateway")
                    with Cluster("Private subnet (app)"):
                        n_ecs1 = Fargate_compute("App tasks")
                with Cluster("AZ b"):
                    with Cluster("Public subnet"):
                        n_nat2 = NATGateway_network("NAT Gateway")
                    with Cluster("Private subnet (app)"):
                        n_ecs2 = Fargate_compute("App tasks")
    n_users >> Edge(label="HTTPS") >> n_cf
    n_cf >> Edge() >> n_waf
    n_waf >> Edge() >> n_alb
    n_cf >> Edge(label="static", style="dashed") >> n_s3
    n_alb >> Edge() >> n_ecs1
    n_alb >> Edge() >> n_ecs2
    n_ecs1 >> Edge() >> n_db
    n_ecs2 >> Edge() >> n_db
    n_ecs1 >> Edge(style="dashed") >> n_nat1
    n_ecs2 >> Edge(style="dashed") >> n_nat2
