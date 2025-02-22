#!/usr/bin/env python3

import urllib.request
import json
from typing import Optional


def get_image_tags(repository: str, page_size: Optional[int] = 10) -> str:
    """
    Returns a JSON string of available images from Docker Hub.

    Args:
        repository (str): The repository name. Official images use "library/image_name" format, otherwise "username/image_name".
        page_size (Optional[int], optional): Number of images to return. Defaults to 10.

    Returns:
        str: JSON-formatted string of images.
    
    Raises:
        ValueError: If page_size is less than 0.
    """
    
    try:
        if page_size <= 0:
            raise ValueError("param2 must be greater than zero.")
        
        url = f"https://hub.docker.com/v2/repositories/{repository}/tags?&page_size={page_size}"
        
        # Make a GET request and fetch the response
        with urllib.request.urlopen(url) as response:
            # Read and decode the response
            data = response.read().decode()

            # Parse the JSON data and get the results
            parsed_data = (json.loads(data)).get('results')

        return parsed_data
    
    except ValueError as e:
        # Log the error before raising it
        logging.error("Error in get_image_tags: %s", e)
        raise
    except Exception as e:
        # General exception handling
        logging.error("Unexpected error: %s", e)
        raise

def get_latest_digest(json_data: str) -> str:
    """
    Returns a string of with the digest (sha256) of the image tagged 'latest'.

    Args:
        json_data (str): JSON data returned from DockerHub.

    Returns:
        str: digest of the image tagged 'latest'.
    """

    # Extract the sha of the 'latest' image tag
    for image in json_data:
        if image.get('name') == "latest":
            digest = image.get('digest')

    return digest

def get_tags_by_digest(json_data: str, digest: str) -> str:
    """
    Returns a list of images tags for a given digest string.

    Args:
        json_data (str): JSON data returned from DockerHub.
        digest (str): Docker image digest string.

    Returns:
        list: List of image tags matching the digest string.
    """

    # Create an empty list
    image_tags = []

    # Extract the names of time images with matching digest
    for image in json_data:
        if image.get('digest') == digest:
            image_tags.append(image.get('name'))

    return image_tags

if __name__ == "__main__":

    image = "library/telegraf"

    json_data = get_image_tags(image)
    latest_sha = get_latest_digest(json_data)
    tags = get_tags_by_digest(json_data, latest_sha)
    
    # Create a dictionary with these values so we can output json
    data = {
        "image": image,
        "digest": latest_sha,
        "tags": tags
    }

    # Convert the Python dictionary to a JSON string
    json_data = json.dumps(data, indent=4)  # The indent argument formats the JSON for readability

    # Output the JSON string
    print(json_data)
