from setuptools import setup, find_packages
setup(
    name="sublimat",
    packages=find_packages(include=['sublimat*']),
    install_requires=[
        "pandas",  
    ],
    package_dir={'': '.'}, 
)