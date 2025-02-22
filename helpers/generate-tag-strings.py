#!/usr/bin/env python3

import json

def generate_tag_strings(file_path: str, base_name: str) -> str:
    """
    Returns a CSV string of tag names.

    Args:
        file_path (str): Path to the JSON file.
        base_name: The base name of the image, i.e. edingc/telegraf-python

    Returns:
        str: A comma separated string of tag names.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # Use a list comprehension to create the tag list
    tag_list = [f"{base_name}:{tag}" for tag in data.get('tags', [])]
    
    return ','.join(tag_list)

if __name__ == "__main__":
    tag_string = generate_tag_strings('image.json','edingc/telegraf-python')
    print(tag_string)
