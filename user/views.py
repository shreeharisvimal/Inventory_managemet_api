from rest_framework.views import APIView
from .models import User
from django.core.cache import cache
from rest_framework import permissions, status
from rest_framework_simplejwt.tokens import RefreshToken 
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer


# Create your views here.

class MyRefreshTokenObtainPairSerializer(TokenRefreshSerializer):
	def __init__(self, *args, **kwargs):
		request = kwargs.pop('request', None)
		super().__init__(*args, **kwargs)

class MyRefreshTokenObtainPairView(TokenRefreshView):
	serializer_class = MyRefreshTokenObtainPairSerializer


class LogoutView(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		try:
			refresh_token = request.data.get('refresh_token')
			if not refresh_token:
				return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

			token = RefreshToken(refresh_token)
			token.blacklist()
			return Response(status=status.HTTP_205_RESET_CONTENT)
		except Exception as e:
			return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserAuths(APIView):

	def post(self, request):
		data = request.data
		email = data.get('email')
		password = data.get('password')

		if email is None or password is None:
			return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

		try:
			user = User.objects.get(email=email)
			if user.check_password(password):
				token = user.tokens()
				return Response({
					'access': token['AccessToken'],
					'refresh': token['RefreshToken'],
				}, status=status.HTTP_200_OK)
			else:
				return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

		except User.DoesNotExist:
			user = User.objects.create_user(email=email, password=password)
			token = user.tokens()
			return Response({
				'access': token['AccessToken'],
				'refresh': token['RefreshToken'],
			}, status=status.HTTP_201_CREATED)

		except Exception as e:
			return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
