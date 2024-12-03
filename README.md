Docker Action Staged Taint Analysis Utilizing Summaries and WIR
Description

Uses the fundamental ideologies established in the ARGUS taint analysis engine and expands it to Docker actions.
This is a standalone tool and does NOT work with ARGUS. Currently only works with select projects and is not tested
on industry-datasets. This is meant more as a proof-of-concept to show that it is possible to complete given enough resources
and time.

How to Use

    Make sure the repository is your current working directory.

    Run python ./src/main.py

    The output is located in the terminal and a file in the ./results/ folder

Currently supported docker types: 

    Local Dockerfiles (✓)
    Remote Docker Images (X)

Dataset

    As discussed in the presentation, there is not a reliable way to find datasets for GitHub Actions that utilize docker. 
    As a result this tool was tested using hand-built workflows. This repository is set up to utilize one of these example 
    workflows by default. If a user wants to test their own workflow they need to modify the filepath in the main python file.

Limitations: 

    Stops taint propagation once the Dockerfile is reached
    Only supports Dockerfiles that execute shell commands, does not support Dockerfiles that rely on external file execution (i.e. Python or JavaScript)

    Why? Time constraints. The support for these are relatively trivial, another parsing function needs to be added. But adding support for every type of Docker Action
    is not reasonable for the goal of the project. The main goal of propagating taints into Dockerfiles was achieved. It is already known that you can perform taint
    analysis on Python/JavaScript files with ease.

    May crash or miss taints when other workflows are attempted to be used.

    Why? As mentioned in the dataset section, finding thorough actions for testing was difficult given the time frame. The 
    handmade workflow lacks depth and as a result it does not encapsulate every taint imaginable in Docker actions. Other
    workflows may be missing parts that lack error handling, though most cases should be covered. The more likley result is
    a blank result being displayed.
    

Credits

Rochester Institute of Technology Golisano College of Computer Science and Information Technology Department of Cybersecurity CSEC 795 : Advanced Software Security
