from django.urls import path
from .views import SignupView, LoginView, UserSearchView, SendFriendRequestView, RespondToFriendRequestView, ListFriendsView, ListPendingRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='user-search'),
    path('friend-request/send/<int:to_user_id>/', SendFriendRequestView.as_view(), name='send-friend-request'),
    path('friend-request/respond/<int:request_id>/<str:response>/', RespondToFriendRequestView.as_view(), name='respond-friend-request'),
    path('friends/', ListFriendsView.as_view(), name='list-friends'),
    path('friend-requests/pending/', ListPendingRequestsView.as_view(), name='list-pending-requests'),
]