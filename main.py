import wir_generator
import generate_action_summary
import taint_analysis
BASE_DIR = "example/"

def main():
    main_workflow = BASE_DIR + "sample-workflow.yaml"

    # Step 1: Generate Taint Summaries
    taint_summaries = generate_action_summary.Taint_Summaries().get_summaries()
    # Step 2: Create a WIR of the main workflow
    workflow_intermediate_representation = wir_generator.parse_workflow(main_workflow)
    # Step 3: Perform static analysis on the WIR, using taint summaries for actions
    taint_analysis_summary = taint_analysis.Docker_Action_Taint_Analysis(workflow_intermediate_representation, taint_summaries)
    
    tainted_vars, tainted_flow = taint_analysis_summary.get_tainted_variables()
    print("All Tainted Variables:")
    for var in tainted_vars:
        print(var)
    print()
    
    print("Tainted Flows:")
    num = 1
    for origin in tainted_flow:
        print("Flow " + str(num) + ":")
        flow = tainted_flow[origin]
        for affected_var in flow:
            print(" " + affected_var)
        num += 1
        print()
    
if __name__ == "__main__":
    main()