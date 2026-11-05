from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r"users", views.UserViewSet, basename="user")
router.register(r"profiles", views.MemberProfileViewSet, basename="profile")

urlpatterns = [
    path("me/", views.CurrentUserView.as_view(), name="auth-me"),
    path("logout/", views.LogoutView.as_view(), name="auth-logout"),
    path("member-check/", views.MemberAreaCheckView.as_view(), name="auth-member-check"),
    path("pending/", views.PendingAccountsView.as_view(), name="auth-pending"),
    path("approve/<int:pk>/", views.ApproveAccountView.as_view(), name="auth-approve"),
    path("reject/<int:pk>/", views.RejectAccountView.as_view(), name="auth-reject"),
    path("", include(router.urls)),
]
