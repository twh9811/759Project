import yaml
from yaml import SafeLoader
import os

class Taint_Summaries:
    
    def __init__(self):
        self.summaries = {}
        
    def get_yaml(self, action_file):
        with open(action_file) as action_file:
            action_workflow = yaml.load(action_file, Loader=SafeLoader)
        action_file.close()
        return action_workflow
    
    def add_summary(self, name, taint_summary):
        self.summaries[name] = taint_summary
    
    def display_summaries(self):
        print(self.summaries)
    
    def parse_action(self, action_file):
        action_workflow = self.get_yaml(action_file)
        
        taint_summary = {}
        if "name" in action_workflow:
            workflow_name = action_workflow["name"]
        
        # Potential Taint Sources
        if "inputs" in action_workflow:
            workflow_inputs = action_workflow["inputs"]
            taint_summary["inputs"] = list(workflow_inputs.keys())
            
        # Potential Taint Sinks
        if "outputs" in action_workflow:
            workflow_outputs = action_workflow["outputs"]
            taint_summary["outputs"] = list(workflow_outputs.keys())
        
        self.add_summary(workflow_name, taint_summary)
    
def main():
    summary_database = Taint_Summaries()
    base_dir = "offline_actions_for_summary/"
    files = os.listdir(base_dir)
    for file in files:
        action_file = base_dir + file
        summary_database.parse_action(action_file)
        
    summary_database.display_summaries()
    
if __name__ == "__main__":
    main()
        
            
        
    
        