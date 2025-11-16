#!/usr/bin/env python3
"""
Test for client.py
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient class"""

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected, mock_get_json):
        """Test GithubOrgClient.org returns correct data"""
        mock_get_json.return_value = expected
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected)
        mock_get_json.assert_called_once()

    @patch("client.GithubOrgClient.org", new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """Test _public_repos_url property"""
        mock_org.return_value = {"repos_url": "http://fake.url"}
        client = GithubOrgClient("org_name")
        self.assertEqual(client._public_repos_url, "http://fake.url")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test public_repos returns expected list"""
        repos_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = repos_payload
        client = GithubOrgClient("org_name")
        self.assertEqual(client.public_repos(), ["repo1", "repo2"])

    @patch("client.get_json")
    def test_public_repos_with_license(self, mock_get_json):
        """Test public_repos with license filter"""
        repos_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}}
        ]
        mock_get_json.return_value = repos_payload
        client = GithubOrgClient("org_name")
        self.assertEqual(client.public_repos("apache-2.0"), ["repo1"])
        self.assertEqual(client.public_repos("mit"), ["repo2"])
        self.assertEqual(client.public_repos("bsd"), [])

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method"""
        client = GithubOrgClient("org_name")
        self.assertEqual(client.has_license(repo, license_key), expected)
