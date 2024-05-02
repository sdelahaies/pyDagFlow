import networkx as nx
import matplotlib.pyplot as plt

def draw_dag(dag_definition):
    G = nx.DiGraph()

    for edge in dag_definition:
        sources, targets = edge.split('>>')
        source_nodes = [int(node) for node in sources.split(',')]
        target_nodes = [int(node) for node in targets.split(',')]
        for source in source_nodes:
            for target in target_nodes:
                G.add_edge(source, target)

    #pos = nx.spring_layout(G)
    #pos = nx.bfs_layout(G, 1)
    #pos = nx.spectral_layout(G)
    #pos = nx.shell_layout(G)
    pos = nx.planar_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=10, arrowsize=20)
    plt.title("Directed Acyclic Graph")
    #plt.show()
    plt.savefig("dag.png")
    plt.close()

dag_definition = [
    "1>>2,3",
    "2,3>>4",
    "4,5>>6",
    "6>>7"
]

draw_dag(dag_definition)
