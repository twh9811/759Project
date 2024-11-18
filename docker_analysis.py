import yaml
from yaml.loader import SafeLoader


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
        self.process_parameters(docker_action, parameters)
        
    def process_parameters(self, docker_action, parameters):
        for parameter in parameters:
            # Variable most likely tainted?
            if parameter in DOCKER_ACTIONS[docker_action]["sources"]:
                self.taint_step(parameters[parameter])
    
def main():
    docker_file = "test_file.yaml"
    taint_analysis_obj = DockerActionTaintAnalysis(docker_file)
    taint_analysis_obj.process_jobs()
    print(taint_analysis_obj.taint_set)
    
if __name__ == "__main__":
    main()