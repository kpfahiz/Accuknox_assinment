from django.db.models import Q
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import AllowAny,IsAuthenticated
from django.contrib.auth import get_user_model, authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from datetime import timedelta
from django.core.cache import cache

from .models import MyUser, FriendRequest, Friend
from .serializers import UserSerializer, FriendRequestSerializer, FriendListSerializer,SignupSerializer, LoginSerializer

User = get_user_model()

class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_200_OK)
    


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        keyword = self.request.query_params.get('q', None)
        if keyword:
            q = MyUser.objects.filter(Q(email__icontains=keyword))
            return q
        return MyUser.objects.none()
    
class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, to_user_id):
        user = request.user
        to_user = MyUser.objects.get(id=to_user_id)
        
        # Rate limiting
        requests = cache.get(f'friend_request_{user.id}', 0)
        if requests >= 3:
            return Response({"error": "You can only send 3 friend requests per minute."}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        friend_request, created = FriendRequest.objects.get_or_create(from_user=user, to_user=to_user)
        if not created:
            return Response({"error": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Increment request count
        cache.set(f'friend_request_{user.id}', requests + 1, timeout=60)

        return Response({"success": "Friend request sent."}, status=status.HTTP_201_CREATED)
class RespondToFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, request_id, response):
        try:
            friend_request = FriendRequest.objects.get(id=request_id, to_user=request.user)
            if response not in ['accept', 'reject']:
                return Response({"error": "Invalid response."}, status=status.HTTP_400_BAD_REQUEST)
            
            if response == 'accept':
                friend_request.status = 'accepted'
                Friend.make_friend(request.user, friend_request.from_user)
                Friend.make_friend(friend_request.from_user, request.user)
            elif response == 'reject':
                friend_request.status = 'rejected'
            
            friend_request.save()
            return Response({"success": f"Friend request {response}ed."}, status=status.HTTP_200_OK)
        except FriendRequest.DoesNotExist:
            return Response({"error": "Friend request not found."}, status=status.HTTP_404_NOT_FOUND)

class ListFriendsView(generics.ListAPIView):
    serializer_class = FriendListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friends = Friend.objects.filter(current_user=user).first()
        if friends:
            return friends.users.all()
        return MyUser.objects.none()

class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FriendRequest.objects.filter(to_user=self.request.user, status='pending')