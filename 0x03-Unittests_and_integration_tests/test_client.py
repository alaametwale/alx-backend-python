#!/usr/bin/env python3
"""
Test module for client.py
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient
from utils import access_nested_map, get_json, memoize


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.requests.get')
    def test_org(self, org_name, mock_get):
        """Test GithubOrgClient.org returns correct data"""
        client = GithubOrgClient(org_name)
        mock_get.return_value.json.return_value = {"login": org_name}
        result = client.org
        self.assertEqual(result["login"], org_name)
        mock_get.assert_called_once()

    @patch('client.GithubOrgClient.org', new_callable=unittest.mock.PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url property"""
        mock_org.return_value = {"repos_url": "https://api.github.com/orgs/test/repos"}
        client = GithubOrgClient("test_org")
        self.assertEqual(client._public_repos_url, "https://api.github.com/orgs/test/repos")

    @patch('client.requests.get')
    @patch('client.GithubOrgClient._public_repos_url', new_callable=unittest.mock.PropertyMock)
    def test_public_repos(self, mock_repos_url, mock_get):
        """Test public_repos method"""
        mock_repos_url.return_value = "https://api.github.com/orgs/test/repos"
        mock_get.return_value.json.return_value = [
            {"name": "repo1"}, {"name": "repo2"}
        ]
        client = GithubOrgClient("test_org")
        result = client.public_repos()
        self.assertEqual(result, ["repo1", "repo2"])
        mock_get.assert_called_once_with("https://api.github.com/orgs/test/repos")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method"""
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)
