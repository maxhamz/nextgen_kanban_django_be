from rest_framework import serializers
from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password


class AccountsSerializer(serializers.HyperlinkedModelSerializer):
    # of course, when accessing user's post from user, we gotta make it
    # read only to easier maintain !   
    # we need create & update serializer for hashing passwords
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    tasks = serializers.HyperlinkedRelatedField(many=True, 
                                                view_name='task-detail',
                                                read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'tasks', 'owner']
        read_only_fields = ['is_staff', 'is_superuser']
        write_only_fields = ['password']
        # fields = '__all__'
