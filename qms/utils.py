from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import UntypedToken


def fetch_jwttoken_claims(request):
    jwt_authenticator = JWTAuthentication()
    auth_header = jwt_authenticator.get_header(request)
    raw_token = jwt_authenticator.get_raw_token(auth_header)
    token_claims = UntypedToken(token=raw_token)
    return token_claims.payload