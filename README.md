[![License](https://img.shields.io/badge/License-BSD_3--Clause-yellow.svg)](https://opensource.org/licenses/BSD-3-Clause)
[![tokei](https://tokei.rs/b1/github/mbrav/ansible-inventory-diagram?category=lines)](https://tokei.rs/b1/github/mbrav/ansible-inventory-diagram)
[![Hits-of-Code](https://hitsofcode.com/github/mbrav/ansible-inventory-diagram?branch=main)](https://hitsofcode.com/github/mbrav/ansible-inventory-diagram/view?branch=main)

# ansible-inventory-diagram

Script for generating infrastructure diagrams from Ansible inventory files

![Example diagram](./ansible_inventory_diagram.png)

[Link to image](https://github.com/mbrav/ansible-inventory-diagram/blob/main/ansible_inventory_diagram.png)

## Prerequisites

Before using this script you must install the [Graphviz library](https://graphviz.org/).

### Inventory file preparation

To prepare the JSON necessary to feed the script you must first prepare it using `ansible-inventory` the following way (YAML, INI, and JSON formats can be used):

```bash
ansible-inventory -i inventory/example.yml --list > inventory/example.json
```

**Note:** The script currently is not able to parse inventories tha have many redefinitions of groups. To do so, a more intricate algorithm is necessary. Currently, a very naive one is implemented. To see what kind of inventory structure works well, see [`inventory/example.yml`](inventory/example.yml).

## Usage

Once you have an outputted JSON inventory file you can run the script:

```bash
python3 diagram/main.py -i inventory/example.json
```

For instructions run

```bash
python3 diagram/main.py -h
```

You will see the following

```text
usage: ansible-inventory-diagram [-h] [-i INVENTORY]
                                 [-o {png,jpg,svg,pdf,dot}] [-n NAME]
                                 [-f FILENAME] [-s]

Script for generating infrastructure diagrams from Ansible inventory files

options:
  -h, --help            show this help message and exit
  -i INVENTORY, --inventory INVENTORY
                        Path to Ansible JSON inventory file
  -o {png,jpg,svg,pdf,dot}, --outformat {png,jpg,svg,pdf,dot}
                        Format of the output format
  -n NAME, --name NAME  Name of the diagram
  -f FILENAME, --filename FILENAME
                        Name of file to output
  -s, --show            Show file after generation using the default program

2023 - mbrav https://github.com/mbrav/ansible-inventory-diagram
```

## Installation

Clone repo

```bash
git clone https://github.com/mbrav/ansible-inventory-diagram.git
cd ansible-inventory-diagram
```

Install Python libraries

```bash
pip3 install -r requirements.txt 
```

Run script

```bash
python3 diagram/main.py
```
