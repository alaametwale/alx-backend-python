
from django.http import JsonResponse

def index(request):
    return JsonResponse({'message': 'Chats API working'})
