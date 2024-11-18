import yaml
from yaml.loader import SafeLoader
import json

# These will be used in the "Use" section to indicate which action is being used.
DOCKER_ACTIONS = {
    "docker/build-push-action@v6" : ["add-hosts", "allow","annotations","build-args","build-contexts","cache-from","cache-to","context","file","labels","network","platforms","pull","push","secrets","secret-envs","secret-files","ssh","tags","target","github-token"], 
    "docker/login-action@v2" : [], 
    "docker/setup-buildx-action@v2" : [], 
    "docker/metadata-action@v4" : [],  
    "docker/setup-qemu-action@v2" : [],  
    "docker/buildx-bake-action@v1" : [],  
    "docker/scout-action@v1" : []
    }


def analyze_workflow(docker_file):
    with open(docker_file) as docker_file:
        # Returns a dictionary representing the workflow. Every colon indicates a key, anyhting inside the colon is stored at that key value.
        # There can be dicts inside dicts inside dicts.
        yaml_workflow = yaml.load(docker_file, Loader=SafeLoader)
        workflow_jobs = yaml_workflow["jobs"]
        for job_name in workflow_jobs:
            job_steps = workflow_jobs[job_name]["steps"]
            for step in job_steps:
                the_docker_action = step['uses']
                if(the_docker_action in DOCKER_ACTIONS):
                    print("Use Summary Here ?")
                else:
                    step_with = step['with']
                    print(step_with)
                
                
        
    
def main():
    docker_file = "test_file.yaml"
    print(DOCKER_ACTIONS["docker/build-push-action@v6"])
    analyze_workflow(docker_file)
    
if __name__ == "__main__":
    main()