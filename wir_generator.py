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

# Looks for any DOCKER VARS followed by a whitespace then captures the remaining input
DOCKER_PATTERN = "(CMD|RUN|ARG)\\s+(.*)"
GITHUB_CI_VARS = ["secrets.", "github.", "docker.","env.","inputs.","jobs.","steps."]

class WIR:
    def __init__(self, workflow_name):
        self.name = workflow_name
        self.taskgroups = {}
        
    def add_taskgroup(self, job_name, job_in_wir_format):
        """
        Stores a job that has been converted into wir format in the main WIR object.
        Uses the job name as the key.
        
        Confusing function name but taskgroups are the same as jobs (as jobs are just a group of tasks).
        The same goes for steps and tasks, they are the same. Steps are the tasks that a job executes.

        Args:
            job_name (string): Name of the job to be used as the storage key
            job_steps_in_wir_format (dictionary): Workflow in WIR format. Basically a bunch of nested dictionaries
        """
        self.taskgroups[job_name] = job_in_wir_format
        
    def get_taskgroups(self):
        return self.taskgroups
    
    def get_name(self):
        return self.name
    
    def display_wir(self):
        """
        Displays the WIR in a nicely formatted string. Not __str__ because that would be more annoying to format
        """
        print("Workflow:", self.name)
        for job in self.taskgroups:
            job_contents = self.taskgroups[job]
            print(" Taskgroup:", job)
            print("  Execution ID", job_contents["execution_id"])
            print("  Environment", job_contents["environment"])
            print("  dependency", job_contents["dependency"])
            print("  Tasks:")
            for task in job_contents["tasks"]:
                task_contents = job_contents["tasks"][task]
                print("   Task:", task)
                for step in task_contents:
                    step_contents = task_contents[step]
                    print("    ", step + ":", step_contents)
                    
def get_yaml(action_file):
    """
    Returns YAML file as a YAML object in python

    Args:
        action_file (file): File loaded in Python "File" object

    Returns:
        Yaml_File: The action file in a YAML object in python
    """
    with open(action_file) as action_file:
        action_workflow = yaml.load(action_file, Loader=SafeLoader)
    action_file.close()
    return action_workflow

def parse_dockerfile(dockerfile_path):
    with open(dockerfile_path) as docker_file:
        for line in docker_file:
            if "#" not in line:
                docker_vars = re.findall(DOCKER_PATTERN, line)
                if len(docker_vars) > 0:
                    print(docker_vars)

def parse_workflow(workflow_path):
    """
    Parses the workflow YAML file. Split into two main sections:
    Parsing the jobs and parsing the tasks inside the jobs.
    It builds a workflow intermediate representation according to the criteria established in the paper, see comment at top.

    Args:
        workflow_path (str): filepath of the workflow to build the WIR for

    Returns:
        WIR Object: A workflow intermediate representation of the entire workflow
    """
    
    yaml_workflow = get_yaml(workflow_path)

    if "name" in yaml_workflow:
        workflow_name = yaml_workflow["name"]

    workflow_intermediate_representation = WIR(workflow_name)
    
    # =====================================================
    # The following focuses on the jobs inside the workflow
    # =====================================================
    
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
        
        if "env" in job_contents:
            env_variables = job_contents["env"]
            for env_variable in env_variables:
                env_contents = env_variables[env_variable]
                job_env[env_variable] = env_contents
                
        # ==================================================
        # The following  focuses on the tasks inside the job
        # ==================================================
        
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
            task_ci = []

            
            # Gets the name of the task. Should always be one. Rest aren't guaranteed
            if "name" in step:
                task_name = step["name"]
            
            # Gets the execution mechanism and what the task executed
            if "uses" in step:
                if "run" in step:
                    task_exec["type"] = "command"
                    task_exec["executed"] = step["run"]
                else:
                    task_exec["type"] = "docker_action"
                    # Removes author from the tag
                    task_exec["executed"] = step["uses"].split("/")[1]
            
            
            # Gets the args used in the task.
            if "with" in step:
                args = step["with"]
                arg_ref = 0
                for arg in args:
                    arg_contents = args[arg]
                    task_args[arg] = arg_contents
                    for ci_indicator in GITHUB_CI_VARS:
                        # contents are booleans sometimes which breaks this, luckily none of them are CI vars.
                        if type(arg_contents) is not bool and ci_indicator in arg_contents:
                            no_bracket_args = re.findall(REFERENCE_PATTERN, arg_contents)
                            if(len(no_bracket_args) > 0):
                                no_brack_args_cleaned = no_bracket_args[0].strip()
                                split_arg = no_brack_args_cleaned.split(".", 1)
                                var_type = split_arg[0]
                                name = split_arg[1]
                                ci_var_in_wir_format = {
                                    "type": var_type,
                                    "name": name,
                                    "arg_ref": arg_ref
                                }
                                task_ci.append(ci_var_in_wir_format)
                    arg_ref += 1
                        
            # Gets the environment setup for the task
            if "env" in step:
                env_vars = step["env"]
                for env_var in env_vars:
                    task_env[env_var] = env_vars[env_var]
        
            
            # Creates an WIR representation for the task portion of the job
            task_in_wir_format  = {
                "exec" : task_exec,
                "execution_id" : task_execution_id,
                "args" : task_args,
                "environment" : task_env,
                "CIvars" : task_ci
            }
            
            # Store tasks in a group of overall tasks for the job
            job_tasks[task_name] = task_in_wir_format
            task_execution_id += 1 
        
        # Creates an WIR representation for the job.
        job = {
            "execution_id": job_execution_id,
            "environment" : job_env,
            "dependency": job_dependency,
            "tasks" : job_tasks 
        }
        
        # Job is added to the main WIR object.
        workflow_intermediate_representation.add_taskgroup(job_name, job)
        job_execution_id += 1
        
    # WIR should be built when all workflow is parsed
    return workflow_intermediate_representation
    
    
def main():
    # github_action = "example/sample-workflow.yaml"
    # #github_action = "slack-notification-action/slack-notification-workflow.yaml"
    # wir = parse_workflow(github_action)
    # wir.display_wir()
    test = "docker/Dockerfile"
    parse_dockerfile(test)
    
if __name__ == "__main__":
    main()
    
    
