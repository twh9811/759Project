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
        # Make-shift database. More like a cache?
        self.taint_summaries = {}
            
    def is_tainted(self, step):
        return step in self.taint_set
    
    def taint_variable(self, variable):
        self.tainted_variables.add(variable)

    
def main():
    docker_file = "test_file.yaml"
    taint_analysis_obj = DockerActionTaintAnalysis(docker_file)
    taint_analysis_obj.process_workflow()
    print(taint_analysis_obj.tainted_variables)
    
if __name__ == "__main__":
    main()