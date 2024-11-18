import yaml
from yaml.loader import SafeLoader
import re

def analyze_workflow(docker_file):
    with open(docker_file) as docker_file:
        # Returns a dictionary representing the workflow. Every colon indicates a key, anyhting inside the colon is stored at that key value.
        # There can be dicts inside dicts inside dicts.
        yaml_workflow = yaml.load(docker_file, Loader=SafeLoader)
        workflow_jobs = yaml_workflow["jobs"]
        for job_name in workflow_jobs:
            job_steps = workflow_jobs[job_name]["steps"]
            print(job_name, job_steps)
        
    
def main():
    docker_file = "test_file.yaml"
    analyze_workflow(docker_file)
    
if __name__ == "__main__":
    main()