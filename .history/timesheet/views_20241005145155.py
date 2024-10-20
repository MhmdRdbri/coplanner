from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from .models import Timesheet, Pause
from .serializers import TimesheetSerializer, PauseSerializer
from datetime import timedelta
from django.db.models import Sum

class TimesheetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def start(self, request):
        today = timezone.now().date()
        user = request.user

        if Timesheet.objects.filter(user=user, date=today).exists():
            return Response({"detail": "You have already started a timesheet today."}, status=status.HTTP_400_BAD_REQUEST)

        timesheet = Timesheet.objects.create(user=user, start_time=timezone.now(), date=today)
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

        # Get the current time
        now = timezone.now()

        # Filter based on the period parameter
        if period == 'day':
            # Filter for timesheets created today
            queryset = queryset.filter(date=now.date())
        elif period == 'week':
            # Calculate the start of the current week (assuming week starts on Monday)
            start_of_week = now - timedelta(days=now.weekday())
            queryset = queryset.filter(date__gte=start_of_week.date(), date__lte=now.date())
        elif period == 'month':
            # Filter for the current month
            queryset = queryset.filter(date__year=now.year, date__month=now.month)

        # If no period is specified, return all timesheets
        if period not in ['day', 'week', 'month']:
            return Response({"detail": "Please provide a valid period: day, week, or month."}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total worked time for the filtered timesheets
        total_worked_time = timedelta()
        for timesheet in queryset:
            total_worked_time += timesheet.total_worked_time

        # Serialize the data
        serialized_data = TimesheetSerializer(queryset, many=True).data

        # Add total worked time to the response
        return Response({
            "timesheets": serialized_data,
            "total_worked_time": str(total_worked_time)
        })

    def list_for_admin(self, request):
        # Ensure the user has special access (modify this condition as per your app's rules)
        if not request.user.has_special_access:
            return Response({"detail": "You do not have permission to view this data."}, status=status.HTTP_403_FORBIDDEN)

        period = request.query_params.get('period')  # Default period is 'day'
        queryset = Timesheet.objects.all()

        # Filter based on period (day, week, or month)
        if period == 'day':
            queryset = queryset.filter(date=timezone.now().date())
        elif period == 'week':
            start_of_week = timezone.now().date() - timedelta(days=timezone.now().date().weekday())
            queryset = queryset.filter(date__gte=start_of_week)
        elif period == 'month':
            queryset = queryset.filter(date__month=timezone.now().date().month)

        # Calculate total worked time for all users for this period
        total_worked_time = queryset.aggregate(Sum('total_worked_time'))['total_worked_time__sum'] or timedelta()

        return Response({
            'timesheets': TimesheetSerializer(queryset, many=True).data,
            'total_worked_time': str(total_worked_time)  # Format timedelta as string
        })