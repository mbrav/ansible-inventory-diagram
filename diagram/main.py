import argparse
import os

from graph import InventoryGraph, generate_ansible_graph

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

parser = argparse.ArgumentParser(
    prog="ansible-inventory-diagram",
    description="Script for generating infrastructure diagrams from Ansible inventory files",
    epilog="2023 - mbrav https://github.com/mbrav/ansible-inventory-diagram",
)
parser.add_argument(
    "-i",
    "--inventory",
    action="store",
    help="Path to Ansible JSON inventory file",
    default=f"{SCRIPT_DIR}/../inventory/example.json",
)
parser.add_argument(
    "-o",
    "--outformat",
    action="store",
    help="Format of the output format",
    default="pdf",
    choices=("png", "jpg", "svg", "pdf", "dot"),
)
parser.add_argument(
    "-n",
    "--name",
    action="store",
    help="Name of the diagram",
    default="Ansible inventory diagram",
)
parser.add_argument(
    "-f",
    "--filename",
    action="store",
    help="Name of file to output",
    default="ansible_inventory_diagram",
)
parser.add_argument(
    "-s",
    "--show",
    help="Show file after generation using the default program",
    action="store_true",
)

if __name__ == "__main__":
    """Run CLI with argument parsing"""

    args = parser.parse_args()
    # Load inventory
    with open(args.inventory, "r") as file:
        inventory = file.read().rstrip()

    # Create graph class
    graph = InventoryGraph(inventory)

    # Generate tree
    tree = graph.generate_tree()

    # Generate graph
    generate_ansible_graph(
        data=tree,
        name=args.name,
        filename=args.filename,
        show=args.show,
        outformat=args.outformat,
    )
