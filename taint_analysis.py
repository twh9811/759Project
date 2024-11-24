import wir_generator
import generate_action_summary

class Docker_Action_Taint_Analysis:
    def __init__(self, WIR, summaries):
        self.wir = WIR
        self.summaries = summaries
        self.tainted_variables = set()
        self.perform_analysis()
    def is_tainted(self, step):
        return step in self.taint_set
    
    def taint_variable(self, variable):
        self.tainted_variables.add(variable)


    def perform_analysis(self):
        print(self.summaries)
def main():
    # summaries = generate_action_summary.Taint_Summaries()
    
    # github_action = "wir_test.yaml"
    # workflow_representation = wir_generator.parse_workflow(github_action)
    # taint_analysis_obj = Docker_Action_Taint_Analysis(workflow_representation)
    # taint_analysis_obj.wir.display_wir()
    pass
if __name__ == "__main__":
    main()