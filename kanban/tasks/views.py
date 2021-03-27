from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view   # for root
from tasks.permissions import IsOwnerOrReadOnly
from tasks.models import Task
from tasks.serializers import TaskSerializer
from django.http import Http404


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'accounts': reverse('accounts-list', request=request, format=format),
        'tasks': reverse('task-list', request=request, format=format)
    })


# Create your views here.
class TaskList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        tasks = Task.objects.all()
        serializer = TaskSerializer(
            tasks,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = TaskSerializer(
            data=request.data,
            context={'request': request}
        )
        if (serializer.is_valid()):
            serializer.save(owner=self.request.user)  # set current user?
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsOwnerOrReadOnly
    ]

    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(task, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        task = self.get_object(pk)
        serializer = TaskSerializer(
            task,
            data=request.data,
            context={'request': request}
        )  # level 2
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        task = self.get_object(pk)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # level 2
