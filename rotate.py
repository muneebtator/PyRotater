import os
import sys
from concurrent.futures import ThreadPoolExecutor
import random
from datetime import datetime
from itertools import product

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(os.path.join("outputs", timestamp, "temp"), exist_ok=True)
os.makedirs(os.path.join("outputs", timestamp, "runs"), exist_ok=True)

def divide_models(array):

    k = len(array) // os.cpu_count()
    m = len(array) % os.cpu_count()

    result = []
    start = 0

    for i in range(os.cpu_count()):
        end = start + k + (1 if i < m else 0)
        result.append(array[start:end])
        start = end

    return result


def read_sets_from_file(file_path):
    sets = []
    runs_without_set = None
    with open(file_path, 'r') as file:
        current_set = []
        for line in file:
            stripped_line = line.strip()
            if stripped_line.startswith("Runs_Without_Set"):
                runs_without_set = [int(val) for val in stripped_line.split("=")[1].split(",")]
            elif stripped_line:
                current_set.append(stripped_line)
            elif current_set:
                sets.append(current_set)
                current_set = []
        if current_set:  # Append the last set if not empty
            sets.append(current_set)

    # Create a directory for excluded sets if it doesn't exist
    excluded_dir = "excluded"
    if not os.path.exists(excluded_dir):
        os.makedirs(excluded_dir)

    if runs_without_set:
        # Write each excluded set to a separate file
        for idx in runs_without_set:
            if 1 <= idx <= len(sets):  # Check if idx is within valid range
                excluded_set = sets[idx - 1]
                excluded_sets = sets[:idx - 1] + sets[idx:]
                with open(os.path.join(excluded_dir, f"excluded_{idx}.txt"), 'w') as excluded_file:
                    for item in excluded_sets:
                        for sub_item in item:
                            excluded_file.write("%s\n" % sub_item)
                        excluded_file.write("\n")  # Add a blank line between sets
                    if excluded_sets:  # Add a blank line after the last set
                        excluded_file.write("\n")
    return sets, runs_without_set

def generate_models(sets, runs_without_set=None):
    all_combinations = list(product(*sets))

    # Check if there are excluded files
    excluded_dir = "excluded"
    if runs_without_set and os.path.exists(excluded_dir):
        excluded_files = [os.path.join(excluded_dir, f"excluded_{idx}.txt") for idx in runs_without_set]
        # Read sets from each excluded file
        for file in excluded_files:
            excluded_sets = []
            with open(file, 'r') as f:
                current_set = []
                for line in f:
                    stripped_line = line.strip()
                    if stripped_line:
                        current_set.append(stripped_line)
                    elif current_set:
                        excluded_sets.append(current_set)
                        current_set = []
                if current_set:  # Append the last set if not empty
                    excluded_sets.append(current_set)
            
            if excluded_sets:
                excluded_combinations = list(product(*excluded_sets))
                all_combinations.extend(excluded_combinations)

    return all_combinations

def config(model):

    set_name = ""
    indv_target = ""
    random_number = random.randint(1000, 9999)
    leftpops = os.path.join("outputs", timestamp, "temp", f"model_{random_number}.txt")
    
    with open(os.path.join("outputs", timestamp, "temp", f"parqpadm_{random_number}"), 'w') as outfile, open("parqpadm", 'r') as infile:
        for line in infile:
            if line.startswith('#'):
                if 'Set_Name' in line:
                    set_name = line.split('=')[1].strip()

                if 'Target' in line:
                    indv_target = line.split('=')[1].strip()
            else:
                outfile.write(line)
    
        outfile.write(f"popleft: outputs/{timestamp}/temp/model_{random_number}.txt\n")
        outfile.write(f"indivname: set/{set_name}.ind\n")
        outfile.write(f"snpname: set/{set_name}.snp\n")
        outfile.write(f"genotypename: set/{set_name}.geno\n")

    with open(leftpops, "w") as file:
        file.write(indv_target + "\n")
        if isinstance(model, (list, tuple)):
            for item in model:
                file.write(str(item) + '\n')
        else:
            file.write(str(model) + '\n')

    return random_number

def initiate_model(divided_models):

    for models in divided_models:

        if models:

            if isinstance(models, list) and any(isinstance(model, list) for model in models):

                for model in models:
                    
                    id = config(model)
                    os.system(f"qpAdm -p outputs/{timestamp}/temp/parqpadm_{id} > outputs/{timestamp}/runs/{id}")
                    print(f"Model {id} done")

            else:
                
                id = config(models)
                os.system(f"qpAdm -p outputs/{timestamp}/temp/parqpadm_{id} > outputs/{timestamp}/runs/{id}")
                print(f"Model {id} done")
    

def main():
    
    # Read sets of source populations from the file
    sets, runs_without_set = read_sets_from_file("source_populations.txt")
    
    # Generate all possible combinations of source populations
    all_models = generate_models(sets, runs_without_set)
    
    divided_models = divide_models(all_models)

    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(initiate_model, divided_models)

if __name__ == "__main__":
    main()