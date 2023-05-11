from github import Github

git = Github()


def get_authors_repos(username):
    repos = git.get_user(username).get_repos()
    data = [
        {
            "name": repo.name,
            "url": repo.svn_url,
            "updated_at": repo.pushed_at,
        }
        for repo in repos
    ]
    return data


if __name__ == "__main__":
    from pprint import pprint

    pprint(get_authors_repos("kpomak"))
