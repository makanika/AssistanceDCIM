from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import VisitorLog
from .forms import VisitorLogForm # We will create this form next

@login_required
def visitor_log_list(request):
    """
    Displays a list of all visitor logs.
    """
    visitors = VisitorLog.objects.all().order_by('-visit_date', '-time_in')
    form = VisitorLogForm() # Form for adding new entries
    context = {
        'visitors': visitors,
        'form': form,
    }
    return render(request, 'visitors/visitor_log.html', context)

@login_required
def add_visitor_log(request):
    """
    Handles adding a new visitor log entry.
    """
    if request.method == 'POST':
        form = VisitorLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('visitor_log_list')
    # If not POST or form is invalid, redirect back to the list page (which will display the form)
    return redirect('visitor_log_list')

@login_required
def edit_visitor_log(request, pk):
    """
    Handles editing an existing visitor log entry.
    """
    visitor_entry = get_object_or_404(VisitorLog, pk=pk)
    if request.method == 'POST':
        form = VisitorLogForm(request.POST, instance=visitor_entry)
        if form.is_valid():
            form.save()
            return redirect('visitor_log_list')
    else:
        form = VisitorLogForm(instance=visitor_entry)
    return render(request, 'visitors/edit_visitor_log.html', {'form': form, 'visitor_entry': visitor_entry})

@login_required
def delete_visitor_log(request, pk):
    """
    Handles deleting a visitor log entry.
    """
    visitor_entry = get_object_or_404(VisitorLog, pk=pk)
    if request.method == 'POST':
        visitor_entry.delete()
        return redirect('visitor_log_list')
    return render(request, 'visitors/confirm_delete.html', {'visitor_entry': visitor_entry})

