from node_functions.testFlowFunctions import *
from node_functions.flowFunctions import *

from pubsub import pub

class Node:
    def __init__(self, node_data,workflow):
        self.name = node_data['name']
        self.type = node_data['type']
        self.upstream = node_data['upstream']
        self.downstream = node_data['downstream']
        self.data = node_data['data']
        self.status = node_data['status']
        self.completed_upstreams = set()
        self.workflow = workflow

        # Register listener for this node
        pub.subscribe(self.listener, self.name)

    def listener(self, arg):
        # Check if all upstream nodes are completed
        for upstream_node in self.upstream:
            if upstream_node not in self.completed_upstreams:
                if self.workflow.verbose:
                    print(
                        f"Node \033[1;38;5;208m{self.name}\033[0;0m waiting for \033[1;38;5;208m{upstream_node}\033[0;0m to proceed")
                return
            
        if self.workflow.verbose:
            print("\033[5;38;5;162m------------ NEW TASK ------------\033[0;0m")
            print(f"Node \033[1;38;5;208m{self.name}\033[0;0m processing task")

        # Update status
        function = globals()[self.type]
        input = self.data['input']
        output = function(input)
        self.status = 'completed'
        if self.workflow.verbose:
            print(
                f"Node \033[1;38;5;208m{self.name}\033[0;0m \033[1;38;5;77m{self.status}\033[0;0m task")
        self.workflow.update_node_in_dto(self.name, self.status)

        # hydrate node data with function output
        for node in self.workflow.dto['workflow']:
            if node['name'] == self.name:
                node['data']['output'] = output
                if self.workflow.verbose:
                    print(
                    f"   Hydrating \033[1;38;5;208m{self.name}\033[0;0m with output \033[1;38;5;158m{output}\033[0;0m")

        # Mark this node as completed upstream for downstream nodes
        for downstream_node in self.downstream:
            if downstream_node in self.workflow.nodes:
                self.workflow.nodes[downstream_node].mark_upstream_completed(self.name)

        for downstream_node in self.downstream:
            # hydrate downstream nodes data with function output
            for node in self.workflow.dto['workflow']:
                if node['name'] == downstream_node:
                    node['data']['input'][self.name] = self.data['output']
                    if self.workflow.verbose:
                        print(f"   Hydrating \033[1;38;5;208m{downstream_node}\033[0;0m with \033[1;38;5;208m{self.name}\033[0;0m data")            


        # Notify downstream nodes ###  wait until previous loop is done otherwise I may send the message before it is hydrated(?)
        for downstream_node in self.downstream:
            if self.workflow.verbose:
                print(
                f"   Node \033[1;38;5;208m{self.name}\033[0;0m sending message to \033[1;38;5;208m{downstream_node}\033[0;0m")
            pub.sendMessage(downstream_node, arg=self.data)

    def mark_upstream_completed(self, upstream_node):
        self.completed_upstreams.add(upstream_node)