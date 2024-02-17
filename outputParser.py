import os
import pandas as pd

# Directory containing the output files
directory = 'outputs'

# Initialize lists to store data and column names
all_data = []
header_row = ["Model file", "Sample", "P-Value"]

added_row = False

# Iterate over each file in the directory
for filename in os.listdir(directory):
    # Check if the file is a text file
    if filename.endswith(".txt"):
        filepath = os.path.join(directory, filename)
        # Open the file
        with open(filepath, 'r') as file:
            lines = file.readlines()
            
            left_pops = []
            p_value = None
            extra_values = []
            std_errors = []
            best_coefficients = []

            parsing_left_pops = False
            parsing_summ = False
            parsing_std_errors = False
            parsing_best_coefficients = False

            # Iterate through each line in the file
            for line in lines:
                line = line.strip()

                if line == "left pops:":
                    parsing_left_pops = True
                    continue
                
                if parsing_left_pops:
                    if line == "" or line.startswith("right pops:"):
                        parsing_left_pops = False
                        continue
                    else:
                        left_pops.append(line)

                if line.startswith("summ:"):
                    parsing_summ = True
                    # Split the line and extract the p-value and additional values
                    parts = line.split()
                    p_value = parts[3]
                    # Convert additional values to percentages
                    num_extra_values = len(left_pops) - 1
                    extra_values = [float(value) * 100 for value in parts[4:4+num_extra_values]]
                    parsing_summ = False
                    continue

                if line.startswith("std. errors:"):
                    parsing_std_errors = True
                    # Split the line and extract the standard errors values
                    std_errors = [float(value) * 100 for value in line.split()[2:]]  # Convert to percentage
                    parsing_std_errors = False
                    continue
                
                if line.startswith("best coefficients:"):
                    parsing_best_coefficients = True
                    # Split the line and extract the coefficients
                    parts = line.split()
                    coefficients = [float(value) * 100 for value in parts[2:]]  # Convert to percentage
                    best_coefficients.extend(coefficients)
                    parsing_best_coefficients = False
                    continue

            # Append data for the current file to the list
            all_data.append([filename, left_pops[0], p_value] + left_pops[1:] + extra_values + std_errors + best_coefficients)
            
            if added_row == False:
                # Update header row based on the number of source files, std errors, and best coefficients
                num_sources = len(left_pops) - 1
                num_sources2 = len(left_pops) - 1
                num_std_errors = len(std_errors)
                num_best_coefficients = len(best_coefficients)
                for i in range(1, num_sources + 1):
                    header_row.append(f"Source {i}")
                for i in range(1, num_sources2 + 1):
                    header_row.append(f"Weight {i}")
                for i in range(1, num_std_errors + 1):
                    header_row.append(f"Std Error {i}")
                for i in range(1, num_best_coefficients + 1):
                    header_row.append(f"Coefficient {i}")
                added_row = True

# Prepend the header row to the list of data
all_data.insert(0, header_row)

# Create a DataFrame from the list of data
df = pd.DataFrame(all_data)

# Write the DataFrame to an Excel file
output_excel = 'output_data.xlsx'
df.to_excel(output_excel, index=False, header=False)

print("Output data written to", output_excel)

