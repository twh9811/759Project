import wir_generator
import generate_action_summary

class Docker_Action_Taint_Analysis:
    def __init__(self, WIR, summaries):
        self.wir = WIR
        self.summaries = summaries
        self.tainted_variables = set()
        self.taint_variable("username")
        self.taint_variable("password")
        self.perform_analysis()
        
    def is_tainted(self, var):
        return var in self.tainted_variables
    
    def taint_variable(self, variable):
        self.tainted_variables.add(variable)


    def perform_analysis(self):
        print("Analyzing Workflow:", self.wir.get_name())
        jobs = self.wir.get_taskgroups()
        print(jobs)
        for job in jobs:
            print(" Analyzing Job:", job)
            job_obj = jobs[job]
            tasks = job_obj["tasks"]
            for task in tasks:
                print("   Analyzing Task:", task)
                task_obj = tasks[task]
                # Gets rid of the version tag for the action
                docker_action = task_obj['exec']['executed'].split("@")[0]
                
                taint_summary = None
                if docker_action in self.summaries:
                    taint_summary = self.summaries[docker_action]
                
                for inputs in taint_summary["inputs"]:
                    print("      Analyzing Task Variable:", inputs)
                    # Checks to see if input could be tainted
                    if self.is_tainted(inputs):
                        print("        Variable: ", inputs, "is tainted")
                        # If its marked as tainted, the outputs will be affected as well
                        for outputs in taint_summary["outputs"]:
                            print("          Variable: ", outputs, "is tainted because it used a value touched by", inputs)
                            self.taint_variable(outputs)
                            

def main():
    # summaries = generate_action_summary.Taint_Summaries()
    
    # github_action = "wir_test.yaml"
    # workflow_representation = wir_generator.parse_workflow(github_action)
    # taint_analysis_obj = Docker_Action_Taint_Analysis(workflow_representation)
    # taint_analysis_obj.wir.display_wir()
    pass
if __name__ == "__main__":
    main()