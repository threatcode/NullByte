import json
import requests
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Load the data.json file
with open("core/data.json", "r") as data_file:
    data = json.load(data_file)

def sanitize_url(url):
    return url.strip().rstrip(':')  # Remove any trailing colons

def get_latest_version(repo_url):
    api_url = repo_url.replace("github.com", "api.github.com/repos") + "/releases/latest"
    headers = {'Authorization': f'token {YOUR_GITHUB_TOKEN}'}
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get(api_url, headers=headers)
        if response.status_code == 403:
            rate_limit_reset = int(response.headers.get('X-RateLimit-Reset', 0))
            if rate_limit_reset > 0:
                sleep_time = rate_limit_reset - time.time() + 1
                print(f"Rate limit exceeded. Sleeping for {sleep_time} seconds.")
                time.sleep(max(sleep_time, 0))
        response.raise_for_status()
        return response.json().get("tag_name")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching version for {repo_url}: {e}")
        return None

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
