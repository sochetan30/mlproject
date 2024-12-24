from setuptools import find_packages,setup
from typing import List

HYPHEN_E_DOT="-e ."
def get_requirements(file_path:str) -> List[str]:
    '''
    Functions returns the list of requirement
    '''
    requirements=[]

    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace('\n','') for req in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


set(
    name='ml_project',
    version='0.01',
    author='chetan',
    author_email='chetantrust30@gmail.com',
    packages=find_packages,
    install_requires=['pandas','numpy','seaborn']
)