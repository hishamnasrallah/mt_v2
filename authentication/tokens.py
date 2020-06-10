from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken


class VScribeToken(AccessToken):
    token_type = 'vscribe'
    lifetime = api_settings.ACCESS_TOKEN_LIFETIME

    def set_jti(self):
        pass

    def verify(self):
        # Verify Token's Expiration
        self.check_exp()
        # Verify Token's Type
        self.verify_token_type()


class VScribeRefreshToken(RefreshToken):
    token_type = 'vscribe_refresh'
    lifetime = api_settings.REFRESH_TOKEN_LIFETIME

    def set_jti(self):
        pass

    @property
    def access_token(self):
        access = VScribeToken()
        access.set_exp(from_time=self.current_time)
        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value
        return access

    def verify(self):
        self.check_exp()
        self.verify_token_type()





