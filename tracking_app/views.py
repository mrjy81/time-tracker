from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from .forms import TrackerForm
from .models import TrackerModel, TrackerTitles
import jdatetime
from django.utils import timezone
from .forms import UserLoginForm, EditTrackerTextForm
from django.http import HttpResponse
import csv

def login_view(request):
    form = UserLoginForm()
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    context = {'form': form}
    return render(request, 'login.html', context)


@login_required
def index(request):
    form = TrackerForm()
    if request.method == 'POST':
        today = jdatetime.date.today()
        title = request.POST['title']
        title_obj, is_tracker = TrackerTitles.objects.get_or_create(title=title)
        time_tracker_obj = TrackerModel.objects.create(title=title_obj, datetime=today, user=request.user)
        return redirect("handler", pk=time_tracker_obj.pk)

    context = {
        "form": form,
    }
    return render(request, 'tracking.html', context=context)


@login_required
def handler(request, pk):
    time_tracker_obj = TrackerModel.objects.get(pk=pk)
    now = timezone.localtime(timezone.now())
    context = {
        "stopped": time_tracker_obj.is_stopped,
        "item": time_tracker_obj
    }
    if request.method == 'POST':
        if 'stop_button' in request.POST:
            if time_tracker_obj.paused_at:
                delta = now - time_tracker_obj.paused_at
            else:
                delta = now - time_tracker_obj.created_at
            time_tracker_obj.total_minutes = time_tracker_obj.total_minutes + delta.total_seconds() // 60
            time_tracker_obj.paused_at = now
            time_tracker_obj.is_stopped = True
            time_tracker_obj.save()
            context['stopped'] = True
            return render(request, 'tracking_handler.html', context=context)

        if "start_button" in request.POST:
            time_tracker_obj.paused_at = now
            time_tracker_obj.is_stopped = False
            time_tracker_obj.save()
            context['stopped'] = False
            return render(request, 'tracking_handler.html', context=context)

    return render(request, 'tracking_handler.html', context=context)


@login_required
def dashboard(request):
    trackers = TrackerModel.objects.filter(user=request.user)
    total_hours = sum([i.total_minutes for i in trackers]) // 60
    context = {
        'trackers': trackers,
        'total_hours': total_hours,
    }
    return render(request, 'dashboard.html', context=context)


@login_required
def edit(request, pk):
    tracker = TrackerModel.objects.get(pk=pk)
    form = EditTrackerTextForm(initial={'text': tracker.text})
    if request.method == "POST":
        form = EditTrackerTextForm(request.POST)
        if form.is_valid():
            tracker.text = form.cleaned_data['text']
            tracker.save()
    context = {
        'form': form,
        "tracker": tracker
    }
    return render(request, 'edit.html', context=context)


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="time.csv"'

    # Create a CSV writer object
    csv_writer = csv.writer(response,delimiter=',')

    # Write the header row with column names
    csv_writer.writerow(['start-date', 'title', 'total minutes'])

    for t in TrackerModel.objects.all():
        date_string = t.datetime.strftime('%m/%d/%Y')
        csv_writer.writerow([date_string, t.title, t.total_minutes])
    return response
