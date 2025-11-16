import unittest
from parameterized import parameterized
from typing import Mapping, Sequence, Any

# افتراض أن الدالة access_nested_map موجودة في ملف utils.py
from utils import access_nested_map

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
    def test_access_nested_map_exception(self, nested_map: Mapping, path: Sequence, expected_key: str) -> None:
        """
        اختبار أن الدالة access_nested_map تثير خطأ KeyError للمدخلات غير الصالحة،
        والتأكد من أن حجة الاستثناء (رسالة الخطأ) هي المفتاح المفقود المتوقع.
        
        Args:
            nested_map (Mapping): القاموس المتداخل للاختبار.
            path (Sequence): تسلسل المفاتيح للوصول إلى القيمة.
            expected_key (str): المفتاح الذي من المتوقع أن يثير خطأ KeyError.
        """
        # استخدام مدير السياق assertRaises لاختبار إثارة KeyError
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        
        # التأكد من أن حجة الاستثناء الأولى (وهي رسالة الخطأ) تطابق المفتاح المفقود المتوقع
        self.assertEqual(cm.exception.args[0], expected_key,
                         f"رسالة استثناء KeyError غير صحيحة. المتوقع: '{expected_key}', الفعلي: {cm.exception.args[0]}")

# ملاحظة: يجب أن يظل ملف utils.py كما هو لإنجاح الاختبار