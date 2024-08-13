import json
import requests

# Load the data.json file
with open("core/data.json", "r") as data_file:
    data = json.load(data_file)

# Function to get the latest version from the GitHub API
def get_latest_version(repo_url):
    api_url = repo_url.replace("github.com", "api.github.com/repos") + "/releases/latest"
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()["tag_name"]
    return None

# Update the versions
updated = False
for tool_name, tool_data in data.items():
    repo_url = tool_data["url"].replace(".git", "")
    latest_version = get_latest_version(repo_url)
    if latest_version and tool_data.get("version") != latest_version:
        print(f"Updating {tool_name} from {tool_data.get('version')} to {latest_version}")
        tool_data["version"] = latest_version
        updated = True

# Save the updated data.json file if changes were made
if updated:
    with open("core/data.json", "w") as data_file:
        json.dump(data, data_file, indent=2)
else:
    print("No updates were necessary.")
