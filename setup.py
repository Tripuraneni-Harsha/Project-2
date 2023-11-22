from setuptools import setup, find_packages

setup(
    name="my_package",  
    version="0.1.0",  
    author="Tripuraneni Venkat Sai Sri Harsha",  
    author_email="harshatripuraneni@gmail.com",  
    description="A package for extracting and analyzing web data",  
    long_description=open(
        "README.md"
    ).read(),  # Long description read from the the readme file
    long_description_content_type="text/markdown",
    url="https://github.com/Tripuraneni-Harsha/Project-2",  
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.2.0",
        "beautifulsoup4>=4.9.3",
        
    ],
    classifiers=[
        # Full list: https://pypi.org/classifiers/
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Minimum version requirement of the package
)
