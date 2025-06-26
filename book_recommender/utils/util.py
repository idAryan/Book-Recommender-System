import yaml
import os

def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its contents as a dictionary.
    
    Args:
        file_path (str): Path to the YAML file.
    
    Returns:
        dict: Parsed YAML content.
    
    Raises:
        FileNotFoundError: If the file doesn't exist.
        yaml.YAMLError: If the file is not a valid YAML.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"YAML file not found: {file_path}")
    
    with open(file_path, 'r') as yaml_file:
        try:
            content = yaml.safe_load(yaml_file)
            return content if content else {}
        except yaml.YAMLError as e:
            raise Exception(f"Error while reading YAML file: {file_path}\n{e}")
