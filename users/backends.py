from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


# extending the default django ModelBackend to be able the override the default authenticate() to help authenticate
# users for the login view This implementation takes a request object and username and password as input arguments.
# It retrieves the user model using get_user_model(), which returns the model class that is currently set as the user
# model. Then it queries the user model to find a user with the provided username. If a user is found, it checks the
# provided password using the check_password() method of the user model. If the password is correct, it returns the
# user object. If the password is incorrect or no user is found, it returns None.
class CustomModelBackend(ModelBackend):
    # overriding the authentication backend
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return None
        if user.check_password(password):
            return user
        return None
