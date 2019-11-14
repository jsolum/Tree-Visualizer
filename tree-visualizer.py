import sys, csv
'''
Example Usage: 

python tree-visualizer.py recursion_output.txt --csv-delimiter '|' --format '{code} {name}'
'''

args = {}
STATIC_ARGS = 1
for idx, arg in enumerate(sys.argv):
    if idx > 0 and idx <= STATIC_ARGS:
        if idx == 1: args['file'] = arg
    if idx > STATIC_ARGS and (idx % 2) == ((STATIC_ARGS + 1) % 2):
        args[arg] = sys.argv[idx+1]

# INPUT
INPUT_CSV        = args['file']
CSV_DELIMITER    = args.get('--csv-delimiter') or ','
NODE_IDENTIFIER  = args.get('--id')            or 'id'
PARENT_REFERENCE = args.get('--parent-id')     or 'parent_id'

# FORMATTING
DATA_FORMAT    = args.get('--format')         or '{code} {name}'
TREE_DELIMITER = args.get('--tree-delimiter') or ' '
SORT_ATTRIBUTE = args.get('--sort-by')        or 'code'
CHILD_SPACING  = 2 * TREE_DELIMITER
SORT_FUNCTION  = lambda x: x.data[SORT_ATTRIBUTE]

class Node:
    def __init__(self, data):
        self.data = data   # Dictionary of Data
        self.children = [] # List of Nodes

    def add_child(self, node):
        self.children.append(node)
        self.children.sort(key=SORT_FUNCTION)

    def parent_id(self):
        return self.data[PARENT_REFERENCE]

    def id(self):
        return self.data[NODE_IDENTIFIER]

def print_tree(root, depth=0):
    print_node(root, depth)
    for child in root.children:
        print_tree(child, depth + 1)
    
def print_node(root, depth):
    print((depth * CHILD_SPACING) + data_formatter(root.data))

def data_formatter(data):
    return DATA_FORMAT.format(**data)

def generate_tree(nodes):
    roots = []
    for key, node in nodes.items():
        if node.parent_id():
            parent = nodes[node.parent_id()]
            parent.add_child(node)
        else:
            roots.append(node)
    roots.sort(key=SORT_FUNCTION)
    return roots

def create_nodes_from_csv():
    nodes = {}
    with open(INPUT_CSV, 'rb') as csvfile:
        data_reader = csv.DictReader(csvfile, delimiter=CSV_DELIMITER)
        for row in data_reader:
            nodes[row[NODE_IDENTIFIER]] = Node(row)
    return nodes

nodes = create_nodes_from_csv()
roots = generate_tree(nodes)

for root in roots:
    print_tree(root)
