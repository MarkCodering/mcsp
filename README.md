# Model Context Store Protocol

# How to use the Model Context Store Protocol

# 1. Install the required packages

pip install mcsp

```python
from mcsp import ModelContextStoreProtocol

# 2. Create a ModelContextStoreProtocol instance
mcs = ModelContextStoreProtocol(name="example_model_context_store",
                                description="An example model context store",
                                version="1.0.0",
                                author="Your Name",
                                author_email="your_email@example.com",
                                isTracking=True,
                                )

# 3. Run it as a MCP server
mcs.run()

# 4. Use the ModelContextStoreProtocol instance to store and retrieve model contexts
mcs.create_space("example_space")
mcs.create_context(space="example_space", name="example_context", context={"name": "value"})
# 5. Retrieve the context
context = mcs.get_context(space="example_space", name="example_context")
print(context)  # Output: {'name': 'value'}

# 6. List all spaces
spaces = mcs.list_spaces()
print(spaces)  # Output: ['example_space']

# 7. List all contexts in a space
contexts = mcs.list_contexts(space="example_space")
print(contexts)  # Output: ['example_context']

# 8. Delete a context
mcs.delete_context(space="example_space", name="example_context")
# 9. Delete a space
mcs.delete_space("example_space")

# 10. Search for contexts
search_results = mcs.search_contexts(space="example_space", query="name")
print(search_results)  # Output: [{'name': 'value'}]
# 11. Get the version of the ModelContextStoreProtocol
version = mcs.get_version()
print(version)  # Output: 1.0.0
# 12. Get the author of the ModelContextStoreProtocol
author = mcs.get_author()
print(author)  # Output: Your Name
# 13. Get the author email of the ModelContextStoreProtocol    
author_email = mcs.get_author_email()
print(author_email)  # Output:

# 14. Search across all spaces
search_results = mcs.search_all_spaces(query="name")
```