import os
from setuptools import setup, find_packages

# Read the requirements from the requirements.txt file
def get_requirements():
    with open("requirements.txt") as f:
        requirements = f.read().splitlines()
    return requirements

setup(
    name="clinical-chatbot",
    version="0.1.0",
    description="A clinical QA chatbot using Flask and LlamaIndex.",
    author="Kathiravan Thilagar",
    author_email="kathirloyola14@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires=">=3.10",
)
