from setuptools import setup, find_packages

setup(
    name='Drone Trajectory Planner',
    version='1.0.0',
    description='Tool for planning waypoints for ariel capture of an area.',
    author='Ayush Baid',
    author_email='ayushrakeshbaid@gmail.com',
    url='https://hub.buildfellowship.com/projects/drone-flight-planner-system-flight-path-for-efficient-data-capture',
    packages=find_packages(), # Automatically discovers all packages in the directory
    install_requires=[
        'ruff',
        'jupyterlab',
        'plotly',
        'numpy'
    ],
)
