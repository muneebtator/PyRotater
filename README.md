# qpAdm.py
qpAdm.py is an experimental qpAdm model rotation automation script written in Python that supports multithreading. It efficiently generates all possible combinations of source populations, runs models on them, and saves the qpAdm output for each model. Additionally, it creates a spreadsheet summarizing all the models run. By distributing the workload across all available CPU cores, it significantly speeds up the process.
## Installation instructions
### Dependencies
Before starting, make sure you have AdmixTools, python3 and pandas python package (through pip) already installed.

    wget https://github.com/muneebtator/qpAdm.py/archive/refs/heads/main.zip
    unzip main.zip

### Running script
Put your source/left pop model sets/groups in the `source_populations.txt` file. Each source set/group is separated by a new line, you can check the example `source_populations.txt`.

Make sure the `popleft` in  your qpAdm parameter file is called `left.txt`, this file will be automatically generated for each model by qpAdm.py.

Your qpAdm parameter file needs to be called `parqpadm` and it needs to be in the following format

    # Set_Name = rotation
    # Target = Dad
    popright: right.txt
    inbreed: NO
    allsnps: YES
    details: YES
    summary: YES
The `#` prefix is used to config qpAdm.py. `Set_Name` should be the name of your set and it needs to be in a separate folder called 'set'. The `Target` should be the name of the sample you want to run models on.

qpAdm.py takes the name of the sample you want to generate rotated models for as it's parameter, see below example to rotate.

    python3 qpAdm.py
Once the rotation is complete and all the models are generated in the output folder, you can run `outputparser.py` to generate a spreadsheet of all your rotated models.

    python3 outputParser.py
