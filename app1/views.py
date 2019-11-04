from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly

@csrf_exempt
@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticatedOrReadOnly, ])
# @permission_classes([AllowAny, ])
@permission_classes([IsAuthenticated, ])
def sample_api(request):

    print(request.user)
    print(request.user.is_authenticated)
    print(request.user.username)
    return HttpResponse("This is sample API response." + request.user.username)
