from node import Node
from pubsub import pub
from datetime import datetime


class Workflow:
    def __init__(self, dto, verbose=True):
        """
        Initialize the Workflow object.

        Args:
            dto: A dictionary containing workflow data.
            verbose: A boolean indicating whether to print verbose output (default is True).

        Returns:
            None.
        """
        self.dto = dto
        self.nodes = self.create_nodes(dto['workflow'])
        self.verbose = verbose

    def create_nodes(self, workflow):
        """
        Create nodes for the workflow.

        Args:
            workflow: A list of dictionaries representing nodes in the workflow.

        Returns:
            A dictionary mapping node names to Node objects.
        """
        nodes = {}
        for node_data in workflow:
            node = Node(node_data, self)
            nodes[node.name] = node
        return nodes

    def process_workflow(self, input_nodes):
        """
        Process the workflow by sending messages to input nodes.

        Args:
            input_nodes: A list of input node names.

        Returns:
            None.
        """
        for node_name in input_nodes:
            pub.sendMessage(node_name, arg=None)

    def update_node_in_dto(self, node_name, status):
        """
        Update the status of a node in the workflow data.

        Args:
            node_name: The name of the node to update.
            status: The new status of the node.

        Returns:
            None.
        """
        for node in self.dto['workflow']:
            if node['name'] == node_name:
                if self.verbose:
                    print(
                        f"Updating status of node \033[1;38;5;208m{node_name}\033[0;0m to \033[1;38;5;77m{status}\033[0;0m")
                node['status'] = status
                node['completedAt'] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S")

    def init_workflow(self):
        """
        Initialize the workflow by marking input nodes as completed.

        Returns:
            A list of input node names.
        """
        # Mark input nodes as completed
        input_nodes = []
        for node in self.dto['workflow']:
            if node['upstream'] == []:
                node['status'] = 'completed'
                node['completedAt'] = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S")
                input_nodes.append(node['name'])
        return input_nodes
