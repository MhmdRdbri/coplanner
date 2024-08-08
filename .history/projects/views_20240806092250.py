from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Project
from .serializers import ProjectSerializer
from account.permissions import HasSpecialAccessPermission
from drf_spectacular.utils import extend_schema, extend_schema_view
from telegram import Bot
from django.conf import settings  # To get the bot token from settings if you prefer


# @extend_schema_view(
#     list=extend_schema(
#         description="List all projects or viewable projects based on user permissions.",
#     ),
#     retrieve=extend_schema(
#         description="Retrieve a project by ID. Only accessible by special access users and admins.",
#     ),
#     create=extend_schema(
#         description="Create a new project. Only accessible by admins.",
#     ),
#     update=extend_schema(
#         description="Update a project. Admins can update any project. Responsible persons can update their projects if not completed.",
#     ),
#     destroy=extend_schema(
#         description="Delete a project. Only accessible by admins.",
#     ),
# )

def send_telegram_message(chat_id, text):
    bot = Bot(token='7052281105:AAG5x1yux4ryfDzvfAmn1mwuVqa4LmBtKkk')
    bot.send_message(chat_id=chat_id, text=text)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, HasSpecialAccessPermission]

    def list(self, request):
        if not request.user.has_special_access and not request.user.is_staff:
            return Response({"error": "You do not have permission to view this page."}, status=status.HTTP_403_FORBIDDEN)
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        if not request.user.has_special_access and not request.user.is_staff:
            return Response({"error": "You do not have permission to view this page."}, status=status.HTTP_403_FORBIDDEN)
        queryset = self.get_queryset()
        project = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(project)
        return Response(serializer.data)

    def create(self, request):
        if not request.user.is_staff:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
        project = serializer.save()

        # Send notification to the user
        try:
            chat_id = request.user.telegram_chat_id  # Replace with the correct field
            bot_token = 'YOUR_BOT_TOKEN_HERE'  # Replace with your bot token or get it from settings
            bot = Bot(token=bot_token)
            message = f"Project '{project.name}' has been created."
            bot.send_message(chat_id=chat_id, text=message)
        except Exception as e:
            logging.error(f"Failed to send Telegram message: {e}")

        return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        project = get_object_or_404(Project, pk=pk)
        if request.user.is_staff:
            serializer = self.serializer_class(project, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.user == project.responsible_person and project.status != 'completed':
            serializer = self.serializer_class(project, data=request.data, partial=True)
            if 'status' in serializer.validated_data:
                serializer.validated_data.pop('status')
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        """
        Delete a project. Only accessible by admins.
        """
        if not request.user.is_staff:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        queryset = self.get_queryset()
        project = get_object_or_404(queryset, pk=pk)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MyProjectsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(responsible_person=self.request.user)

    def update(self, request, pk=None):
        """
        Update a project assigned to the currently authenticated user. 
        User cannot update status if the project is completed.
        Dont show the project status field in this part to user in front.
        """
        project = get_object_or_404(self.get_queryset(), pk=pk)
        if project.status == 'completed':
            return Response({"error": "You cannot edit a completed project."}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(project, data=request.data, partial=True)
        # Prevent responsible person from changing the status
        if 'status' in serializer.validated_data:
            serializer.validated_data.pop('status')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)