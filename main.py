import wir_generator
import generate_action_summary

def main():
    main_workflow = "login_workflow.yaml"
    # Step 1: Generate Taint Summaries
    taint_summaries = generate_action_summary.Taint_Summaries()
    # Step 2: Create a WIR of the main workflow
    workflow_intermediate_representation = wir_generator.parse_workflow(main_workflow)
    # Step 3: Perform static analysis on the WIR, using taint summaries for actions
    
    
if __name__ == "__main__":
    main()