#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient  # تأكد أن client.py موجود في نفس المجلد

class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient.org method"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")  # Patch get_json في مكان استخدامها
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected value"""
        # القيمة المتوقعة التي سترجعها الدالة الوهمية
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        # إنشاء كائن العميل
        client = GithubOrgClient(org_name)
        result = client.org()

        # تحقق أن الدالة أعادت القيمة المتوقعة
        self.assertEqual(result, expected)

        # تحقق أن get_json استُدعيت مرة واحدة بالوسيط الصحيح
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

if __name__ == "__main__":
    unittest.main()

