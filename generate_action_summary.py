import yaml
from yaml import SafeLoader
import os
import re

REFERENCE_PATTERN = "\\{\\{(.*?)}}"

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
        #base_dir = "example/"
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
            taint_summary['container_image'] = runs_obj['image']
            
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
        self.add_summary(name, taint_summary)
        
def get_yaml(action_file):
    with open(action_file) as action_file:
        action_workflow = yaml.load(action_file, Loader=SafeLoader)
    action_file.close()
    return action_workflow

def main():
    summary_database = Taint_Summaries()
    summary_database.preload_summaries()
    summary_database.display_summaries()
    
if __name__ == "__main__":
    main()
        
            
        
    
        