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
                print("\n  Analyzing Task:", task)
                
                # Find the initial taint sources from the main workflow.
                ci_vars = tasks[task]["CIvars"]
                args = tasks[task]["args"]
                print("   Finding Taint Sources Based on Task CIVars (GitHub Events)")
                for var in ci_vars:
                    arg_index = var['arg_ref']
                    tainted_variable = list(args.keys())[arg_index]
                    if var['type'] == "github":
                        print("    Variable \'" + tainted_variable + "\' has been tainted directly from user input (GitHub event)")
                        self.taint_variable(tainted_variable)
                
                task_obj = tasks[task]
                # Look at Docker Action Taints. Only they have the exec tag I believe
                if "executed" in task_obj['exec']:
                    if task_obj['exec'] != 'docker_action':
                        continue
                    # Gets rid of the version tag for the action
                    docker_action = task_obj['exec']['executed'].split("@")[0]
                    docker_action_str = "Docker Action: \'" + docker_action + "\'"
                    print("    Uses Docker Action:", docker_action_str)
                    
                    taint_summary = None
                    if docker_action in self.summaries:
                        taint_summary = self.summaries[docker_action]
                        print("      Taint Summary Found:", taint_summary)
                        for sink in taint_summary['sinks']:
                            print("        Tainted Variable \'" + sink + "\' has been tained by a tainted source propagating to the Docker Action")
                            self.taint_variable(sink)
