from .models import Photographer,User
from rest_framework import serializers
# creates classes that takes our model objects and makes it a json data, its more of like the modelForm

class UserSerializer(serializers.ModelSerializer):
    """
    Serializes basic user information for nested use in related serializers.

    This serializer is used to represent Django's built-in User model fields
    such as ID, username, and personal details. It is typically used as a nested
    serializer in other models like Photographer.

    Fields:
        id (IntegerField): Unique identifier for the user.
        username (CharField): Username used for authentication.
        email (EmailField): User's email address.
        first_name (CharField): First name of the user.
        last_name (CharField): Last name of the user.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class PhotographerSerializer(serializers.ModelSerializer):
    """
    Serializes photographer profile details, including related user information and a computed full name.

    This serializer includes a nested read-only `UserSerializer` to display user details
    and uses a SerializerMethodField to compute and expose the photographer's full name
    by combining the first and last names or falling back to the username.

    Fields:
        user (UserSerializer): Nested user information (read-only).
        full_name (CharField): Computed full name from the related user.
        email (EmailField): Photographer's email address.
        bio (CharField): Short biography or profile description.
        phone_number (CharField): Contact number of the photographer.
        specialization (CharField): Area of focus (e.g. weddings, commercial, etc.).
        profession (CharField): Photographer's professional title or role.
    """
    user_details = UserSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),  write_only=True)
    full_name = serializers.SerializerMethodField() #This tells DRF that the value of full_name is not a model field. It’ll be provided using a custom method, in this case get_full_name().
    # user_email = serializers.EmailField(write_only=True)
    # user_fName= serializers.CharField(write_only=True)
    # user_lName =serializers.CharField(wrute_only=True)

    class Meta:
        model = Photographer
        fields = ['id', 'user','user_details', 'full_name', 'bio','phone_number', 'specialization','profession']
        read_only_fields = ['id']
    
    def get_full_name(self,obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
