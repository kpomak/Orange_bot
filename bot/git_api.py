import os
from github import Github

git = Github()

repos = git.get_user(os.getenv("GITHUB_USER") or "kpomak").get_repos()

for repo in repos:
    print(repo.name, repo.svn_url, repo.pushed_at, sep="\n", end="\n" * 3)
