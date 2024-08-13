import json
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Load the data.json file
with open("core/data.json", "r") as data_file:
    data = json.load(data_file)

def sanitize_url(url):
    return url.strip().rstrip(':')  # Remove any trailing colons

def get_latest_version(repo_url):
    repo_url = sanitize_url(repo_url)
    api_url = repo_url.replace("github.com", "api.github.com/repos") + "/releases/latest"
    print(f"Requesting URL: {api_url}")  # Debug print statement
    session = requests.Session()
    retry = Retry(total=5, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    try:
        response = session.get(api_url)
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
