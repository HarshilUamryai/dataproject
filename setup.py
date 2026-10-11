from pathlib import Path

from setuptools import find_packages, setup


def get_requirements(file_path):
    file_path = Path(file_path)
    if not file_path.exists():
        alt_file = file_path.with_name('requirement.txt')
        if alt_file.exists():
            file_path = alt_file
    with file_path.open() as file:
        requirements = file.readlines()
    return [req.strip() for req in requirements if req.strip() and not req.startswith('#')]


setup(
    name='datascience_project',
    version='0.1',
    author='harshil',
    author_email='23bmiit116@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements(Path(__file__).resolve().parent / 'requirement.txt')
)