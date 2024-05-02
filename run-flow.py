from functions.testFlowFunctions import *
from functions.flowFunctions import *
from pubsub import pub
import time
from datetime import datetime
from pprint import pprint
import json
import sys
import importlib.util

class Node:
    def __init__(self, node_data):
        self.name = node_data['name']
        self.type = node_data['type']
        self.upstream = node_data['upstream']
        self.downstream = node_data['downstream']
        self.data = node_data['data']
        self.status = node_data['status']
        self.completed_upstreams = set()

        # Register listener for this node
        pub.subscribe(self.listener, self.name)

    def listener(self, arg):
        # Check if all upstream nodes are completed
        for upstream_node in self.upstream:
            if upstream_node not in self.completed_upstreams:
                print(f"Node \033[1;38;5;208m{self.name}\033[0;0m waiting for \033[1;38;5;208m{upstream_node}\033[0;0m to proceed")
                return
        print("\033[5;38;5;162m------------ NEW TASK ------------\033[0;0m")
        # Process task
        print(f"Node \033[1;38;5;208m{self.name}\033[0;0m processing task")# with data: {self.data}")

        # Update status
        function = globals()[self.type]
        input = self.data['input']
        output= function(input)
        self.status = 'completed'
        print(f"Node \033[1;38;5;208m{self.name}\033[0;0m \033[1;38;5;77m{self.status}\033[0;0m task")
        update_node_in_dto(self.name, self.status)
        
        # hydrate node data with function output
        for node in dto['workflow']:
            if node['name'] == self.name:
                node['data']['output'] = output
                print(f"   Hydrating \033[1;38;5;208m{self.name}\033[0;0m with output \033[1;38;5;158m{output}\033[0;0m")

        # Mark this node as completed upstream for downstream nodes
        for downstream_node in self.downstream:
            if downstream_node in nodes:
                nodes[downstream_node].mark_upstream_completed(self.name)

        
        for downstream_node in self.downstream:
            # hydrate downstream nodes data with function output
            for node in dto['workflow']:
                if node['name'] == downstream_node:
                    node['data']['input'][self.name] = self.data['output']
                    print(f"   Hydrating \033[1;38;5;208m{downstream_node}\033[0;0m with \033[1;38;5;208m{self.name}\033[0;0m data")
        
        # Notify downstream nodes ###  wait until previous loop is done otherwise I may send the message before it is hydrated(?)
        for downstream_node in self.downstream:
            print(f"   Node \033[1;38;5;208m{self.name}\033[0;0m sending message to \033[1;38;5;208m{downstream_node}\033[0;0m")
            pub.sendMessage(downstream_node, arg=self.data)

    def mark_upstream_completed(self, upstream_node):
        self.completed_upstreams.add(upstream_node)

def create_nodes(workflow):
    nodes = {}
    for node_data in workflow:
        node = Node(node_data)
        nodes[node.name] = node
    return nodes

def process_workflow(input_nodes):
    for node_name in input_nodes:
        pub.sendMessage(node_name,arg=None)

def update_node_in_dto(node_name, status):
    for node in dto['workflow']:
        if node['name'] == node_name:
            print(f"Updating status of node \033[1;38;5;208m{node_name}\033[0;0m to \033[1;38;5;77m{status}\033[0;0m")
            node['status'] = status
            node['completedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def init_workflow():
    # Mark input nodes as completed
    input_nodes = []
    for node in dto['workflow']:
        if node['upstream'] == []:
            node['status'] = 'completed'
            node['completedAt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
            input_nodes.append(node['name'])
    return input_nodes


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit("You need 1 argument: python run-flow.py <path-to-dto>")
    dto_path = sys.argv[1]
    with open(dto_path) as f:
        dto = json.load(f)
    # initialize the workflow
    input_nodes = init_workflow()
    # Create nodes
    nodes = create_nodes(dto['workflow'])
    # Start the workflow
    process_workflow(input_nodes)

    print()
    print("\033[5;38;5;162m------------ FINAL DTO ------------\033[0;0m")
    pprint(dto,width=300,depth=4) 
