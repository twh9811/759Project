import yaml
from yaml import SafeLoader
import os

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
        base_dir = "offline_actions_for_summary/"
        files = os.listdir(base_dir)
        for file in files:
            action_file = base_dir + file
            # Takes off .yaml extension
            action_name = file[:-5]
            self.parse_action(action_name, action_file)
            
    def parse_action(self, name, action_file):
        action_workflow = get_yaml(action_file)
        
        taint_summary = {}
        
        # Potential Taint Sources
        if "inputs" in action_workflow:
            workflow_inputs = action_workflow["inputs"]
            taint_summary["inputs"] = list(workflow_inputs.keys())
            
        # Potential Taint Sinks
        if "outputs" in action_workflow:
            workflow_outputs = action_workflow["outputs"]
            taint_summary["outputs"] = list(workflow_outputs.keys())
        
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
        
            
        
    
        