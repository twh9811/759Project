import wir_generator

# Taint summary support?
DOCKER_ACTIONS = ["docker/build-push-action@v6""docker/login-action@v2", "docker/setup-buildx-action@v2" , "docker/metadata-action@v4",  "docker/setup-qemu-action@v2",  "docker/buildx-bake-action@v1",  "docker/scout-action@v1"]

class DockerActionTaintAnalysis:
    def __init__(self, WIR):
        self.wir = WIR
        self.tainted_variables = set()
        # Make-shift database. More like a cache?
        self.taint_summaries = {}
            
    def is_tainted(self, step):
        return step in self.taint_set
    
    def taint_variable(self, variable):
        self.tainted_variables.add(variable)

    
def main():
    github_action = "wir_test.yaml"
    workflow_representation = wir_generator.parse_workflow(github_action)
    taint_analysis_obj = DockerActionTaintAnalysis(workflow_representation)
    taint_analysis_obj.wir.display_wir()
    
if __name__ == "__main__":
    main()