import yaml
from yaml import SafeLoader

class Taint_Summaries:
    
    def __init__(self):
        self.summaries = self.preload_summaries()
    
    def preload_summaries(self):
        pass
        
    def parse_action(self, action_file):
        with open(action_file) as action_file:
            action_workflow = yaml.load(action_file, Loader=SafeLoader)
            if "name" in action_workflow:
                workflow_name = action_workflow["name"]
                
            if "inputs" in action_workflow:
                workflow_inputs = action_workflow["inputs"]
                
            if "outputs" in action_workflow:
                workflow_outputs = action_workflow["outputs"]
            
def main():
    test_str = "action.yaml"
    summary_database = Taint_Summaries()
    summary_database.parse_action(test_str)
    
if __name__ == "__main__":
    main()
        
            
        
    
        