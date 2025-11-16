#!/usr/bin/env python3
"""Client module for GithubOrgClient"""
import requests


def get_json(url):
    """Get JSON content from a URL"""
    response = requests.get(url)
    return response.json()


class GithubOrgClient:
    """Github client class"""

    def __init__(self, org_name):
        self.org_name = org_name

    @property
    def org(self):
        """Return org information"""
        url = f"https://api.github.com/orgs/{self.org_name}"
        return get_json(url)

    @property
    def _public_repos_url(self):
        """Return repos URL from org data"""
        return self.org.get("repos_url")

    def public_repos(self):
        """Return list of public repo names"""
        url = self._public_repos_url
        repos = get_json(url)
        return [repo.get("name") for repo in repos]

    def has_license(self, repo, license_key):
        """Return True if repo has the given license_key"""
        return repo.get("license", {}).get("key") == license_key
