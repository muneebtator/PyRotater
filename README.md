# PyRotator
PyRotator is an experimental qpAdm model rotation automation script written Python. It generates the maximum number of possible source population combinations and then runs models on them, saving the individual qpAdm output for each model and creating a spreadsheet for all the models ran as well. 
## Installation instructions
### Dependencies
Before starting, make sure you have AdmixTools, python3 and pandas python package (through pip) already installed.

    wget https://github.com/muneebtator/PyRotator/archive/refs/heads/main.zip
    unzip main.zip

### Running script
Put your source/left pop model sets/groups in the `source_populations.txt` file. Each source set/group is separated by a new line, you can check the example `source_populations.txt`.

Create a directory called `outputs` in your workspace, this is where the model outputs will be saved. Make sure the `popleft` in  your qpAdm parameter file is called `left.txt`, this file will be automatically generated for each model by PyRotator.

Your qpAdm parameter file needs to be called `parqpadm`.

PyRotator takes the name of the sample you want to generate rotated models for as it's parameter, see below example to rotate.

    python3 rotate.py Pashtun_Yusufzai
Once the rotation is complete and all the models are generated, you can run `outputparser.py` to generate a spreadsheet of all your rotated models.

    python3 outputParser.py
### Features to be added.
 - Create different directories for different rotation runs and automatically parse model files to generate spreadsheet once rotation is done.
 - Automatically create output directory if not created.
 - Have the parser sort the spreadsheet based on p-value and provide a 'passed' column.
 - Switch to job scheduler instead of directly running the qpAdm command.
 - Further work on model generations to generate more models for runs (e.g. option to drop source populations sets/groups).
