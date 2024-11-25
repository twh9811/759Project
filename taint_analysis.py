import wir_generator
import generate_action_summary

class Docker_Action_Taint_Analysis:
    def __init__(self, WIR, summaries):
        self.wir = WIR
        self.summaries = summaries
        self.tainted_variables = set()
        self.perform_analysis()
        
    def is_tainted(self, variable):
        return variable in self.tainted_variables
    
    def taint_variable(self, variable):
        self.tainted_variables.add(variable)

    def get_tainted_variables(self):
        return self.tainted_variables

    def perform_analysis(self):
        print("Analyzing Workflow:", self.wir.get_name())
        jobs = self.wir.get_taskgroups()
        for job in jobs:
            print(" Analyzing Job:", job)
            job_obj = jobs[job]
            tasks = job_obj["tasks"]
            for task in tasks:
                
                
                # These indicate the initial taint sources from the workflow.
                ci_vars = tasks[task]["CIvars"]
                args = tasks[task]["args"]
                for var in ci_vars:
                    print("  Analyzing For Initial Taints Based On CIVars")
                    if var['type'] == "github" or var['type'] == "secrets":
                        arg_index = var['arg_ref']
                        tainted_variable = list(args.keys())[arg_index]
                        print("    Variable \'" + tainted_variable + "\' has been tainted directly from user input")
                        self.taint_variable(tainted_variable)
                        
                
                print("  Analyzing Task:", task)
                task_obj = tasks[task]
                # Gets rid of the version tag for the action
                docker_action = task_obj['exec']['executed'].split("@")[0]
                print("    Uses Docker Action \'" + docker_action + "\'")
                
                taint_summary = None
                if docker_action in self.summaries:
                    taint_summary = self.summaries[docker_action]
                    print("      Taint Summary Found")
                    print(taint_summary)
                    # for taint in taint_summary:
                    #     if taint in self.get_tainted_variables():
                    #         print("      Action is using tainted variable")
                    
                    
                    

                
                # for inputs in taint_summary["inputs"]:
                #     print("      Analyzing Task Variable:", inputs)
                #     # Checks to see if input could be tainted
                #     if self.is_tainted(inputs):
                #         print("        Variable: ", inputs, "is tainted")
                #         # If its marked as tainted, the outputs will be affected as well
                #         for outputs in taint_summary["outputs"]:
                #             print("          Variable: ", outputs, "is tainted because it used a value touched by", inputs)
                #             self.taint_variable(outputs)
                            

def main():
    # summaries = generate_action_summary.Taint_Summaries()
    
    # github_action = "wir_test.yaml"
    # workflow_representation = wir_generator.parse_workflow(github_action)
    # taint_analysis_obj = Docker_Action_Taint_Analysis(workflow_representation)
    # taint_analysis_obj.wir.display_wir()
    pass
if __name__ == "__main__":
    main()