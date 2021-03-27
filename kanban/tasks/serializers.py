from rest_framework import serializers
from tasks.models import Task
from accounts.serializers import AccountsSerializer
# from django.contrib.auth.hashers import make_password


class TaskSerializer(serializers.HyperlinkedModelSerializer):  # new one
    # AFTER USING META
    # owner = serializers.ReadOnlyField(source='owner.username')
    owner = AccountsSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'url', 'owner', 'created', 'title',
                  'details', 'status', 'due_date']

    def create(self, validated_data):
        return Task.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.details = validated_data.get('details', instance.details)
        instance.owner = validated_data.get('owner', instance.owner)
        instance.save()

        return instance
