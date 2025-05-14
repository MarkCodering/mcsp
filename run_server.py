from mcsp import ModelContextStore

def start_mcp_server():
    mcs = ModelContextStore(
        name="example_model_context_store",
        description="An example model context store",
        version="1.0.0",
        author="Your Name",
        author_email="your.email@example.com",
    )
    
    mcs.create_space("example_space", "An example space")
    mcs.create_context("example_space", "example_context", {"key": "value"})
    print(mcs.get_context("example_space", "example_context"))
    print(mcs.list_spaces())
    print(mcs.list_contexts("example_space"))
    
if __name__ == "__main__":
    start_mcp_server()