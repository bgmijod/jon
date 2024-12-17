import requestsimport base64
import osimport logging
# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")logger = logging.getLogger(__name__)
# Environment Variables
TOKEN = os.getenv("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")if not TOKEN:
    logger.error("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")    exit(1)
REPO = "bgmijod/jon"  # Replace with your GitHub username/repo
FILE_PATH = ".travis.yml"  # Ensure this matches the actual file in the repositoryBRANCH = "main"  # Default branch; ensure it matches your repository structure
HEADERS = {
    "Authorization": f"token {TOKEN}",    "Accept": "application/vnd.github.v3+json"
}
def fetch_file_info():
    """
    Fetch file content and SHA.    """
    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}?ref={BRANCH}"    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()    data = response.json()
    return data["sha"], data["content"]
def update_file(new_content, sha):
    """    Update the file content on GitHub.
    """    url = f"https://api.github.com/repos/{REPO}/contents/{FILE_PATH}"
    data = {        "message": "Add space to the end of file",
        "content": new_content,        "sha": sha,
        "branch": BRANCH    }
    response = requests.put(url, json=data, headers=HEADERS)    response.raise_for_status()
    logger.info("File updated successfully.")
def main():
    """    Main function to update the file once.
    """    try:
        logger.info("Fetching file information...")        sha, current_content = fetch_file_info()
        # Decode, modify, and encode the file content
        decoded_content = base64.b64decode(current_content).decode("utf-8").rstrip()  # Remove trailing spaces        updated_content = decoded_content + " "  # Add a single space
        encoded_content = base64.b64encode(updated_content.encode("utf-8")).decode("utf-8")
        # Update the file        logger.info("Updating file content...")
        update_file(encoded_content, sha)        logger.info("Successfully added a space to the file.")
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP Error: {e.response.status_code} - {e.response.text}")    except Exception as e:
        logger.error(f"An error occurred: {e}")
if name == "__main__":
n    main()
