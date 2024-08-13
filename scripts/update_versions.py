import json
import os
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Load the data.json file
with open("core/data.json", "r") as data_file:
    data = json.load(data_file)

# Function to get the latest version from the GitHub API
def get_latest_version(repo_url):
    # Strip .git if present in the URL
    repo_url = repo_url.rstrip('.git')
    api_url = repo_url.replace("github.com", "api.github.com/repos") + "/releases/latest"
    print(f"Requesting URL: {api_url}")  # Debug print
    token = os.getenv('GITHUB_TOKEN')
    headers = {'Authorization': f'token {token}'} if token else {}
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get(api_url, headers=headers)
        print(f"Response status code: {response.status_code}")  # Debug print
        if response.status_code == 403:
            rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))
            if rate_limit_reset > 0:
                sleep_time = rate_limit_reset - time.time() + 1
                print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
                time.sleep(max(sleep_time, 0))
                return get_latest_version(repo_url)  # Retry after sleeping
        response.raise_for_status()
        if response.status_code == 404:
            print(f"Repository {repo_url} does not have a release or is not found.")
            return None
        return response.json().get("tag_name")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching version for {repo_url}: {e}")
        return None

# Example usage
for repo_name, repo_info in data.items():
    version = get_latest_version(repo_info['url'])
    print(f"Latest version for {repo_name}: {version}")

# Update the versions
updated = False
for tool_name, tool_data in data.items():
    repo_url = tool_data.get("url")
    if repo_url:  # Check if the URL is not None
        repo_url = repo_url.replace(".git", "")
        latest_version = get_latest_version(repo_url)
        if latest_version and tool_data.get("version") != latest_version:
            print(f"Updating {tool_name} from {tool_data.get('version')} to {latest_version}")
            tool_data["version"] = latest_version
            updated = True
    else:
        print(f"Skipping {tool_name} due to missing URL")

# Save the updated data.json file if changes were made
if updated:
    with open("core/data.json", "w") as data_file:
        json.dump(data, data_file, indent=2)
else:
    print("No updates were necessary.")
