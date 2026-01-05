import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient  # تأكد أن client.py موجود ويحتوي على GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test GithubOrgClient.org method"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch("client.get_json")  # نستخدم patch كديكور
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the expected value"""

        # إعداد القيمة المتوقعة ليُرجعها get_json
        expected = {"login": org_name}
        mock_get_json.return_value = expected

        client = GithubOrgClient(org_name)
        result = client.org()

        # تحقق من أن الدالة أعادت القيمة المتوقعة
        self.assertEqual(result, expected)

        # تحقق أن get_json استُدعيت مرة واحدة مع الرابط الصحيح
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")
