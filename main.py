from workflow import Workflow
from dotenv import load_dotenv
from yaml2json_workflow import generate_json_workflow
from pprint import pprint
import json
import sys
from datetime import datetime

load_dotenv() 

# write the script below if __main__ block as a function
def run_workflow(dto_path, verbose=True):
    if dto_path.endswith('.yaml'):
        dto=generate_json_workflow(dto_path, verbose=verbose)
    else:
        with open(dto_path) as f:
            dto = json.load(f)

    workflow = Workflow(dto,verbose=verbose)

    # initialize the workflow
    input_nodes = workflow.init_workflow()
    # Start the workflow
    workflow.process_workflow(input_nodes)

    # if verbose:
    #     print()
    #     print("\033[5;38;5;162m------------ FINAL DTO ------------\033[0;0m")
    #     pprint(workflow.dto, width=300, depth=4)

    return workflow.dto


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        exit("You need at least 1 argument: python run-flow.py <path-to-dto> <verbose>")

    dto_path=sys.argv[1]
    if len(sys.argv) > 2:
        verbose = sys.argv[2]
    dto=run_workflow(dto_path,verbose=verbose)

    #print(json.dumps(dto, indent=4))
    print("\033[5;38;5;162m------------ FINAL DTO ------------\033[0;0m")
    pprint(dto, width=300, depth=4)
    