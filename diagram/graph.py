import json
from dataclasses import dataclass, field


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
