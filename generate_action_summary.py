import yaml
from yaml import SafeLoader
import os
import re

REFERENCE_PATTERN = "\\{\\{(.*?)}}"
DOCKER_VARIABLE_PATTERN = "\\{(.*?)}"
# Looks for any docker commands followed by a whitespace then captures the remaining args
DOCKER_PATTERN = "(CMD|ENV)\\s+(.*)"

class Taint_Summaries:
    
    def __init__(self):
        self.summaries = {}
        self.preload_summaries()
    
    def add_summary(self, name, taint_summary):
        self.summaries[name] = taint_summary
        
    def get_summaries(self):
        return self.summaries
    
    def display_summaries(self):
        print(self.summaries)
    
    def preload_summaries(self):
        base_dir = "actions/"
        files = os.listdir(base_dir)
        for file in files:
            action_file = base_dir + file
            # Takes off .yaml extension
            action_name = file[:-5]
            self.parse_action(action_name, action_file)
            
    def parse_action(self, name, action_file=None):
        taint_summary = {}
        if(action_file is None):
            pass
        else:
            action_workflow = get_yaml(action_file)
        

        
        # Input parameters allow you to specify data that the action expects to use during runtime. GitHub stores input parameters as environment variables.
        if "inputs" in action_workflow:
            workflow_inputs = action_workflow["inputs"]
            taint_summary["inputs"] = list(workflow_inputs.keys())
            
        # Output parameters allow you to declare data that an action sets. Actions that run later in a workflow can use the output data set in previously run actions.
        # Shows where tainted args propagate to
        if "outputs" in action_workflow:
            workflow_outputs = action_workflow["outputs"]
            taint_summary["outputs"] = list(workflow_outputs.keys())
            
        # Configures the image used for the Docker container action OR
        # This shows where the tainted vars propagate to.
        if "runs" in action_workflow:
            runs_obj = action_workflow["runs"]
            # Not a docker action.
            if "image" not in runs_obj:
                return
            docker_filename = runs_obj['image']
            taint_summary['docker_details'] = {}
            docker_summary = taint_summary['docker_details']
            docker_summary["container_image"] = docker_filename
                
            # Passes in args to docker container. Final sink before execution
            if "args" in runs_obj:
                action_args = runs_obj['args']
                
                action_sinks = []
                for arg in action_args:
                    arg_sinks = re.findall(REFERENCE_PATTERN, arg)
                    if len(arg_sinks) > 0:
                        for sink in arg_sinks:
                            action_sinks.append(sink.strip())
                taint_summary["sinks"] = action_sinks
        
            # Parses dockerfile to get the command it executes using the passed in variables
            # Only has support for python containers :(
            docker_base_dir = "docker/"
            docker_wir = parse_dockerfile(docker_base_dir + docker_filename)
            print(docker_wir)
                
        self.add_summary(name, taint_summary)

def parse_dockerfile(dockerfile_path):
    """
    Parsese a docker file and extracts any taint sources and sinks, stores them in WIR format

    Args:
        dockerfile_path (string): path to the dockerfile

    Returns:
        dictionary : Nested dictionary (WIR FORMAT) representing the dockerfile
    """
    docker_file_wir = {}
    with open(dockerfile_path) as docker_file:
        for line in docker_file:
            # Skip any comments
            if "#" not in line:
                # Look for any docker args.
                docker_vars = re.findall(DOCKER_PATTERN, line)
                if len(docker_vars) > 0:
                    # Restricted to one docker var per line, so only one match (allowing index 0 usage). Gets it out of list format
                    docker_vars = docker_vars[0]
                    # The docker command being used i.e. CMD, FROM, WORKDIR, COPY, etc.
                    docker_command = docker_vars[0]
                    # The args passed into the command
                    docker_args = docker_vars[1]
                    
                    
                    # THIS IS THE FINAL SINK. DOCKER FILE EXECUTES USING THESE ARGS
                    if docker_command == "CMD":
                        # Handles case if there are multiple args per command
                        arg_parts = docker_args.split("&&")
                        for arg_part in arg_parts:
                            arg_part = arg_part.strip()
                            if "sinks" in docker_file_wir:
                                docker_file_wir["sinks"].append(arg_part)
                            else:
                                docker_file_wir["sinks"] = [arg_part]
                    # Format of ENV "variable_name="assigned_value""
                    # THIS IS FOR TAINT SOURCES
                    elif docker_command == "ENV":
                        split_args = docker_args.split("=")
                        docker_variable_name = split_args[0]
                        # Extracts the referenced contents to see the input variable used.
                        # Should only be one result, hence 0 index usage
                        variable_contents = re.findall(DOCKER_VARIABLE_PATTERN, split_args[1])[0]
                        if "sources" in docker_file_wir:
                            docker_file_wir["sources"][variable_contents] = docker_variable_name
                        else:
                            docker_file_wir["sources"] = {}
                            docker_file_wir["sources"][variable_contents] = docker_variable_name
    return docker_file_wir

def get_yaml(action_file):
    with open(action_file) as action_file:
        action_workflow = yaml.load(action_file, Loader=SafeLoader)
    action_file.close()
    return action_workflow

def main():
    summary_database = Taint_Summaries()
    summary_database.display_summaries()
    
if __name__ == "__main__":
    main()
        
            
        
    
        