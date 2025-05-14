from setuptools import setup, find_packages

setup(
    name="mcsp",
    version="1.0.0",
    description="Model Context Store Protocol (MCSP) - a multimodal context store with MCP support",
    author="Mark Chen, Mindify AI",
    author_email="mark@mindifyai.dev",
    url="https://github.com/MarkCodering/mcsp",  # update if publishing
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.20.0",
        "pydantic>=1.10.0",
        "mcp @ git+https://github.com/modelcontextprotocol/python-sdk.git",  # or replace with PyPI if available
    ],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": [
            "mcsp-server = mcsp.server:start_mcp_server",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License"
    ],
    include_package_data=True,
    zip_safe=False,
)
