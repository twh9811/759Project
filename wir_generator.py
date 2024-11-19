
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

def Generate_WIR(github_action_workflow):
    wir = {}
    with open(github_action_workflow) as workflow:
        # Returns a dictionary representing the workflow. Every colon indicates a key, anyhting inside the colon is stored at that key value.
        # There can be dicts inside dicts inside dicts.
        yaml_workflow = yaml.load(workflow, Loader=SafeLoader)
        # try:
        # I dont know the right word for this but its the outermost tags in the action file that define core aspects of the action file
        # I.e. the workflow name, the event that triggers it, its jobs etc.
        for action_outline in yaml_workflow:
            contents = yaml_workflow[action_outline]
            if type(action_outline) is bool:
                wir["triggers"] = contents
            else:
                if action_outline == "jobs":
                    wir_attributed_job = process_job(contents)
                else:
                    wir[action_outline] = yaml_workflow[action_outline]
        print(wir)
        # except TypeError:
        #     print("Error Parsing Workflow. No jobs")
                
            
def process_job(yaml_of_workflow):
    # Declare WIR that will be added into main WIR
    key_for_jobs = "jobs"
    job_wir = {}
    
    for job in yaml_of_workflow:
        # Create a new entry in the WIR for each jobs contents
        job_wir[key_for_jobs] = job
        job_wir[key_for_jobs][job] = {}
        
        job_steps = yaml_of_workflow[job]
        for step in job_steps:
            print(step)
    print(job_wir)
def main():
    github_action = "wir_test.yaml"
    wir_representation = Generate_WIR(github_action)
    
if __name__ == "__main__":
    main()