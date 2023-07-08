from diagrams import Diagram
from graphviz import Digraph


class OsageDiagram(Diagram):
    """Patched Diagram Class with osage set as engine"""

    __directions = ("TB", "BT", "LR", "RL")
    __curvestyles = ("ortho", "curved")
    __outformats = ("png", "jpg", "svg", "pdf", "dot")

    # fmt: off
    _default_graph_attrs = {
        "pad": "2.0",
        "splines": "ortho",
        "nodesep": "0.60",
        "ranksep": "0.75",
        "fontname": "Sans-Serif",
        "fontsize": "15",
        "fontcolor": "#2D3436",
    }
    _default_node_attrs = {
        "shape": "box",
        "style": "rounded",
        "fixedsize": "true",
        "width": "1.4",
        "height": "1.4",
        "labelloc": "b",
        "imagescale": "true",
        "fontname": "Sans-Serif",
        "fontsize": "13",
        "fontcolor": "#2D3436",
    }
    _default_edge_attrs = {
        "color": "#7B8894",
    }

    def __init__(
        self,
        name: str = "",
        filename: str = "",
        direction: str = "LR",
        curvestyle: str = "ortho",
        outformat: str = "png",
        autolabel: bool = False,
        show: bool = True,
        strict: bool = False,
        graph_attr: dict = {},
        node_attr: dict = {},
        edge_attr: dict = {},
    ):
        self.name = name
        if not name and not filename:
            filename = "diagrams_image"
        elif not filename:
            filename = "_".join(self.name.split()).lower()
        self.filename = filename
        self.dot = Digraph(
            self.name, filename=self.filename, engine="osage", strict=strict
        )

        # Set attributes.
        for k, v in self._default_graph_attrs.items():
            self.dot.graph_attr[k] = v
        self.dot.graph_attr["label"] = self.name
        for k, v in self._default_node_attrs.items():
            self.dot.node_attr[k] = v 
        for k, v in self._default_edge_attrs.items():
            self.dot.edge_attr[k] = v

        if not self._validate_direction(direction):
            raise ValueError(f'"{direction}" is not a valid direction')
        self.dot.graph_attr["rankdir"] = direction

        if not self._validate_curvestyle(curvestyle):
            raise ValueError(f'"{curvestyle}" is not a valid curvestyle')
        self.dot.graph_attr["splines"] = curvestyle

        if isinstance(outformat, list):
            for one_format in outformat:
                if not self._validate_outformat(one_format):
                    raise ValueError(f'"{one_format}" is not a valid output format')
        else:
            if not self._validate_outformat(outformat):
                raise ValueError(f'"{outformat}" is not a valid output format')
        self.outformat = outformat

        # Merge passed in attributes
        self.dot.graph_attr.update(graph_attr)
        self.dot.node_attr.update(node_attr)
        self.dot.edge_attr.update(edge_attr)

        self.show = show
        self.autolabel = autolabel
