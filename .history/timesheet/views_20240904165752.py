from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Timesheet, Pause
from .serializers import TimesheetSerializer, PauseSerializer
from datetime import timedelta

class TimesheetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def start(self, request):
        today = timezone.now().date()
        user = request.user

        if Timesheet.objects.filter(user=user, date=today).exists():
            return Response({"detail": "You have already started a timesheet today."}, status=status.HTTP_400_BAD_REQUEST)

        timesheet = Timesheet.objects.create(user=user, start_time=timezone.now())
        return Response(TimesheetSerializer(timesheet).data)

    def pause(self, request):
        today = timezone.now().date()
        user = request.user

        try:
            timesheet = Timesheet.objects.get(user=user, date=today, end_time__isnull=True)
        except Timesheet.DoesNotExist:
            return Response({"detail": "No active timesheet found."}, status=status.HTTP_400_BAD_REQUEST)

        if timesheet.pauses.filter(resume_time__isnull=True).exists():
            return Response({"detail": "You have already paused your timesheet."}, status=status.HTTP_400_BAD_REQUEST)

        pause = Pause.objects.create(timesheet=timesheet, pause_time=timezone.now())
        return Response(PauseSerializer(pause).data)

    def resume(self, request):
        today = timezone.now().date()
        user = request.user

        try:
            timesheet = Timesheet.objects.get(user=user, date=today, end_time__isnull=True)
        except Timesheet.DoesNotExist:
            return Response({"detail": "No active timesheet found."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            pause = timesheet.pauses.get(resume_time__isnull=True)
        except Pause.DoesNotExist:
            return Response({"detail": "No paused timesheet found."}, status=status.HTTP_400_BAD_REQUEST)

        pause.resume_time = timezone.now()
        pause.save()

        # Update total worked time
        timesheet.total_worked_time += pause.resume_time - pause.pause_time
        timesheet.save()

        return Response(PauseSerializer(pause).data)

    def stop(self, request):
        today = timezone.now().date()
        user = request.user

        try:
            timesheet = Timesheet.objects.get(user=user, date=today, end_time__isnull=True)
        except Timesheet.DoesNotExist:
            return Response({"detail": "No active timesheet found."}, status=status.HTTP_400_BAD_REQUEST)

        if timesheet.pauses.filter(resume_time__isnull=True).exists():
            return Response({"detail": "You need to resume before stopping."}, status=status.HTTP_400_BAD_REQUEST)

        timesheet.end_time = timezone.now()

        # Calculate total worked time considering the pauses
        total_worked_today = timesheet.end_time - timesheet.start_time - timesheet.total_worked_time
        timesheet.total_worked_time = total_worked_today

        timesheet.save()
        return Response(TimesheetSerializer(timesheet).data)

    def list(self, request):
        user = request.user
        period = request.query_params.get('period')
        queryset = Timesheet.objects.filter(user=user)

        if period == 'day':
            queryset = queryset.filter(date=timezone.now().date())
        elif period == 'week':
            start_of_week = timezone.now().date() - timedelta(days=timezone.now().date().weekday())
            queryset = queryset.filter(date__gte=start_of_week)
        elif period == 'month':
            queryset = queryset.filter(date__month=timezone.now().date().month)

        return Response(TimesheetSerializer(queryset, many=True).data)

    def list_for_admin(self, request):
        if not request.user.has_special_access:
            return Response({"detail": "You do not have permission to view this data."}, status=status.HTTP_403_FORBIDDEN)

        period = request.query_params.get('period')
        queryset = Timesheet.objects.all()

        if period == 'day':
            queryset = queryset.filter(date=timezone.now().date())
        elif period == 'week':
            start_of_week = timezone.now().date() - timedelta(days=timezone.now().date().weekday())
            queryset = queryset.filter(date__gte=start_of_week)
        elif period == 'month':
            queryset = queryset.filter(date__month=timezone.now().date().month)

        return Response(TimesheetSerializer(queryset, many=True).data)
