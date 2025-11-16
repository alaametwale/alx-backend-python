#!/usr/bin/env python3
"""Module for testing utility functions: access_nested_map, get_json, memoize."""
import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from typing import Mapping, Sequence, Any, AnyStr

# افتراض أن الدالة access_nested_map موجودة في ملف utils.py
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """اختبارات الوحدة لدالة access_nested_map."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: Mapping, path: Sequence,
                               expected: Any) -> None:
        """اختبار الوصول إلى قيمة في خريطة متداخلة بمسارات صالحة."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        # الحالة 1: الخريطة فارغة والمفتاح المتوقع: 'a'.
        ({}, ("a",), "a"),
        # الحالة 2: المسار غير صحيح. المفتاح المفقود المتوقع هو 'b'.
        ({"a": 1}, ("a", "b"), "b"),
    ])
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence,
                                         expected_key: AnyStr) -> None:
        """
        اختبار أن الدالة access_nested_map تثير خطأ KeyError للمدخلات غير
        الصالحة، والتأكد من أن حجة الاستثناء (رسالة الخطأ) هي المفتاح
        المفقود المتوقع.
        """
        # استخدام مدير السياق assertRaises لاختبار إثارة KeyError.
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # التأكد من أن حجة الاستثناء الأولى تطابق المفتاح المفقود المتوقع
        self.assertEqual(cm.exception.args[0], expected_key)


class TestGetJson(unittest.TestCase):
    """اختبارات الوحدة لدالة utils.get_json باستخدام المزيفات."""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url: str, test_payload: Mapping,
                      mock_get: Mock) -> None:
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

        # 3. اختبار أن mock_get تم استدعاؤها مرة واحدة بالضبط مع test_url.
        mock_get.assert_called_once_with(test_url)

        # 4. اختبار أن الناتج يساوي test_payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """اختبارات الوحدة لديكور utils.memoize."""

    def test_memoize(self) -> None:
        """
        اختبار أن خاصية memoize تقوم بتخزين النتيجة مؤقتاً (Caching)
        عن طريق التأكد من أن الدالة a_method يتم استدعاؤها مرة واحدة فقط.
        """
        # تعريف الفئة الداخلية المطلوبة
        class TestClass:
            """فئة اختبار تحتوي على طريقة عادية وطريقة مزودة بديكور memoize."""

            def a_method(self) -> int:
                """طريقة يتم تزييفها واختبار عدد مرات استدعائها."""
                return 42

            @memoize
            def a_property(self) -> int:
                """خاصية تستخدم التخزين المؤقت، وتعتمد على a_method."""
                return self.a_method()

        # استخدام patch.object لتزييف a_method داخل TestClass
        with patch.object(TestClass, 'a_method',
                          return_value=42) as mock_a_method:
            # إنشاء كائن من الفئة
            test_instance = TestClass()

            # الاستدعاء الأول لـ a_property. يجب أن يستدعي a_method.
            result1 = test_instance.a_property

            # الاستدعاء الثاني لـ a_property. يجب أن يعيد النتيجة المخزنة مؤقتاً.
            result2 = test_instance.a_property

            # 1. اختبار أن النتيجة الصحيحة يتم إرجاعها (42)
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # 2. اختبار أن mock_a_method تم استدعاؤها مرة واحدة بالضبط
            mock_a_method.assert_called_once()