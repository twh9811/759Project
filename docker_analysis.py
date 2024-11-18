import yaml
from yaml.loader import SafeLoader
import re

# These will be used in the "use" section to indicate which action is being used.
DOCKER_ACTIONS = ["docker/build-push-action@v6""docker/login-action@v2", "docker/setup-buildx-action@v2" , "docker/metadata-action@v4",  "docker/setup-qemu-action@v2",  "docker/buildx-bake-action@v1",  "docker/scout-action@v1"]

# Extracts any text between {{ }}
# Python magic strikes again. Need to escape the escape character to make it see the brackets as a string
REFERENCE_PATTERN = '\\{\\{(.*)\\}\\}'


test = {}
class DockerActionTaintAnalysis:
    def __init__(self, docker_file):
        self.tainted_placeholders = set()
        self.tainted_variables = set()
        self.yaml_file = None
        with open(docker_file) as docker_file:
            # Returns a dictionary representing the workflow. Every colon indicates a key, anyhting inside the colon is stored at that key value.
            # There can be dicts inside dicts inside dicts.
            self.yaml_file = yaml.load(docker_file, Loader=SafeLoader)
            
    def is_tainted(self, step):
        return step in self.taint_set
    
    def taint_step(self, step):
        self.taint_set.add(step)
    
    def process_jobs(self):
        workflow_jobs = self.yaml_file["jobs"]
        for job_name in workflow_jobs:
            job_steps = workflow_jobs[job_name]["steps"]
            self.process_bulk_steps(job_steps)
                    
    def process_bulk_steps(self, job_steps):
        # This will have ALL the steps of the job as dictionaries
        for bulk_steps in job_steps:
            self.process_individual_steps(bulk_steps)
            
    def process_individual_steps(self, bulk_steps):
        step_name = bulk_steps["name"]
        docker_action = bulk_steps["uses"]
        parameters = bulk_steps["with"]
        self.process_parameters(parameters)
        
    def process_parameters(self, parameters):
        for parameter in parameters:
            parameter_instructions = parameters[parameter]
            self.process_parameter_instructions(parameter_instructions)
                
    def process_parameter_instructions(self, parameter_instructions):
        # Sometimes the data is stored in a variable, sometimes it is just referenced.
        # This handles both scenarios.
        
        taints = re.findall(parameter_instructions, REFERENCE_PATTERN)
        print(taints)
        # # Taint the variable
        # if "=" in parameter_instructions:
        
        # print(parameter_instructions)
def main():
    docker_file = "test_file.yaml"
    taint_analysis_obj = DockerActionTaintAnalysis(docker_file)
    taint_analysis_obj.process_jobs()
    
if __name__ == "__main__":
    main()