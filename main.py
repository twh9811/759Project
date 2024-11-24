import wir_generator
import generate_action_summary

def main():
    main_workflow = "login_workflow.yaml"
    taint_summaries = generate_action_summary()
    workflow_intermediate_representation = wir_generator.parse_workflow(main_workflow, taint_summaries)
    
if __name__ == "__main__":
    main()