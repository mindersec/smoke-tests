import random
import string

from sh import gh
from robot.api.deco import keyword
from robot.api import logger


def randstring(size=6, chars=string.ascii_uppercase + string.digits):
    return "".join(random.choice(chars) for _ in range(size))  # nosec B311


def randint():
    return f"{random.randint(1000000, 9999999)}"  # nosec B311


class GitHub:
    def __init__(self):
        self.repos = []

    @keyword
    def random_repo_name(self, org, base_name):
        return f"{org}/{base_name}-{randint()}"

    @keyword
    def a_copy_of_repo(self, repo_template, repo_name):
        """Fork the given repo using base_name as name."""
        # gh repo create $repo_name --template $repo_template --public --include-all-branches
        logger.info(
            gh.repo.create(
                repo_name,
                "--template",
                repo_template,
                "--public",
                "--include-all-branches",
            )
        )
        self.repos.append(repo_name)

    @keyword
    def delete_repo(self, repo_name):
        """Delete repository from GitHub."""
        # gh repo delete $repo_name --yes
        logger.info(gh.repo.delete(repo_name, "--yes"))

    @keyword
    def cleanup_github_repos(self):
        """Deletes all created repositories."""
        for repo_name in self.repos:
            self.delete_repo(repo_name)

    @keyword
    def create_pr(self, repo_name, pr_title):
        """Opens a Pull Request against repository."""
        # gh pr create --base main --head $PR_TITLE --title $PR_TITLE --body $PR_TITLE
        logger.info(
            gh.pr.create(
                "--base",
                "main",
                "--head",
                pr_title,
                "--title",
                pr_title,
                "--body",
                pr_title,
                "--repo",
                repo_name,
            )
        )
