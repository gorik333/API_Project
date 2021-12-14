from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import TestSerializer
from api.views import get_client_ip
from api.utils import save_request
from api.models import UserRequest, UserIP


class RestEndpoint(APIView):
    permission_classes = (AllowAny,)
    serializer_class = TestSerializer

    def get(self, request):
        requests = UserRequest.objects.filter(ip__ip=get_client_ip(request)).values('email', 'password',
                                                                                    'first_name', 'last_name')

        return Response({'requests': requests}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user_ip, created = UserIP.objects.get_or_create(ip=get_client_ip(request))

            save_request(user_ip, serializer.data)

            content = {
                'email': serializer.data['email'],
                'password': serializer.data['password'],
                'first_name': serializer.data['first_name'],
                'last_name': serializer.data['last_name'],
            }

            return Response(content, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
