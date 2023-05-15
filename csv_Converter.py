import os
import csv

def convert_txt_to_csv(input_dir, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get a list of all text files in the input directory
    txt_files = [file for file in os.listdir(input_dir) if file.endswith('.txt')]

    for txt_file in txt_files:
        # Read the text file
        with open(os.path.join(input_dir, txt_file), 'r') as file:
            lines = file.readlines()

        # Remove the header (first line)
        data_lines = lines[1:]

        # Extract the column names from the header
        column_names = ['RF', 'BF', 'VM', 'ST', 'FX']

        # Prepare the output CSV file
        csv_file = txt_file.replace('.txt', '.csv')
        csv_path = os.path.join(output_dir, csv_file)

        # Write the data to the CSV file
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(column_names)  # Write column headings
            for line in data_lines:
                    values = line.strip().split('\t')[1:]
                    writer.writerow(values)

# Example usage
input_directory = "C:/Users/ayush/Downloads/SEMG_DB1/A_TXT"
output_directory = "C:/EMG/CSV_A"

convert_txt_to_csv(input_directory, output_directory)