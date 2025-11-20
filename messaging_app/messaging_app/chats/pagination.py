~~~{"variant":"standard","title":"chats/pagination.py with MessagePagination","id":"59022"}
"""
chats/pagination.py
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,  # Total messages
            'page_number': self.page.number,
            'page_size': self.page.paginator.per_page,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
"""
~~~

### ✅ ملاحظات:

1. `page.paginator.count` يعطي العدد الكلي للرسائل، وهو ما تطلبه الشيكات.  
2. يمكنك استخدام `page_size_query_param` لتغيير عدد الرسائل في كل صفحة ديناميكيًا عبر query params.  
3. هذا الملف جاهز للاستخدام مباشرة مع `MessageViewSet` في `chats/views.py`.  

بعد إنشاء الملف:

```bash
git add messaging_app/chats/pagination.py
git commit -m "Add MessagePagination with total count for DRF"
git push origin main
``` 

هذا سيغطي الشيك المتعلق بـ **pagination** تمامًا.  

إذا أحببت، أقدر أجهز لك أيضًا **MessageFilter** جاهز لـ `chats/filters.py` ليتوافق مع التصفية حسب المستخدمين ونطاق الوقت. هل تريد أن أفعل ذلك الآن؟
