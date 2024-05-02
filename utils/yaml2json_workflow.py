import yaml
import json
import sys

def generate_json_workflow(yaml_file):
    with open(yaml_file, 'r') as stream:
        data = yaml.safe_load(stream)

    flowname=data['name']
    date=data['createdAt']
    nodes = {int(node): name for node_dict in data['nodes'] for node, name in node_dict.items()}
    flow = data['flow']
    inputs = {key: value for item in data['inputs'] for key, value in item.items()}

    json_workflow = {
        "name": flowname,
        "createdAt": date,
        "workflow": []
    }

    for node_id, node_name in nodes.items():
        upstream = []
        downstream = []
        for link in flow:
            source_nodes = [int(s) for s in link.split(">>")[0].split(",")]
            target_nodes = [int(s) for s in link.split(">>")[1].split(",")]
            if node_id in source_nodes:
                downstream.extend(nodes[target_node] for target_node in target_nodes)
            if node_id in target_nodes:
                upstream.extend(nodes[source_node] for source_node in source_nodes)
        
        input_data = inputs.get(node_name, {})

        json_node = {
            "name": node_name,
            "type": node_name.lower(),
            "upstream": list(set(upstream)),
            "downstream": list(set(downstream)),
            "data": {
                "input": input_data,
                "output": {}
            },
            "status": "pending",
            "completedAt": None
        }
        json_workflow['workflow'].append(json_node)

    return json_workflow

def save_json_workflow(json_workflow, filename):
    with open(filename, 'w') as f:
        json.dump(json_workflow, f, indent=4)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python yaml2json_workflow.py input_yaml_file output_json_file")
        sys.exit(1)
    
    input_yaml_file = sys.argv[1]
    output_json_file = sys.argv[2]
    
    json_workflow = generate_json_workflow(input_yaml_file)
    save_json_workflow(json_workflow, output_json_file)
