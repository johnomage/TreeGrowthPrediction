import importlib
import pkg_resources

def print_package_versions(package_names):
    """
    Prints the version of each package in the provided list of package names.

    This function attempts to import each package by name and retrieve its version.
    If the package does not have a `__version__` attribute, it tries to get the version 
    using `pkg_resources`. If the package cannot be imported or its version cannot be determined,
    an appropriate message will be printed.

    Args:
        package_names (list of str): A list of package names to check. Package names should be 
                                      provided as strings. Note that for packages with hyphens 
                                      in their names (like 'python-dotenv'), use underscores 
                                      (e.g., 'python_dotenv').

    Example:
        package_list = ['pandas', 'numpy', 'python_dotenv']
        
        print_package_versions(package_list)
    """
    for package_name in package_names:
        try:
            # Attempt to import the package
            package = importlib.import_module(package_name)
            version = package.__version__
        except (ImportError, AttributeError):
            try:
                # If __version__ doesn't exist, try getting the version from pkg_resources
                version = pkg_resources.get_distribution(package_name).version
            except Exception as e:
                version = f"Could not determine version: {e}"
        
        print(f"{package_name}=={version}")

# Use case
package_list = [
    'pandas',
    'numpy',
    'kagglehub',
    'python_dotenv',  # Use underscore for importing
    'joblib',
    'tqdm',
    'geopy',
    'streamlit',
    'matplotlib',
    'plotly',
    'sklearn',
    'tensorflow',
]

print_package_versions(package_list)
