
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
        "jobs = taskgroup and tasks = steps"
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
        
        # Gets the jobs that will be executed in the workflow
        jobs = {}
        if "jobs" in yaml_workflow:
            jobs = yaml_workflow["jobs"]
            
        job_execution_id = 0
        for job_name in jobs:
            job_contents = jobs[job_name]
            
            # Gets the tasks that the job will execute
            steps = {}
            if "steps" in job_contents:
                steps = job_contents["steps"]
            
            task_execution_id = 0
            for step in steps:
                # Declare the variables here.
                task_name = ""
                execution_done = ""
                execution_mechanism = ""
                task_args = {}
                
                # Gets the name of the task
                if "name" in step:
                    task_name = step["name"]
                
                # Gets the execution mechanism of the task 
                if "uses" in step:
                    execution_done = step["uses"]
                    execution_mechanism = "docker_action"
                elif "run" in step:
                    execution_done = step["run"]
                    execution_mechanism = "command"
                
                # Gets the args used in the task.
                if "with" in step:
                    args = step["with"]
                    for arg in args:
                        task_args[arg] = args[arg]  

                # Creates an object for the task
                task  = {
                    "name" : task_name,
                    "execution_mechanism" : execution_mechanism,
                    "execution_performed" : execution_done,
                    "execution_id" : task_execution_id,
                    "args" : task_args,
                    "environment" : [],
                    "CIvars" : []
                }
                print(task)
                task_execution_id += 1
            job_execution_id += 1
          
        

def main():
    github_action = "wir_test.yaml"
    parse_workflow(github_action)
    
if __name__ == "__main__":
    main()