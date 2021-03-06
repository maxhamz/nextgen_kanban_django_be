# from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
# from rest_framework.reverse import reverse
# from rest_framework.decorators import api_view   # for root
from accounts.serializers import AccountsSerializer
from django.http import Http404
from django.contrib.auth.models import User

# Create your views here.
# FOR ACCOUNT VIEW
# Create your views here.


class AccountsList(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = AccountsSerializer(
            users,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = AccountsSerializer(
            data=request.data,
            context={'request': request}
        )
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountsDetail(APIView):
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        serializer = AccountsSerializer(user, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        user = self.get_user(pk)
        serializer = AccountsSerializer(
            user,
            data=request.data,
            context={'request': request}
        )  # level 2
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_user(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  # level 2
