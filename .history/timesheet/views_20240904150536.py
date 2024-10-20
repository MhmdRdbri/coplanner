from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Sum, Q
from .models import TimeSheet
from .serializers import TimeSheetSerializer
from datetime import timedelta

class TimeSheetStartView(generics.CreateAPIView):
    serializer_class = TimeSheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        today = timezone.now().date()

        # Check if the user already has a started timesheet today
        if TimeSheet.objects.filter(user=user, date=today, end_time__isnull=True).exists():
            return Response({"detail": "You have already started a timesheet today."}, status=status.HTTP_400_BAD_REQUEST)
        
        data = {
            'user': user.id,
            'start_time': timezone.now()
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class TimeSheetPauseResumeView(generics.UpdateAPIView):
    serializer_class = TimeSheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        today = timezone.now().date()
        timesheet = TimeSheet.objects.filter(user=user, date=today, end_time__isnull=True).first()

        if not timesheet:
            return Response({"detail": "No active timesheet found."}, status=status.HTTP_404_NOT_FOUND)

        # If paused, resume; if active, pause
        if 'pause' in request.data and request.data['pause']:
            if not timesheet.end_time:
                timesheet.paused_time += timezone.now() - timesheet.start_time
                timesheet.start_time = timezone.now()
                timesheet.save()
                return Response({"detail": "TimeSheet paused."}, status=status.HTTP_200_OK)
        elif 'resume' in request.data and request.data['resume']:
            timesheet.start_time = timezone.now()
            timesheet.save()
            return Response({"detail": "TimeSheet resumed."}, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

class TimeSheetStopView(generics.UpdateAPIView):
    serializer_class = TimeSheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = request.user
        today = timezone.now().date()
        timesheet = TimeSheet.objects.filter(user=user, date=today, end_time__isnull=True).first()

        if not timesheet:
            return Response({"detail": "No active timesheet found."}, status=status.HTTP_404_NOT_FOUND)

        timesheet.end_time = timezone.now()
        timesheet.save()
        return Response({"detail": "TimeSheet stopped.", "total_time": timesheet.total_time()}, status=status.HTTP_200_OK)

class TimeSheetListView(generics.ListAPIView):
    serializer_class = TimeSheetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        today = timezone.now().date()

        if user.has_special_access:
            queryset = TimeSheet.objects.all()
        else:
            queryset = TimeSheet.objects.filter(user=user)

        period = self.request.query_params.get('period', 'day')

        if period == 'day':
            queryset = queryset.filter(date=today)
        elif period == 'week':
            week_start = today - timedelta(days=today.weekday())
            queryset = queryset.filter(date__range=[week_start, today])
        elif period == 'month':
            queryset = queryset.filter(date__month=today.month, date__year=today.year)

        return queryset
