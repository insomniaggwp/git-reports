import os
import argparse
from github import Github, Auth

# Load token from environment variable
TOKEN = os.getenv("GITHUB_TOKEN")  # Store token securely

if not TOKEN:
    raise ValueError("GitHub token is missing. Set GITHUB_TOKEN as an environment variable.")

# Authenticate using the secure method
auth = Auth.Token(TOKEN)
g = Github(auth=auth)

def get_all_repos():
    """ Fetch and print all repositories for the authenticated user. """
    try:
        for repo in g.get_user().get_repos():
            print(repo.name)
    except Exception as e:
        print(f"Error fetching repositories: {e}")

def get_all_commits(owner, repo_name, branch="main", author_email=None):
    """ Fetch and print all commits in the specified repository. """
    try:
        # Ensure the repository exists
        try:
            repo = g.get_repo(f"{owner}/{repo_name}")
        except Exception as e:
            print(f"Error: Unable to access repository '{owner}/{repo_name}'. Please check if it exists.")
            return

        # Fetch commits from the specified branch
        commits = repo.get_commits(sha=branch)

        if commits.totalCount == 0:
            print(f"No commits found in branch '{branch}'.")
            return

        for commit in commits:
            author = commit.commit.author

            if author_email is None or (author and author.email == author_email):
                print(f"Commit: {commit.html_url}")
                print(f"Commit SHA: {commit.sha}")
                print(f"Message: {commit.commit.message}")
                print(f"Author: {author.name if author else 'Unknown'}")
                print(f"Email: {author.email if author else 'Unknown'}")
                print(f"Date: {commit.commit.author.date if commit.commit.author else 'Unknown'}")
                print("-" * 50)

    except Exception as e:
        print(f"Error fetching commits: {e}")

def main():
    parser = argparse.ArgumentParser(description="GitHub API CLI")
    parser.add_argument("command", choices=["get_all_repos", "get_all_commits"], help="Command to execute")
    
    parser.add_argument("--owner", help="GitHub repository owner")
    parser.add_argument("--repo", help="Repository name")
    parser.add_argument("--branch", default="main", help="Select branch (default: main)")
    parser.add_argument("--author", help="Filter based on author email")

    args = parser.parse_args()

    if args.command == "get_all_repos":
        get_all_repos()
    elif args.command == "get_all_commits":
        if not args.owner or not args.repo:
            print("Error: --owner and --repo are required for get_all_commits")
            return
        get_all_commits(args.owner, args.repo, args.branch, args.author)
    else:
        print(f"Unknown command: {args.command}")

if __name__ == "__main__":
    main()
