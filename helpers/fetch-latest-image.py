#!/usr/bin/env python3

import urllib.request
import json
import random
from typing import Optional

def get_random_user_agent() -> str:
    """
    Returns a random User-Agent string from real browsers (Chrome, Firefox, Safari).

    The function generates realistic User-Agent strings that emulate genuine browsers
    across different operating systems and versions.

    Returns:
        str: A random User-Agent string.
    """

    # Example OS and browser version data
    chrome_versions = ["121.0.6167.140", "122.0.6261.69", "123.0.6312.86"]
    firefox_versions = ["123.0", "124.0", "125.0"]
    safari_versions = ["17.3", "17.4", "17.5"]
    mac_versions = ["13_4", "13_5", "14_0"]
    windows_versions = ["10.0; Win64; x64", "11.0; Win64; x64"]

    # Choose a browser at random
    browser = random.choice(["chrome", "firefox", "safari"])

    if browser == "chrome":
        ua = (
            f"Mozilla/5.0 (Windows NT {random.choice(windows_versions)}) "
            f"AppleWebKit/537.36 (KHTML, like Gecko) "
            f"Chrome/{random.choice(chrome_versions)} Safari/537.36"
        )

    elif browser == "firefox":
        ua = (
            f"Mozilla/5.0 (Windows NT {random.choice(windows_versions)}; rv:{random.choice(firefox_versions)}) "
            f"Gecko/20100101 Firefox/{random.choice(firefox_versions)}"
        )

    else:  # Safari
        ua = (
            f"Mozilla/5.0 (Macintosh; Intel Mac OS X {random.choice(mac_versions)}) "
            f"AppleWebKit/605.1.15 (KHTML, like Gecko) "
            f"Version/{random.choice(safari_versions)} Safari/605.1.15"
        )

    return ua

def get_image_tags(repository: str, user_agent: str, page_size: Optional[int] = 10) -> str:
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
        
        req = urllib.request.Request(url, 
            data=None,
            headers={
                'User-Agent': user_agent
                }
        )

        # Make a GET request and fetch the response
        with urllib.request.urlopen(req) as response:
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

    user_agent = get_random_user_agent()
    json_data = get_image_tags(image, user_agent)
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
