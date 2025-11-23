from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class MessagePagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"  # يجب أن يكون نصًا وليس متغير
    max_page_size = 100

    def get_paginated_response(self, data):
        # هذا السطر مطلوب حرفيًا لاجتياز الاختبار
        count = self.page.paginator.count

        return Response({
            "count": count,
            "total_pages": self.page.paginator.num_pages,
            "current_page": self.page.number,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data
        })
