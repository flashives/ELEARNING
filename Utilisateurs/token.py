from django.contrib.auth.tokens import PasswordResetTokenGenerator

class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return f"{user.pk}{timestamp}{user.is_active}"

generate_token = AppTokenGenerator()