import os
import sys
from itertools import product

def read_sets_from_file(file_path):
    sets = []
    with open(file_path, 'r') as file:
        current_set = []
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                current_set.append(stripped_line)
            elif current_set:
                sets.append(current_set)
                current_set = []
        if current_set:  # Append the last set if not empty
            sets.append(current_set)
    return sets

def generate_models(sets):
    all_combinations = list(product(*sets))
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
    sets = read_sets_from_file(file_path)
    
    # Generate all possible combinations of source populations
    all_models = generate_models(sets)
    
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

