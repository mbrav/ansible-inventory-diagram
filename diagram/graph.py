import json
from dataclasses import dataclass, field

from diagrams import Cluster
from diagrams.elastic.elasticsearch import ElasticSearch
from diagrams.k8s.infra import ETCD, Master, Node
from diagrams.onprem.ci import ConcourseCI
from diagrams.onprem.database import Clickhouse, Mssql, PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Consul, Haproxy, Nginx
from diagrams.onprem.queue import Kafka
from diagrams.onprem.registry import Harbor
from diagrams.onprem.security import Vault
from diagrams.programming.flowchart import Database as DBDiagram
from patch import OsageDiagram


@dataclass
class AnsibleHost:
    """Ansible Host dataclass representation"""

    name: str = field(default_factory=str)
    host: str = field(default_factory=str)

    def __repr__(self) -> str:
        return f"Host {self.name} ({self.host})"


@dataclass
class AnsibleGroup:
    """Ansible Group dataclass representation"""

    name: str = field(default_factory=str)
    parent: str | None = field(default=None)
    children: list["AnsibleGroup"] = field(default_factory=list)
    hosts: list[AnsibleHost] = field(default_factory=list)

    def __repr__(self) -> str:
        return f"Group {self.name}[{len(self.children)}] ({len(self.hosts)})"


class InventoryGraph:
    """Inventory graph generation class"""

    def __init__(self, inventory: str) -> None:
        self.inventory = json.loads(inventory)
        self.hosts = {}
        self.groups = {}

    def generate_tree(self) -> dict[str, AnsibleGroup]:
        """Naive tree generation algorithm from Ansible JSON inventory"""

        # Generate hosts
        for k, v in self.inventory.get("_meta", {}).get("hostvars", {}).items():
            host = AnsibleHost(name=k, host=v.get("ansible_host", ">ip unknown<"))
            self.hosts[k] = host

        # Generate groups
        for k, v in self.inventory.items():
            if k not in ("all", "_meta"):
                group = AnsibleGroup(
                    name=k,
                    hosts=self._get_group_hosts(k),
                    children=self._get_children_groups(k),
                )
                self.groups[k] = group

        # Shake tree
        groups = list(self.groups.keys())
        for g in self.groups.values():
            for child in g.children:
                if child.name in groups:
                    del groups[groups.index(child.name)]
        for k in list(self.groups.keys()):
            if k not in groups:
                del self.groups[k]

        return self.groups

    def _get_children_groups(self, group_name: str) -> list[AnsibleGroup]:
        """Recursive child group list generation"""

        # Parse group children if present
        children = []
        for group_child in self.inventory.get(group_name, {}).get("children", []):
            children.append(
                AnsibleGroup(
                    name=group_child,
                    hosts=self._get_group_hosts(group_child),
                    children=self._get_children_groups(group_child),
                )
            )

        return children

    def _get_group_hosts(self, group_name: str) -> list[AnsibleHost]:
        """Get group hosts"""

        hosts = []
        for host in self.inventory.get(group_name, {}).get("hosts", []):
            hosts.append(self.hosts[host])
        return hosts


# Attributes for services
# https://graphviz.org/docs/attrs
node_attr = {"fontsize": "10", "pad": "5.0"}
graph_attr = {}


def generate_ansible_graph(
    data: dict[str, AnsibleGroup],
    name: str = "Ansible inventory diagram",
    filename: str = "ansible_inventory_diagram",
    outformat: str = "pdf",
    show: bool = False,
) -> None:
    """Ansible inventory graph generation"""
    with OsageDiagram(
        name=name,
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
            if (
                "postgres" in group_name_lower
                or "stolon" in group_name_lower
                or "patroni" in group_name_lower
            ):
                PostgreSQL(host.name)
            elif "mysql" in group_name_lower:
                Mssql(host.name)
            elif "elastic" in group_name_lower:
                ElasticSearch(host.name)
            elif "haproxy" in group_name_lower:
                Haproxy(host.name)
            elif "consul" in group_name_lower:
                Consul(host.name)
            elif "vault" in group_name_lower:
                Vault(host.name)
            elif "concourse" in group_name_lower:
                ConcourseCI(host.name)
            elif "harbor" in group_name_lower:
                Harbor(host.name)
            elif "etcd" in group_name_lower:
                ETCD(host.name)
            elif "kafka" in group_name_lower:
                Kafka(host.name)
            elif "grafana" in group_name_lower:
                Grafana(host.name)
            elif "prom" in group_name_lower:
                Prometheus(host.name)
            elif "nginx" in group_name_lower:
                Nginx(host.name)
            elif "clickhouse" in group_name_lower:
                Clickhouse(host.name)
            elif "k8s" in group_name_lower:
                if "master" in group_name_lower:
                    Master(host.name)
                else:
                    Node(host.name)
            elif "redis" in group_name_lower:
                Redis(host.name)
            # elif "minio" in group_name_lower:
            #     Redis(host.name)
            else:
                DBDiagram(host.name)

        # Draw group children
        for child in group.children:
            # Recurse
            _graph_recurse(child.name, child)