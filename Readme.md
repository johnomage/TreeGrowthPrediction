
# Predicting Tree Growth Using 5 Million 🌴 Across the US


## Overview

This project aims to predict tree growth using a dataset comprising over 5 million trees across the United States. By applying machine learning techniques, we seek to analyse various factors influencing tree growth and make accurate predictions that could benefit tree-related overhead powerline faults management, forestry management, and maybe ecological research 😎.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Dataset](#dataset)
- [Packages You May Need](#packages-you-may-need)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Getting Started

To get started with the project, follow these instructions:

### Prerequisites

Ensure that you have Python 3.x installed on your machine.

### Installation

1. **Clone the repository:**
   ```bash
    git clone https://github.com/johnomage/TreeGrowthPrediction.git
    cd TreeGrowthPrediction
    pip install -r requirements.txt
   ```

2. **Install required packages:**
   You can install the required packages using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```
Or if you prefer Conda:
```bash
    conda create --name venv -y
    conda activate venv
    pip install -r requirements.txt
```

---

## Dataset

The dataset used in this project includes data from 5 million trees in the US, covering various features such as species, age, location, and environmental conditions.

#### Data Column Descriptions

Get the dataset on [Kaggle](https://www.kaggle.com/datasets/mexwell/5m-trees-dataset)


The dataset contains several columns that provide detailed information about each tree. Below is a description of each column:

| **Column Name**                          | **Definition**                                                                                               |
|------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| **city_ID**                              | Unique identifier assigned to the tree by the city.                                                         |
| **tree_ID**                              | Our unique identifier for each tree.                                                                         |
| **planted_date**                         | The date the tree was planted.                                                                               |
| **most_recent_observation**              | The most recent observation date of the tree (among dates such as condition_date, edit_date, inspect_date). |
| **retired_date**                         | The date the tree was retired.                                                                               |
| **most_recent_observation_type**         | The type of the most recent observation (e.g., condition_date, edit_date).                                  |
| **common_name**                          | Common name of the tree species in plain English.                                                           |
| **scientific_name**                      | Biological name of the tree species (e.g., *Quercus rubrus*).                                             |
| **greater_metro**                        | The greater metro area in which the city is located, matching the city name in the filename.                |
| **city**                                 | Properly spelled name of the city (e.g., Las Vegas).                                                        |
| **state**                                | Properly spelled name of the state (not abbreviation).                                                       |
| **longitude_coordinate**                 | Exact longitude of the tree species location.                                                                |
| **latitude_coordinate**                  | Exact latitude of the tree species location.                                                                 |
| **location_type**                        | Where the tree is located (e.g., green_space, built_environment, no_info).                                  |
| **zipcode**                              | Zip code of the tree location.                                                                                |
| **address**                              | Address where the data was collected.                                                                         |
| **neighborhood**                         | Neighborhood of the tree's location.                                                                         |
| **location_name**                        | Name of the location if not an address (e.g., Smith Cemetery, Route 11 Median).                           |
| **ward**                                 | City ward in which the tree is located.                                                                      |
| **district**                             | District where the tree is located.                                                                          |
| **overhead_utility**                    | Indicates the presence of overhead utilities (yes, no, conflicting).                                        |
| **diameter_breast_height_CM**           | Trunk diameter in centimeters at breast height.                                                              |
| **condition**                            | Tree condition as coded by the city-specific protocol, converted to standardized conditions.                 |
| **height_M**                             | Height of the tree in meters.                                                                                |
| **native**                               | Indicates if the tree is native (naturally occurring), not native (introduced), or of unknown status.        |
| **height_binned_M**                      | Range of heights into which the tree falls, converted from feet.                                            |
| **diameter_breast_height_binned_CM**    | Range of diameters into which the tree falls, converted from inches.                                         |

<br></br>
> 💡 **Note:**

For reference on data prepreprocessing, you can follow the original source's [README.md](https://github.com/MrDevel0per/bio-data-analysis/blob/main/README.md). This will provide insights into the dataset structure and the methods employed for cleaning and preparation.


## Packages You May Need

This project utilizes the following packages:

- **pandas**: For data manipulation and analysis.
- **numpy**: For numerical computations.
- **kagglehub**: For accessing datasets from Kaggle.
- **python-dotenv**: For managing environment variables.
- **joblib**: For efficient serialization of large data.
- **tqdm**: For displaying progress bars in loops.
- **geopy**: For geolocation services.
- **streamlit**: For building interactive web applications.

## Usage

To run the application, use the following command:
```bash
streamlit run app.py
```
Replace `app.py` with the name of your main application file.

## Contributing

Contributions are welcome! If you have suggestions, bug fixes, or improvements, please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to [MrDevel0per's bio-data-analysis](https://github.com/MrDevel0per/bio-data-analysis/) for starting this work and for providing the dataset.
- [Praise](https://www.linkedin.com/in/praizerema/): for assisting with web design HTML/CSS stuff
- The open-source community for their invaluable contributions.

---
