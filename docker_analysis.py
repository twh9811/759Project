import yaml
from yaml.loader import SafeLoader
import re

# These will be used in the "use" section to indicate which action is being used.
DOCKER_ACTIONS = ["docker/build-push-action@v6""docker/login-action@v2", "docker/setup-buildx-action@v2" , "docker/metadata-action@v4",  "docker/setup-qemu-action@v2",  "docker/buildx-bake-action@v1",  "docker/scout-action@v1"]
SOURCES = ['env']
SINKS = ['jobs', 'run']
# Extracts any text between {{ }}
# Python magic strikes again. Need to escape the escape character to make it see the brackets as a string
REFERENCE_PATTERN = "\\{\\{(.*?)}}"


test = {}
class DockerActionTaintAnalysis:
    def __init__(self, docker_file):
        self.tainted_variables = set()
        self.yaml_file = None
        with open(docker_file) as docker_file:
            # Returns a dictionary representing the workflow. Every colon indicates a key, anyhting inside the colon is stored at that key value.
            # There can be dicts inside dicts inside dicts.
            self.yaml_file = yaml.load(docker_file, Loader=SafeLoader)
    
    def is_tainted(self, step):
        return step in self.taint_set
    
    def taint_variable(self, variable):
        self.tainted_variables.add(variable)
    
    
    def process_workflow(self):
        for item in self.yaml_file:
            next_workflow = self.yaml_file[item]
            if item == "env":
                self.process_env(next_workflow)
            elif item == "jobs":
                self.process_jobs(next_workflow)
                
    def process_env(self, env_workflow):
        for env_variable in env_workflow:
            variable_contents = env_workflow[env_variable]
            if(self.found_taints(variable_contents)):
                self.taint_variable(env_variable)
            
    def process_jobs(self, job_workflow):
        for job_name in job_workflow:
            print(job_name)
            #print(job_workflow[job_name]["steps"])
            
                
            
def main():
    docker_file = "test_file.yaml"
    taint_analysis_obj = DockerActionTaintAnalysis(docker_file)
    taint_analysis_obj.process_workflow()
    #print(taint_analysis_obj.tainted_variables)
    # taint_analysis_obj.process_jobs()
    # print(taint_analysis_obj.tainted_variables)
    
if __name__ == "__main__":
    main()