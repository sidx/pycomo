from setuptools import setup, find_packages

setup(
    name="pycomo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai>=0.28.0",
        "anthropic>=0.34.1",
        "httpx>=0.25.2",
        "pydantic>=1.10.12",
    ],
    author="sidx",
    author_email="sidharth.xtb@gmail.com",
    description="Python library to consume LLM outputs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sidx/pycomo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
) 