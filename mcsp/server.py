# mcsp/server.py
from mcp.server.fastmcp import FastMCP
from mcsp.core import ModelContextStoreProtocol

def start_mcp_server():
    mcs = ModelContextStoreProtocol(
        name="example_model_context_store",
        description="An example model context store",
        version="1.0.0",
        author="Your Name",
        author_email="your_email@example.com",
        isTracking=True,
    )

    mcp = FastMCP(mcs.name)

    @mcp.tool()
    def create_space(space: str):
        mcs.create_space(space)
        return "Space created"

    @mcp.tool()
    def create_context(space: str, name: str, context: Any):
        mcs.create_context(space, name, context)
        return "Context created"

    @mcp.tool()
    def get_context(space: str, name: str):
        return mcs.get_context(space, name)

    @mcp.tool()
    def delete_context(space: str, name: str):
        mcs.delete_context(space, name)
        return "Context deleted"

    @mcp.tool()
    def list_spaces():
        return mcs.list_spaces()

    @mcp.tool()
    def list_contexts(space: str):
        return mcs.list_contexts(space)

    @mcp.tool()
    def search_contexts(space: str, query: str):
        return mcs.search_contexts(space, query)

    @mcp.tool()
    def search_all_spaces(query: str):
        return mcs.search_all_spaces(query)

    @mcp.tool()
    def get_version():
        return mcs.get_version()

    @mcp.tool()
    def get_author():
        return mcs.get_author()

    @mcp.tool()
    def get_author_email():
        return mcs.get_author_email()

    mcp.run()
if __name__ == "__main__":
    start_mcp_server()