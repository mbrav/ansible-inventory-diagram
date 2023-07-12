from diagrams import Cluster
from diagrams import Diagram as OsageDiagram
from diagrams import Node
from diagrams.elastic.elasticsearch import ElasticSearch
from diagrams.k8s.infra import ETCD, Master
from diagrams.k8s.infra import Node as Worker
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

# from patch import OsageDiagram

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


def _graph_recurse(
    cluster_title: str, group: AnsibleGroup, node: Node | None = None
) -> None:
    """Graphing recursive logic"""

    with Cluster(cluster_title, direction="TB"):
        # Draw hosts if present
        group_name_lower = group.name.lower()
        for host in group.hosts:
            label = f"{host.name}\n{host.host}"
            new_node = _identify_node(group_name_lower, label)

        # Draw group children
        for child in group.children:
            # Recurse
            _graph_recurse(child.name, child, node)


def _identify_node(name: str, label: str) -> Node:
    """Identify what kind of node by name and return icon with label"""

    if "postgres" in name or "stolon" in name or "patroni" in name:
        return PostgreSQL(label)
    elif "mysql" in name:
        return Mssql(label)
    elif "elastic" in name:
        ElasticSearch(label)
    elif "haproxy" in name:
        return Haproxy(label)
    elif "consul" in name:
        return Consul(label)
    elif "vault" in name:
        return Vault(label)
    elif "concourse" in name:
        ConcourseCI(label)
    elif "harbor" in name:
        return Harbor(label)
    elif "kafka" in name:
        return Kafka(label)
    elif "grafana" in name:
        return Grafana(label)
    elif "prom" in name:
        return Prometheus(label)
    elif "nginx" in name:
        return Nginx(label)
    elif "clickhouse" in name:
        return Clickhouse(label)
    elif "k8s" in name or "kube" in name:
        if "master" in name or "kube_control_plane" in name:
            return Master(label)
        elif "etcd" in name:
            return ETCD(label)
        else:
            return Worker(label)
    elif "etcd" in name:
        return ETCD(label)
    elif "redis" in name:
        return Redis(label)
    elif "proxy" in name:
        return Oauth2Proxy(label)
    # elif "minio" in name:
    #     Redis(label)
    else:
        return DBDiagram(label)
