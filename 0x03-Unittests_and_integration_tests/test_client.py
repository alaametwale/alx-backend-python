#!/usr/bin/env python3
"""Tests for GithubOrgClient methods."""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns correct data"""
        expected = {"org": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, expected)

    def test_public_repos_url(self):
        """Test GithubOrgClient._public_repos_url with mocked org property"""
        payload = {"repos_url": "http://some_url.com"}
        client = GithubOrgClient("test_org")

        with patch.object(GithubOrgClient, "org", new_callable=unittest.mock.PropertyMock) as mock_org:
            mock_org.return_value = payload
            result = client._public_repos_url()

        self.assertEqual(result, "http://some_url.com")

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test GithubOrgClient.public_repos returns expected list"""
        # إعداد payload وهمي للدوال
        test_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = test_payload

        client = GithubOrgClient("test_org")

        # Mock _public_repos_url لارجاع URL وهمي
        with patch.object(GithubOrgClient, "_public_repos_url", return_value="http://some_url.com") as mock_url:
            repos = client.public_repos()

        # التحقق من النتائج
        self.assertEqual(repos, ["repo1", "repo2"])

        # التأكد من أن الدالتين تم استدعاؤهما مرة واحدة
        mock_get_json.assert_called_once()
        mock_url.assert_called_once()
