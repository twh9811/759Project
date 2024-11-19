
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
        
    def add_taskgroup(self, job_name, job_steps_in_wir_format):
        "jobs = taskgroup and tasks = steps"
        self.taskgroups[job_name] = job_steps_in_wir_format
        
    def display_wir(self):
        print(self.name)
        for job in self.taskgroups:
            print(job, self.taskgroups[job])
        

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
            
            job_env = {}
            job_dependency = {}
            job_tasks = {}
            
            if "needs" in job_contents:
                job_needed = job_contents['needs']
                # Scuffed logic but only way to get the proper reference index is to convert dict to list
                reference_index = list(workflow_intermediate_representation.taskgroups).index(job_needed)
                job_dependency["ref"] = reference_index
            
            
            # Gets the tasks that the job will execute
            steps = {}
            if "steps" in job_contents:
                steps = job_contents["steps"]
            
            # All comments to describe variable initialization are definitions taken straight from the paper (mostly) 
            # Represents the relative order in which the task is executed within the task group
            task_execution_id = 0
            for step in steps:
                # The name and other grouping attributes that identify a task.
                task_name = ""
                # All the information on “how” the task will be executed (e.g., through shell command or GitHub Actions).
                task_exec = {}
                # This had no paper definition but based on the examples it is the raw variables accessed by the task. 
                task_args = {}
                # Contains the set of environment variables accessed by the task.
                task_env = {}
                # The set of all GitHub variables accessed by the task. 
                # Differs from args because this defines the specific GitHub variable and its type (i.e. secrets) ?
                task_ci = {}

                
                # Gets the name of the task. Should always be one. Rest aren't guaranteed
                if "name" in step:
                    task_name = step["name"]
                
                # Gets the execution mechanism and what the task executed
                if "uses" in step:
                    task_exec["type"] = "docker_action"
                    task_exec["executed"] = step["uses"]
                elif "run" in step:
                    task_exec["type"] = "command"
                    task_exec["executed"] = step["uses"]
                
                # Gets the args used in the task.
                if "with" in step:
                    args = step["with"]
                    for arg in args:
                        task_args[arg] = args[arg]  

                # Gets the environment setup for the task
                if "env" in step:
                    env_vars = step["env"]
                    for env_var in env_vars:
                        task_env[env_var] = env_vars[env_var]
            
                
                # Creates an object for the task portion of the job
                task_in_wir_format  = {
                    "exec" : task_exec,
                    "execution_id" : task_execution_id,
                    "args" : task_args,
                    "environment" : task_env,
                    "CIvars" : []
                }
                # Store tasks in a group of overall tasks for the job
                job_tasks[task_name] = task_in_wir_format
                task_execution_id += 1 
            
            job = {
                "environment" : {},
                "dependency": job_dependency,
                "tasks" : job_tasks 
            }
            workflow_intermediate_representation.add_taskgroup(job_name, job)
            job_execution_id += 1
    return workflow_intermediate_representation
        

def main():
    github_action = "wir_test.yaml"
    wir = parse_workflow(github_action)
    wir.display_wir()
    
if __name__ == "__main__":
    main()
    
    
