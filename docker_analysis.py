import yaml
from yaml.loader import SafeLoader
import json

# These will be used in the "use" section to indicate which action is being used.
DOCKER_ACTIONS = {
    # Map docker actions to their taint sources
    "docker/build-push-action@v6" : {
        "sources" : ["add-hosts", "allow","annotations","build-args","build-contexts","cache-from","cache-to","context","file","labels","network","platforms","pull","push","secrets","secret-envs","secret-files","ssh","tags","target","github-token"],
        "sinks": [""]
        },
    "docker/login-action@v2" : [], 
    "docker/setup-buildx-action@v2" : [], 
    "docker/metadata-action@v4" : [],  
    "docker/setup-qemu-action@v2" : [],  
    "docker/buildx-bake-action@v1" : [],  
    "docker/scout-action@v1" : []
    }

class DockerActionTaintAnalysis:
    def __init__(self, docker_file):
        self.taint_set = set()
        self.yaml_file = None
        with open(docker_file) as docker_file:
            # Returns a dictionary representing the workflow. Every colon indicates a key, anyhting inside the colon is stored at that key value.
            # There can be dicts inside dicts inside dicts.
            self.yaml_file = yaml.load(docker_file, Loader=SafeLoader)
            
    def is_tainted(self, variable):
        return variable in self.taint_set
    
    def process_jobs(self, docker_file):
        with open(docker_file) as docker_file:
            yaml_workflow = self.yaml_file
            workflow_jobs = yaml_workflow["jobs"]
            for job_name in workflow_jobs:
                job_steps = workflow_jobs[job_name]["steps"]
                self.process_jobs(job_steps)
                    
    def process_st(self, job_steps):
        for step_name in job_steps:
            step = job_steps[step_name]
            self.process_steps(step)
    
    def process_steps(self, steps):
        pass
        # print(steps)
        # for step_name in steps:
            
        #     # Gets the docker action being executed in the specific step
        #     the_docker_action = step['uses']
        #     # Gets the parameters passed into the specific step
        #     action_parameters = step['with']
        #     self.process_parameters(the_docker_action, action_parameters)
    
    def process_parameters(self, docker_action, parameters):
        print(docker_action, parameters)
    
def main():
    docker_file = "test_file.yaml"
    taint_analysis_obj = DockerActionTaintAnalysis()
    taint_analysis_obj.process_jobs(docker_file)
    
if __name__ == "__main__":
    main()