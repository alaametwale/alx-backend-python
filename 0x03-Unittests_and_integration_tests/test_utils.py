#!/usr/bin/env python3
import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from typing import Mapping, Sequence, Any, AnyStr

# افتراض أن الدالة access_nested_map موجودة في ملف utils.py
from utils import access_nested_map, get_json

class TestAccessNestedMap(unittest.TestCase):
    """اختبارات الوحدة لدالة access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence, expected: Any) -> None:
        """اختبار الوصول إلى قيمة في خريطة متداخلة بمسارات صالحة."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        # الحالة 1: الخريطة فارغة والمفتاح مفقود. المفتاح المفقود المتوقع هو 'a'.
        ({}, ("a",), "a"),
        # الحالة 2: المسار يؤدي إلى قيمة غير قاموسية والمفتاح التالي مفقود. المفتاح المفقود المتوقع هو 'b'.
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence, expected_key: AnyStr) -> None:
        """
        اختبار أن الدالة access_nested_map تثير خطأ KeyError للمدخلات غير الصالحة،
        والتأكد من أن حجة الاستثناء (رسالة الخطأ) هي المفتاح المفقود المتوقع.
        """
        # استخدام مدير السياق assertRaises لاختبار إثارة KeyError
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        
        # التأكد من أن حجة الاستثناء الأولى (وهي رسالة الخطأ) تطابق المفتاح المفقود المتوقع
        self.assertEqual(cm.exception.args[0], expected_key,
                         f"رسالة استثناء KeyError غير صحيحة. المتوقع: '{expected_key}', الفعلي: {cm.exception.args[0]}")

class TestGetJson(unittest.TestCase):
    """اختبارات الوحدة لدالة utils.get_json باستخدام المزيفات."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url: str, test_payload: Mapping, mock_get: Mock) -> None:
        """
        اختبار أن دالة get_json ترجع الحمولة المتوقعة (test_payload)
        وأن requests.get يتم استدعاؤه مرة واحدة بعنوان URL الصحيح (test_url).
        """
        # 1. إعداد كائن Mock الذي سيعيده requests.get
        # يجب أن يحتوي الكائن المُعاد على طريقة json() تُرجع test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # 2. استدعاء الدالة المراد اختبارها
        result = get_json(test_url)

        # 3. اختبار أن طريقة get الساخرة قد تم استدعاؤها مرة واحدة بالضبط مع test_url
        mock_get.assert_called_once_with(test_url)

        # 4. اختبار أن الناتج يساوي test_payload
        self.assertEqual(result, test_payload)