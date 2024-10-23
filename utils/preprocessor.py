# Import packages
import pandas as pd
import csv
import kagglehub
import os
import shutil
import city_mapper
from typing import List


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
            print('[INFO]: downloading data from kaggle source...')
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
    

    def separate_caps(self, text):
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
    

    def is_all_columns_same(self, data_list: List[pd.DataFrame]):
        """
        Compare the column names of multiple pandas DataFrames against the first DataFrame.

        This function checks whether the columns of each DataFrame in the given list 
        match the columns of the first DataFrame. It reports any discrepancies in 
        column names and lists the differences.

        Parameters:
            data_list (List[pd.DataFrame]): A list of pandas DataFrames to compare. 
                                            The first DataFrame in the list serves 
                                            as the reference for comparison.

        Returns:
            List[Tuple[int, bool]]: A list of tuples, where each tuple contains:
                - int : The index of the DataFrame being compared.
                - bool : True if the columns of the DataFrame match the columns of 
                        the first DataFrame, False otherwise.
        """
        
        reference_columns = data_list[0].columns
        results = []
        truths = []

        for i in range(1, len(data_list)):
            current_columns = data_list[i].columns
            is_equal = current_columns.equals(reference_columns)
            results.append((i, is_equal))
            truths.append(is_equal)

            if not is_equal:
                print(f"File {i} has different columns than the first file.")
                print("Columns in the first file:", reference_columns.tolist())
                print(f"Columns in file {i}:", current_columns.tolist())
                
                # Calculate and display differences
                missing_in_current = set(reference_columns) - set(current_columns)
                missing_in_reference = set(current_columns) - set(reference_columns)

                if missing_in_current:
                    print("In the first file but not in this file:", missing_in_current)
                if missing_in_reference:
                    print(f"In file {i} but not in the first file:", missing_in_reference)
                
                print("\n")

        # Return True only if all files have the same columns as the first file
        return all(truths)


    def load_dataframes(self):
        """Load CSV files into DataFrames, add elevation data, and validate column consistency.

        This method retrieves valid CSV files from the specified directory, 
        loads them into pandas DataFrames, and checks if all DataFrames have 
        the same column structure. If elevation data is needed, it will be 
        added to the relevant CSV files.

        Returns:
            pd.DataFrame: A single DataFrame resulting from the concatenation 
                       of all loaded DataFrames, or an empty DataFrame if 
                       column validation fails.
        """
        self.create_elevation_feature()  # Ensure elevation data is added

        csv_files = self.get_list_of_files()
        
        for file in csv_files:
            data = pd.read_csv(file, encoding='latin-1', on_bad_lines='skip', low_memory=False)
            df_name = file.split('_')[0].split('/')[-1]
            data = data[data.columns.sort_values()].copy()  # Sort the columns
            self.data_list.append(data)
            self.total_rows += data.shape[0]
            print(f'DataFrame {df_name} added. Shape: {data.shape}')

        # Check if all DataFrames have the same columns after loading
        if not self.is_all_columns_same(self.data_list):
            print("Error: Not all DataFrames have the same columns.")
            return []

        print('\nTotal rows match:', self.total_rows)
        
        print(f'Concatenating list of dataframes...')
        data_frame = pd.concat(self.data_list)
        print('Done')
        
        print(f'list of features found: {list(data_frame.columns)}')
        
        selected_features = ['city', 'common_name', 'condition', 'diameter_breast_height_CM', 'greater_metro',
                             'elevation', 'latitude_coordinate', 'longitude_coordinate','most_recent_observation',
                             'most_recent_observation_type', 'native', 'state', 'height_M']
        
        print(f'relevant features: {selected_features}')
        
        return data_frame[selected_features]



class Cleaner:
    pass
# Use case:
# loader = DataFrameLoader()
# dataframes = loader.load_dataframes()

# print(dataframes.sample(20))
