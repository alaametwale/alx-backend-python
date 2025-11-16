#!/usr/bin/env python3
"""Test module for client.py"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
    def test_org(self, org_name, expected_payload, mock_get_json):
        """Test that GithubOrgClient.org returns correct data"""
        mock_get_json.return_value = expected_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)
        mock_get_json.assert_called_once()

    @patch("client.get_json", return_value=[{"name": "repo1"}, {"name": "repo2"}])
    def test_public_repos(self, mock_get_json):
        """Integration test for public_repos"""
        client = GithubOrgClient("org")
        expected = ["repo1", "repo2"]
        self.assertEqual(client.public_repos(), expected)
        mock_get_json.assert_called_once()

    @patch("client.get_json")
    def test_public_repos_with_license(self, mock_get_json):
        """Integration test for public_repos with license filtering"""
        repos_payload = [
            {"name": "repo1", "license": {"key": "apache-2.0"}},
            {"name": "repo2", "license": {"key": "mit"}},
            {"name": "repo3", "license": {"key": "apache-2.0"}}
        ]
        mock_get_json.return_value = repos_payload
        client = GithubOrgClient("org")
        expected = ["repo1", "repo3"]
        self.assertEqual(client.public_repos(license="apache-2.0"), expected)
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """Unit test for has_license method"""
        client = GithubOrgClient("org")
        self.assertEqual(client.has_license(repo, license_key), expected)
