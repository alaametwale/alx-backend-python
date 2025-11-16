import unittest
from unittest.mock import patch
from parameterized import parameterized

# افترض أن GithubOrgClient موجود في module باسم client
from client import GithubOrgClient  # عدّل المسار وفق مشروعك

class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")  # عدّل المسار إلى المكان الذي تُعرّف فيه get_json
    def test_org(self, org, mock_get_json):
        # ترتيب: نحدد القيمة المرجوعة من get_json
        expected = {"login": org}
        mock_get_json.return_value = expected

        # إنشاء الكائن واختبار الخاصية/الدالة التي تُعيد org
        github_org = GithubOrgClient(org)

        # إذا كانت org خاصية (property) فاستدعها بدون أقواس
        result = github_org.org  # أو github_org.org() إذا كانت دالة

        # التحقق من أن get_json دُعيت مرة واحدة وبالحجة الصحيحة
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org}")

        # التأكيد أن الناتج يساوي القيمة المفترضتها المحاكاة
        self.assertEqual(result, expected)
