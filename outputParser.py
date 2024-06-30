import os # Module to interact with filesystem
import sys
import pandas as pd # Module to make tabular data such as excel spreadsheets.


def main(id):

    all_data = [] # The main table
    header_row = ["Model file", "Sample", "P-Value"] # Header row of the table which will be later expanded on based on number of source_populations in each model.
    source_populations = [] # List of source populations which will be used to calculate the header row columns and exluded columns for exluded sources.
    runs_without_set = [] # List of exluded sets, this will be used to empty cells for excluded sources/sets in the spreadhseet.

    # Find out the source populations sets
    with open('source_populations.txt', 'r') as file:
        # Read the source_populations.txt file as a single string
        source_populations_raw = file.read()
        
    # Convert the single string from the source_populations into a list of strings separated by a new line
    source_populations_raw = source_populations_raw.strip().split('\n')

    # Filter and remove any special commands from the source_populations_raw list
    source_populations_filtered = []
    for source_population in source_populations_raw:
        if not source_population.startswith("Runs_Without_Set"):
            source_populations_filtered.append(source_population)
        else:
            runs_without_set = [int(val) for val in source_population.split("=")[1].split(",")]

    # Convert the filtered list back to a single string.
    source_populations_filtered = '\n'.join(source_populations_filtered)

    # Split the filtered string into a list based on blank lines ('\n\n')
    # Each element in the list is a single source population set with sources separated by a newline character ('\n')
    source_populations_filtered = source_populations_filtered.split('\n\n')

    # Loop through every source population set
    for source_population in source_populations_filtered:

        # The extra code here is to remove any empty lines which end up becoming empty sources in the source_populations list.
        
        # Initialize an empty list for the current population set
        source_population_set = []
        
        # Split the current source population string into individual sources based on the newline character
        sources = source_population.split('\n')
        
        # Iterate over each source in the sources list
        for source in sources:
            # Strip the source to remove leading/trailing whitespace and check if it is not empty
            if source.strip():
                # If the source is not empty, add it to the source_population_set list
                source_population_set.append(source)
            
        # Add the new list of source population set to source_populations
        source_populations.append(source_population_set)

    # Create the header rows
    for i in range(1, len(source_populations) + 1):
        header_row.append(f"Source {i}")

    for i in range(1, len(source_populations) + 1):
        header_row.append(f"Weight {i}")

    for i in range(1, len(source_populations) + 1):
        header_row.append(f"Std Error {i}")

    for i in range(1, len(source_populations) + 1):
        header_row.append(f"Coefficient {i}")

    # Iterate over each file in the directory
    for filename in os.listdir(f'outputs/{id}/runs'): # The listdir function returns a list with the filenaes and the fort statement loops over them.
                
        if filename.endswith(".txt"): # Check if the model text files exist.
            
            filepath = os.path.join("outputs", id, "runs", filename) # This function creates a complete filepath to the model file.
            
            with open(filepath, 'r') as file: # Acess the open() context manager using with statement.
                
                lines = file.readlines() # Read the model file line by line and returns a list of strings.
                
                left_pops = []
                p_value = None
                extra_values = []
                std_errors = []
                best_coefficients = []

                left_pops_parsed = False

                # Iterate through each line in the file
                for line in lines:
                
                    line = line.strip() # Remove the leading and trailing whitepaces in the line.
                    
                    # Once we reach the left pops section, set the left_pops_parsed to true.
                    if line == "left pops:":
                        left_pops_parsed = True
                        continue
                    
                    # If we are still at the left pops section then add line (which would be the name of the left pop) to the left_pops list.
                    # If we have reached the right pops section then set the left_pops_parsed to false.
                    # Note that this will include the target as well.
                    if left_pops_parsed:
                        if line == "" or line.startswith("right pops:"):
                            left_pops_parsed = False
                            continue
                        else:
                            left_pops.append(line)

                    # When we reach the summ line.
                    if line.startswith("summ:"):
                        parts = line.split() # Split the line based on whitepaces.
                        p_value = parts[3] # Get the P-value from it's location.
                        num_extra_values = len(left_pops) - 1 # Get the total number of left pops by subtracting the target from the left pops.
                        extra_values = [float(value) * 100 for value in parts[4:4+num_extra_values]] # Using Python list comprehension, convert the weights of the left pops to percentages.
                        continue

                    if line.startswith("std. errors:"):
                        # Split the line and extract the standard errors values
                        std_errors = [float(value) * 100 for value in line.split()[2:]]  # Convert to percentage
                        continue
                    
                    if line.startswith("best coefficients:"):
                        # Split the line and extract the coefficients
                        parts = line.split()
                        coefficients = [float(value) * 100 for value in parts[2:]]  # Convert to percentage
                        best_coefficients.extend(coefficients)
                        continue
                
                # Append data for the current file to the list
                if len(std_errors) != len(source_populations):
            
                    # Contains the positions index of the exluded set
                    adjusted_runs_without_set = [index - 1 for index in runs_without_set]

                    # Iterate over the adjusted_runs_without_set indices
                    for index in adjusted_runs_without_set:
                        
                    # Check if index is within the bounds of source_populations
                        if index < len(source_populations):
                            
                            # Check if the exlcuded set isn't present in the model
                            # If not, add empty rows in it's place.
                            
                            if any(item in source_populations[index] for item in left_pops):
                                
                                print("")

                            else:
                                                    
                                left_pops.insert(index + 1, "")
                                extra_values.insert(index, "")
                                std_errors.insert(index, "")
                                best_coefficients.insert(index, "")


                all_data.append([filename, left_pops[0], p_value] + left_pops[1:] + extra_values + std_errors + best_coefficients)
        

    # Prepend the header row to the list of data
    all_data.insert(0, header_row)


    # Create a DataFrame from the list of data
    df = pd.DataFrame(all_data)

    # Write the DataFrame to an Excel file
    output_excel = f'outputs/{id}/output_data.xlsx'
    df.to_excel(output_excel, index=False, header=False)

    print("Output data written to", output_excel)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    id = sys.argv[1]
    main(id)