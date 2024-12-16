from django.contrib.auth import get_user_model
from django_auth_ldap.backend import LDAPBackend

UserModel = get_user_model()

class ExistingUserLDAPBackend(LDAPBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check if the user exists in the local database
        try:
            UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            # If user does not exist in the database, skip LDAP and stop authentication
            return None
        
        # If user exists, proceed with LDAP authentication
        return super().authenticate(request, username=username, password=password, **kwargs)
