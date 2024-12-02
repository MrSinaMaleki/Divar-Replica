# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework.exceptions import AuthenticationFailed
#
#
# class CookieJWTAuthentication(JWTAuthentication):
#     def get_raw_token(self, request):
#         raw_token = str(request).split(" ")[1]
#
#
#         if not raw_token:
#             raise AuthenticationFailed('Token not found in cookies')
#
#         return raw_token