#!/usr/bin/env python3
"""
Unit tests for GithubOrgClient
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized

# تأكد أن client.py موجود في نفس المجلد أو عدّل المسار إذا كان مختلف
from client import GithubOrgClient  

class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")  # Patch على المكان الذي تُستخدم فيه get_json داخل client.py
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected value"""
        # القيمة المتوقعة التي سترجعها الدالة الوهمية
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        # إنشاء كائن العميل
        client = GithubOrgClient(org_name)
        result = client.org()

        # تحقق من القيمة المرجعة
        self.assertEqual(result, expected)

        # تحقق من أن get_json استُدعيت مرة واحدة بالوسيط الصحيح
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

if __name__ == "__main__":
    unittest.main()
