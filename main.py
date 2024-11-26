import wir_generator
import generate_action_summary
import taint_analysis
BASE_DIR = "example/"
#BASE_DIR = "slack-notification-action/"

def main():
    main_workflow = BASE_DIR + "sample-workflow.yaml"
    #main_workflow = BASE_DIR + "slack-notification-workflow.yaml"
    # main_workflow = "20.yml"
    # Step 1: Generate Taint Summaries
    taint_summaries = generate_action_summary.Taint_Summaries().get_summaries()
    # Step 2: Create a WIR of the main workflow
    workflow_intermediate_representation = wir_generator.parse_workflow(main_workflow)
    # Step 3: Perform static analysis on the WIR, using taint summaries for actions
    taint_analysis_summary = taint_analysis.Docker_Action_Taint_Analysis(workflow_intermediate_representation, taint_summaries)
    
    tainted_vars = taint_analysis_summary.get_tainted_variables()
    print(tainted_vars)
    
if __name__ == "__main__":
    main()