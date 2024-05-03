from node import Node
from pubsub import pub
from datetime import datetime

class Workflow:
    def __init__(self,dto,verbose=True):
        self.dto = dto
        self.nodes = self.create_nodes(dto['workflow'])
        self.verbose = verbose

    def create_nodes(self,workflow):
        nodes = {}
        for node_data in workflow:
            node = Node(node_data,self)
            nodes[node.name] = node
        return nodes

    def process_workflow(self,input_nodes):
        for node_name in input_nodes:
            pub.sendMessage(node_name, arg=None)

    def update_node_in_dto(self,node_name, status):
        for node in self.dto['workflow']:
            if node['name'] == node_name:
                if self.verbose:
                    print(
                        f"Updating status of node \033[1;38;5;208m{node_name}\033[0;0m to \033[1;38;5;77m{status}\033[0;0m")
                node['status'] = status
                node['completedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def init_workflow(self):
        # Mark input nodes as completed
        input_nodes = []
        for node in self.dto['workflow']:
            if node['upstream'] == []:
                node['status'] = 'completed'
                node['completedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                input_nodes.append(node['name'])
        return input_nodes