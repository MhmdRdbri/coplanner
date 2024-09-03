from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from .models import WorkReport
from .serializers import WorkReportSerializer
from account.permissions import HasSpecialAccessPermission

class WorkReportViewSet(viewsets.ModelViewSet):
    queryset = WorkReport.objects.all()
    serializer_class = WorkReportSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.has_special_access:  # بررسی دسترسی ویژه
            return WorkReport.objects.all()
        return WorkReport.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, date=timezone.now().date())

    def create(self, request, *args, **kwargs):
        if WorkReport.objects.filter(user=request.user, date=timezone.now().date()).exists():
            return Response({"error": "You have already submitted a report for today."}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.date != timezone.now().date():
            return Response({"error": "You can only edit today's report."}, status=status.HTTP_403_FORBIDDEN)
        if not request.user.has_special_access:  # کاربر عادی نمی‌تواند تایید یا ویرایش کند
            return Response({"error": "Only users with special access can approve or edit reports."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.date != timezone.now().date() and not request.user.has_special_access:
            return Response({"error": "You can only edit today's report or you need special access."}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def approve(self, request, pk=None):
        report = self.get_object()
        if not request.user.has_special_access:
            return Response({"error": "Only users with special access can approve reports."}, status=status.HTTP_403_FORBIDDEN)
        if report.date >= timezone.now().date():
            report.is_approved = True
            report.save()
            return Response({"success": "Report has been approved."}, status=status.HTTP_200_OK)
        return Response({"error": "You can only approve today's report."}, status=status.HTTP_403_FORBIDDEN)
