#!/usr/bin/env python3
"""Unit tests for client.py"""
import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected, mock_get_json):
        """Test that GithubOrgClient.org returns correct data"""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once()

    @patch("client.GithubOrgClient.org", new_callable=property)
    def test_public_repos(self, mock_org):
        """Test GithubOrgClient.public_repos returns expected list"""
        mock_org.return_value = {"repos_url": "http://api.github.com/orgs/test/repos"}
        with patch("client.get_json") as mock_get_json:
            mock_get_json.return_value = [
                {"name": "repo1"},
                {"name": "repo2"}
            ]
            client = GithubOrgClient("test_org")
            repos = client.public_repos()
            self.assertEqual(repos, ["repo1", "repo2"])
            mock_get_json.assert_called_once_with("http://api.github.com/orgs/test/repos")

    @patch("client.GithubOrgClient.org", new_callable=property)
    def test_public_repos_url(self, mock_org):
        """Test GithubOrgClient._public_repos_url with mocked org property"""
        mock_org.return_value = {"repos_url": "http://api.github.com/orgs/test/repos"}
        client = GithubOrgClient("test_org")
        se
