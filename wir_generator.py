
#WIR Task Attributes
# Identity - Name of Step
# Execution Mechanism - indicated with "run"
# Execution Environment - indicated with 'env'
# CI Variables - indicated "with"
# Task Dependencies - indicated with needs
# Execution Ordering - order steps executed in

import yaml
from yaml.loader import SafeLoader
import re

# Extracts any text between {{ }}
# Python magic strikes again. Need to escape the escape character to make it see the brackets as a string
REFERENCE_PATTERN = "\\{\\{(.*?)}}"

class WIR:
    def __init__(self, workflow_name):
        self.name = workflow_name
        self.taskgroups = {}
        self.dependencies = []
        
    def add_taskgroup(self, job_name, execution_id, steps, environment):
        self.taskgroups[job_name] = {
            "execution_id": execution_id,
            "tasks" : steps,
            "environment" : environment
        }
        
    def __str__(self):
        return self.name + "\n\t" + str(self.taskgroups) + "\n\t" + str(self.dependencies)
        

def parse_workflow(workflow_path):
    with open(workflow_path) as str_workflow:
        
        yaml_workflow = yaml.load(str_workflow, Loader=SafeLoader)

        if "name" in yaml_workflow:
            workflow_name = yaml_workflow["name"]
            
        workflow_intermediate_representation = WIR(workflow_name)
        print(workflow_intermediate_representation)

        

def main():
    github_action = "wir_test.yaml"
    parse_workflow(github_action)
    
if __name__ == "__main__":
    main()