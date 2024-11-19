
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
        self.dependencies = {}
        
    def add_taskgroup(self, job_name, execution_id, steps, environment):
        self.taskgroups[job_name] = {
            "execution_id": execution_id,
            "tasks" : steps,
            "environment" : environment
        }

def main():
    github_action = "wir_test.yaml"
    
if __name__ == "__main__":
    main()