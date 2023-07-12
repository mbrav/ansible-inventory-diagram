from diagrams import Cluster, Diagram, Node
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
from patch import OsageDiagram

COPY = "2023 GNU GPL v3.0 - mbrav https://github.com/mbrav/ansible-inventory-diagram"

# Attributes for services
# https://graphviz.org/docs/attrs
node_attr = {"fontsize": "10", "pad": "5.0"}
graph_attr = {}


# @dataclass
# class AnsibleHost:
#     """Ansible Host dataclass representation"""

#     name: str = field(default_factory=str)
#     host: str = field(default_factory=str)

#     def __repr__(self) -> str:
#         return f"Host {self.name} ({self.host})"


# @dataclass
# class AnsibleGroup:
#     """Ansible Group dataclass representation"""

#     name: str = field(default_factory=str)
#     parent: str | None = field(default=None)
#     children: list["AnsibleGroup"] = field(default_factory=list)
#     hosts: list[AnsibleHost] = field(default_factory=list)

#     def __repr__(self) -> str:
#         return f"Group {self.name}[{len(self.children)}] ({len(self.hosts)})"


class InventoryDiagram:
    """Inventory diagram generation class"""

    def __init__(
        self,
        data: dict[str, AnsibleGroup],
        title: str = "Ansible inventory diagram",
        filename: str = "ansible_inventory_diagram",
        outformat: str = "pdf",
        show: bool = False,
    ) -> None:
        self.data = data
        self.title = f"{title}\n{COPY}"
        self.filename = filename
        self.show = show
        self.outformat = outformat

    def generate_grouping(self) -> None:
        """Diagram with hosts sorted into groups and clusters"""
        with OsageDiagram(
            name=self.title,
            filename=self.filename,
            show=self.show,
            outformat=self.outformat,
            graph_attr=graph_attr,
            node_attr=node_attr,
        ):
            for group_name, group in self.data.items():
                self._graph_recurse(group_name, group)

    def generate_diagram(self) -> None:
        """Diagram with hosts and their relations"""
        with Diagram(
            name=self.title,
            filename=self.filename,
            show=self.show,
            outformat=self.outformat,
            graph_attr=graph_attr,
            node_attr=node_attr,
        ):
            for group_name, group in self.data.items():
                self._graph_recurse(group_name, group)

    def _graph_recurse(
        self, cluster_title: str, group: AnsibleGroup, node: Node | None = None
    ) -> None:
        """Graphing recursive logic"""

        with Cluster(cluster_title, direction="TB") as cluster:
            # Draw hosts if present
            group_name_lower = group.name.lower()
            for host in group.hosts:
                label = f"{host.name}\n{host.host}"
                new_node = identify_node(group_name_lower, label)

            # Draw group children
            for child in group.children:
                # Recurse
                self._graph_recurse(child.name, child, node)


def identify_node(name: str, label: str) -> Node:
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
