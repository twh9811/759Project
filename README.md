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

    As discussed in the presentation, there is not a reliable way to find datasets for Docker actions. As a result this tool
    was tested using hand-built workflows. This repository is set up to utilize one of these example workflows by default. If
    a user wants to test their own workflow they need to modify the filepath in the main python file.

Credits

Rochester Institute of Technology Golisano College of Computer Science and Information Technology Department of Cybersecurity CSEC 795 : Advanced Software Security
