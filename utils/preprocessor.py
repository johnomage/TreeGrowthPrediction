# Import packages
import pandas as pd
import csv
import kagglehub
import os
import shutil
import city_mapper

class DataFrameLoader:
    """Load and process CSV files from a specified directory.

    This class handles downloading datasets, retrieving valid CSV files,
    adding elevation data, and loading the data into pandas DataFrames.
    """

    FILEPATH = os.path.join(os.path.pardir, 'mexwell/5m-trees-dataset')

    def __init__(self):
        """Initialize DataFrameLoader and ensure data is downloaded."""
        self.download_data()
        self.data_list = []
        self.total_rows = 0

    def download_data(self):
        """Download the latest version of the dataset if it does not exist."""
        if not os.path.exists(self.FILEPATH):
            download_path = kagglehub.dataset_download("mexwell/5m-trees-dataset")
            shutil.move(download_path, self.FILEPATH)
            print("Data downloaded and moved to working directory:", self.FILEPATH)
        else:
            print('"mexwell/5m-trees-dataset" already exists')

    def get_list_of_files(self):
        """Retrieve and list valid CSV files (>10KB) from the dataset directory.

        Returns:
            list: Paths of valid CSV files.
        """
        files_list = sorted([file for file in os.listdir(self.FILEPATH) if file.endswith('.csv')])
        print(f'Total files: {len(files_list)}\n')

        csv_files = []
        for file in files_list:
            file_path = os.path.join(self.FILEPATH, file)
            size = os.path.getsize(file_path) / 1024
            
            if size > 10:  # Check file size
                csv_files.append(file_path)
                print(f'Added {file} | size: {round(size / 1024, 2)}MB')

        print(f'\nTotal valid CSV files: {len(csv_files)}\n')
        return csv_files

    @staticmethod
    def separate_caps(text):
        """Inserts spaces between uppercase letters in a string, unless they're consecutive.

        Args:
            text: The string to separate.

        Returns:
            A new string with spaces inserted between uppercase letters.
        """
        result = []
        prev_was_upper = False
        
        for char in text:
            if char.isupper():
                if not prev_was_upper:
                    result.append(" ")
                result.append(char)
                prev_was_upper = True
            else:
                result.append(char)
                prev_was_upper = False
        return "".join(result)

    def create_elevation_feature(self):
        """Add elevation data to city CSV files if not already present."""
        for file in self.get_list_of_files():
            name = file.split("_")[0].split("/")[-1]

            # Check if 'elevation' already exists in the header
            already_elevation = False
            with open(file, "r") as f:
                for line in f:
                    if "elevation" in line.lower():
                        already_elevation = True
                        break
            if already_elevation:
                print(file, "Already contains elevation data. Skipping now.")
                continue

            # Calculate elevation for the city
            x, y = city_mapper.get_city_coordinates(self.separate_caps(name))
            this_elevation = city_mapper.get_elevation(x, y)

            print("Processing file:", name)
            if name == "RanchoCucamonga":
                this_elevation = 368  # Special case

            # Update CSV file with elevation data
            with open(file, "r") as f:
                reader = csv.reader(f, delimiter=",")
                lines = list(reader)
                lines[0].append("elevation")  # Add elevation field to header
                for row in lines[1:]:
                    row.append(this_elevation)

            with open(file, "w", newline="") as f:
                writer = csv.writer(f, delimiter=",")
                writer.writerows(lines)

    def load_dataframes(self):
        """Load CSV files into DataFrames and store them in a list.

        Returns:
            list: A list of pandas DataFrames loaded from the CSV files.
        """
        self.create_elevation_feature()  # Ensure elevation data is added

        for file in self.get_list_of_files():
            data = pd.read_csv(file, encoding='latin-1', on_bad_lines='skip', low_memory=False)
            df_name = file.split('_')[0].split('/')[-1]
            data = data[data.columns.sort_values()]  # Sort the columns
            self.data_list.append(data)
            self.total_rows += data.shape[0]
            print(f'DataFrame {df_name} added. Shape: {data.shape}')
        
        print('\nTotal rows:', self.total_rows)
        return self.data_list

# Example usage:
# loader = DataFrameLoader()
# dataframes = loader.load_dataframes()
