import yaml
from graphviz import Digraph
import sys


def draw_dag(data, output):
    # Create a mapping between node IDs and names with types
    node_mapping = {str(list(node.keys())[0]): str(list(node.values())[0]) for node in data['nodes']}

    # Initialize the Digraph object
    dot = Digraph()

    # Add nodes to the Digraph with names and types on new lines, displayed in red
    for nid, ninfo in node_mapping.items():
        nname, ntype = ninfo.split(',')
        nlabel = f'{nname}\n{ntype}'
        dot.node(nname, label=nlabel, style='filled', color='lightblue')

    # Add edges to the Digraph
    edges = set()
    for edge in data['flow']:
        sources, targets = edge.split('>>')
        sources = [node_mapping[s.strip()].split(',')[0] for s in sources.split(',')]
        targets = [node_mapping[t.strip()].split(',')[0] for t in targets.split(',')]

        for source in sources:
            for target in targets:
                edge_tuple = (source, target)
                if edge_tuple not in edges:  # Check for duplicate edges
                    edges.add(edge_tuple)
                    dot.edge(source, target)

    # Generate the digraph
    dot.format = 'png'
    dot.render(outfile=output, view=True)
    dot.save(output.replace('.png', '.gv'))

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        exit("You need 2 argument: python drawDAG.py <path-to-yaml> <path-to-output>")
    filename = sys.argv[1]
    output = sys.argv[2]
    with open(filename) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    draw_dag(data, output)