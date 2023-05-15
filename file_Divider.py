import os
import shutil

def move_files_to_subfolders(source_path):
    # Create subfolders for each unique starting number
    for file_name in os.listdir(source_path):
        prefix = file_name.split("A")[0]
        folder_name = prefix
        folder_path = os.path.join(source_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)

    # Move files to respective subfolders based on their starting number
    for file_name in os.listdir(source_path):
        prefix = file_name.split("A")[0]
        folder_name = prefix
        source_file_path = os.path.join(source_path, file_name)
        destination_folder_path = os.path.join(source_path, folder_name)
        shutil.move(source_file_path, destination_folder_path)

# Example usage
source_directory = "C:/EMG/CSV_A"

move_files_to_subfolders(source_directory)
