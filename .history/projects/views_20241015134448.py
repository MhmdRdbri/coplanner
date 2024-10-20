from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Project
from .serializers import ProjectSerializer
from account.permissions import HasSpecialAccessPermission
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        description="List all projects or viewable projects based on user permissions.",
    ),
    retrieve=extend_schema(
        description="Retrieve a project by ID. Only accessible by special access users and admins.",
    ),
    create=extend_schema(
        description="Create a new project. Only accessible by admins.",
    ),
    update=extend_schema(
        description="Update a project. Admins can update any project. Responsible persons can update their projects if not completed.",
    ),
    destroy=extend_schema(
        description="Delete a project. Only accessible by admins.",
    ),
)

class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.has_special_access or self.request.user.is_staff:
            return Project.objects.all()
        return Project.objects.filter(team_members=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        project = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(project)
        return Response(serializer.data)

    def create(self, request):
        # Only allow project creation for users with special access or staff
        if not request.user.has_special_access and not request.user.is_staff:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        # Allow staff and special access users to update any project
        if request.user.has_special_access or request.user.is_staff:
            serializer = self.serializer_class(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Regular users can only view projects they are part of, no update allowed
        return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        # Only allow project deletion for users with special access or staff
        if not request.user.has_special_access and not request.user.is_staff:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContentProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ContentProject
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.has_special_access or self.request.user.is_staff:
            return Project.objects.all()
        return Project.objects.filter(team_members=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = self.get_queryset()
        project = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(project)
        return Response(serializer.data)

    def create(self, request):
        if not request.user.has_special_access and not request.user.is_staff:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        if request.user.has_special_access or request.user.is_staff:
            serializer = self.serializer_class(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        if not request.user.has_special_access and not request.user.is_staff:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        project = get_object_or_404(Project, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)