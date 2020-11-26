from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()

# serializer to create user
class CreateUserSerializer(serializers.ModelSerializer):
    # enabling list of strings through serializer
    groups = serializers.ListField(child=serializers.CharField(max_length=500))

    class Meta:
        model = User
        fields = ('email', 'name', 'password', 'groups')
        extra_kwargs = {'password': {'write_only': True}}

    # create method to create and add user in group
    def create(self, validated_data):
        groups_data = validated_data.pop('groups')
        for i in groups_data:
            if 'admin' in i:
                user = User.objects.create_superuser(**validated_data)
            else:
                user = User.objects.create_user(**validated_data)
            group_obj, created = Group.objects.get_or_create(name=i)
            user.groups.add(group_obj.id)
        return user

# to serializer groups
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name', )

# serializer to get user
class GetUserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(read_only=True, many=True)
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'groups')
