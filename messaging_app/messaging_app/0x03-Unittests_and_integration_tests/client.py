#!/usr/bin/env python3
"""GithubOrgClient module."""

from utils import get_json


class GithubOrgClient:
    """Client for accessing GitHub organization data."""

    def __init__(self, org_name: str) -> None:
        self.org_name = org_name

    def org_url(self) -> str:
        """Returns the API URL for the organization."""
        return f"https://api.github.com/orgs/{self.org_name}"

    @property
    def org(self) -> dict:
        """Fetches organization info using get_json."""
        return get_json(self.org_url())

    def _public_repos_url(self) -> str:
        """Returns the URL for public repositories."""
        return self.org["repos_url"]

    @property
    def repos_payload(self) -> list:
        """Fetches the public repos using get_json."""
        return get_json(self._public_repos_url())

    def public_repos(self, license: str = None) -> list[str]:
        """Returns list of public repositories names filtered by license."""
        repos = self.repos_payload
        if license:
            return [
                repo["name"] for repo in repos
                if repo.get("license", {}).get("key") == license
            ]
        return [repo["name"] for repo in repos]
