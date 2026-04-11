from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from .serializer import RegisterSerializer, LoginSerializer
from cart.utils import merge_guest_cart_to_user
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Optionally return token on register
        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "User registered successfully",
            "user_id": user.id,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']

    # 🔥 ensure session exists (important!)
    if not request.session.session_key:
        request.session.create()

    # 🔥 Merge guest cart into user cart
    merge_guest_cart_to_user(user, request.session.session_key)

    # 🔥 Generate JWT tokens
    

    refresh = RefreshToken.for_user(user)

    return Response({
        "user_id": user.id,
        "access": str(refresh.access_token),
        "refresh": str(refresh)
    }, status=status.HTTP_200_OK)


@api_view(["POST"])
def logout_user(request):
    """
    Blacklist refresh token (JWT)
    Expects: { "refresh": "<refresh_token>" }
    """
    try:
        refresh_token = request.data["refresh"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
