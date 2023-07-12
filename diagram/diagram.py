from diagrams import Cluster

from diagrams.elastic.elasticsearch import ElasticSearch
from diagrams.k8s.infra import ETCD, Master, Node
from diagrams.onprem.auth import Oauth2Proxy
from diagrams.onprem.ci import ConcourseCI
from diagrams.onprem.database import Clickhouse, Mssql, PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Consul, Haproxy, Nginx
from diagrams.onprem.queue import Kafka
from diagrams.onprem.registry import Harbor
from diagrams.onprem.security import Vault
from diagrams.programming.flowchart import Database as DBDiagram
from graph import AnsibleGroup
from patch import OsageDiagram

COPY = "2023 GNU GPL v3.0 - mbrav https://github.com/mbrav/ansible-inventory-diagram"

# Attributes for services
# https://graphviz.org/docs/attrs
node_attr = {"fontsize": "10", "pad": "5.0"}
graph_attr = {}


def generate_ansible_diagram(
    data: dict[str, AnsibleGroup],
    name: str = "Ansible inventory diagram",
    filename: str = "ansible_inventory_diagram",
    outformat: str = "pdf",
    show: bool = False,
) -> None:
    """Ansible inventory diagram generation"""

    title = f"{name}\n{COPY}"
    with OsageDiagram(
        name=title,
        filename=filename,
        show=show,
        outformat=outformat,
        graph_attr=graph_attr,
        node_attr=node_attr,
    ):
        for group_name, group in data.items():
            _graph_recurse(group_name, group)


def _graph_recurse(cluster_title: str, group: AnsibleGroup) -> None:
    """Graphing recursive logic"""

    with Cluster(cluster_title, direction="TB"):
        # Draw hosts if present
        group_name_lower = group.name.lower()
        for host in group.hosts:
            label = f"{host.name}\n{host.host}"
            if (
                "postgres" in group_name_lower
                or "stolon" in group_name_lower
                or "patroni" in group_name_lower
            ):
                PostgreSQL(label)
            elif "mysql" in group_name_lower:
                Mssql(label)
            elif "elastic" in group_name_lower:
                ElasticSearch(label)
            elif "haproxy" in group_name_lower:
                Haproxy(label)
            elif "consul" in group_name_lower:
                Consul(label)
            elif "vault" in group_name_lower:
                Vault(label)
            elif "concourse" in group_name_lower:
                ConcourseCI(label)
            elif "harbor" in group_name_lower:
                Harbor(label)
            elif "kafka" in group_name_lower:
                Kafka(label)
            elif "grafana" in group_name_lower:
                Grafana(label)
            elif "prom" in group_name_lower:
                Prometheus(label)
            elif "nginx" in group_name_lower:
                Nginx(label)
            elif "clickhouse" in group_name_lower:
                Clickhouse(label)
            elif "k8s" in group_name_lower or "kube" in group_name_lower:
                if (
                    "master" in group_name_lower
                    or "kube_control_plane" in group_name_lower
                ):
                    Master(label)
                elif "etcd" in group_name_lower:
                    ETCD(label)
                else:
                    Node(label)
            elif "etcd" in group_name_lower:
                ETCD(label)
            elif "redis" in group_name_lower:
                Redis(label)
            elif "proxy" in group_name_lower:
                Oauth2Proxy(label)
            # elif "minio" in group_name_lower:
            #     Redis(label)
            else:
                DBDiagram(label)

        # Draw group children
        for child in group.children:
            # Recurse
            _graph_recurse(child.name, child)
