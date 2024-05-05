import os
import sys
from itertools import product

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


def write_model_to_file(model, parameter):
    with open("left.txt", 'w') as file:
        # Write the parameter as the first line
        file.write(parameter + "\n")
        # Write the model to the left.txt file
        for item in model:
            file.write("%s\n" % item)
            
def run_command_for_model(output_file):
    # Run the command for the current model
    command = f"qpAdm -p parqpadm > outputs/{output_file}"
    os.system(command)

def main(parameter):
    # File path containing sets of source populations
    file_path = "source_populations.txt"
    
    # Read sets of source populations from the file
    sets, runs_without_set = read_sets_from_file(file_path)
    
    # Generate all possible combinations of source populations
    all_models = generate_models(sets, runs_without_set)
    
    # Run the command for each model
    for idx, model_set in enumerate(all_models, start=1):
        write_model_to_file(model_set, parameter)
        output_file = f"model_{idx}.txt"
        run_command_for_model(output_file)
        print(f"Model {idx} done: {model_set}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    parameter = sys.argv[1]
    main(parameter)

