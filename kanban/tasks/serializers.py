from rest_framework import serializers
from tasks.models import Task
from django.contrib.auth.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # of course, when accessing user's post from user, we gotta make it
    # read only to easier maintain!
    tasks = serializers.HyperlinkedRelatedField(many=True, 
                                                view_name='task-detail',
                                                read_only=True)
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'tasks', 'owner']
        # fields = '__all__'


class TaskSerializer(serializers.HyperlinkedModelSerializer):  # new one
    # AFTER USING META
    owner = serializers.ReadOnlyField(source='owner.username')

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
