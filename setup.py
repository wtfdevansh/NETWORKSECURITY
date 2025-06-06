from setuptools import setup, find_packages
from typing import List

def get_requirements(file_path: str) -> List[str]:

    """
    Reads a requirements file and returns a list of requirements.
    """

    requirements_lst:List[str] = []

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            for line in lines:
                requirements = line.strip()


                if requirements and requirements != '-e .':
                    requirements_lst.append(requirements)
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. No requirements will be installed.")

    return requirements_lst


setup(
    name='networksecurity',
    version='0.1.0',
    author='devansh',
    author_email='mrdivu7@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
    description='A package for network security analysis and monitoring',
)

