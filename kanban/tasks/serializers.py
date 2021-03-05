from rest_framework import serializers
from tasks.models import Task
from django.contrib.auth.models import User
# from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # of course, when accessing user's post from user, we gotta make it
    # read only to easier maintain!
    
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


class TaskSerializer(serializers.HyperlinkedModelSerializer):  # new one
    # AFTER USING META
    # owner = serializers.ReadOnlyField(source='owner.username')
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.details = validated_data.get('details', instance.details)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()

        return instance
