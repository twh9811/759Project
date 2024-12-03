import wir_generator
import generate_action_summary
import taint_analysis
BASE_DIR = "src/example/"

def write_to_file(filepath, tainted_vars, tainted_flow):
    """
    Writes the summary to a file. Rewrites the file.

    Args:
        filepath (string): Path to the file
        tainted_vars (list): list of tainted variables
        tainted_flow (ldictionary): dict containing the taint flows 
    """
    with open(filepath, "w") as file:
        file.write("All Tainted Variables:\n\n")
        for var in tainted_vars:
            file.write(var + "\n")

        file.write("\nTainted Flows:\n")
        num = 0
        for origin in tainted_flow:
            file.write("\tFlow " + str(num) + ":\n")
            flow = tainted_flow[origin]
            file.write("\t\tOrigin: " + origin + "\n")
            for affected_var in flow:
                file.write("\t\t\tPropagation: " + affected_var + "\n")
            num += 1
    
def main():
    main_workflow = BASE_DIR + "sample-workflow.yaml"

    # Step 1: Generate Taint Summaries
    taint_summaries = generate_action_summary.Taint_Summaries().get_summaries()
    # Step 2: Create a WIR of the main workflow
    workflow_intermediate_representation = wir_generator.parse_workflow(main_workflow)
    # Step 3: Perform static analysis on the WIR, using taint summaries for actions
    taint_analysis_summary = taint_analysis.Docker_Action_Taint_Analysis(workflow_intermediate_representation, taint_summaries)
    
    # Gets the flow summary and tainted variable summary from the taint analysis
    tainted_vars, tainted_flow = taint_analysis_summary.get_tainted_variables()
    
    filename = "results/summary.txt"
    write_to_file(filename, tainted_vars, tainted_flow)
    
    print("All Tainted Variables:")
    for var in tainted_vars:
        print(var)
    print()
    
    print("Tainted Flows:")
    num = 1
    for origin in tainted_flow:
        print("Flow " + str(num) + ":")
        flow = tainted_flow[origin]
        print(" Origin: " + origin)
        for affected_var in flow:
            print("     Propagation: " + affected_var)
        num += 1
        print()
    
if __name__ == "__main__":
    main()