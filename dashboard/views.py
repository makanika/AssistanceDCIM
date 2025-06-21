from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Rack, SensorData, PDUFeed, CrossConnect
from visitors.models import VisitorLog # Import VisitorLog
import datetime
import json # For passing chart data as JSON to JS
from django.http import HttpResponse
from django.template.loader import get_template
from django.conf import settings
import os

# You'll need to install a PDF generation library. WeasyPrint is a good choice:
# pip install WeasyPrint
# from weasyprint import HTML, CSS # Uncomment if using WeasyPrint

@login_required # Ensures only logged-in users can access this view
def dashboard_view(request):
    """
    Renders the main DCIM dashboard with real-time and log data.
    """
    # Fetch overall data center summary
    total_racks = Rack.objects.count()
    contracted_power_kw = 17.0 # Static for now, could be a setting or another model
    current_total_load = sum(rack.used_power_kw for rack in Rack.objects.all())

    # Cooling status (simplified)
    cooling_status = "Optimal"
    for rack in Rack.objects.all():
        if rack.current_inlet_temp and rack.current_inlet_temp > 28.0:
            cooling_status = "Warning (High Rack Temp)"
            break

    # Active alerts (simplified)
    active_alerts = 0
    warning_alerts = 0
    for rack in Rack.objects.all():
        if rack.current_inlet_temp and rack.current_inlet_temp > 40.0:
            active_alerts += 1
        elif rack.current_inlet_temp and rack.current_inlet_temp > 28.0:
            warning_alerts += 1

    all_racks = list(Rack.objects.all()) # Convert to list for iteration and JSON serialization

    # Prepare rack data for JavaScript (for charts)
    all_racks_json = []
    for rack in all_racks:
        all_racks_json.append({
            'id': rack.id,
            'name': rack.name,
            'power': float(rack.used_power_kw),
            'temp': float(rack.current_inlet_temp) if rack.current_inlet_temp is not None else None,
            'capacity': float(rack.max_power_capacity_kw)
        })

    # PDU Feeds
    pdu_feeds = PDUFeed.objects.all()

    # Cross Connects
    cross_connects = CrossConnect.objects.all()

    # Environmental Monitoring (simplified, directly from template data for now)
    room_ambient_temp = 22.5
    room_ambient_humidity = 48
    crac_unit1_status = "Running"
    crac_unit2_status = "Standby"
    airflow_pressure = 15

    # Visitors Log (last month)
    # Get current date
    today = datetime.date.today()
    # Calculate date for one month ago
    one_month_ago = today - datetime.timedelta(days=30)
    visitors_last_month = VisitorLog.objects.filter(visit_date__gte=one_month_ago).order_by('-visit_date')


    context = {
        'total_racks': total_racks,
        'contracted_power_kw': contracted_power_kw,
        'current_total_load': current_total_load, # Pass as float for JS calc
        'cooling_status': cooling_status,
        'active_alerts': active_alerts,
        'warning_alerts': warning_alerts,
        'all_racks': all_racks,
        'all_racks_json': json.dumps(all_racks_json), # Data for JS charts
        'pdu_feeds': pdu_feeds,
        'cross_connects': cross_connects,
        'room_ambient_temp': room_ambient_temp,
        'room_ambient_humidity': room_ambient_humidity,
        'crac_unit1_status': crac_unit1_status,
        'crac_unit2_status': crac_unit2_status,
        'airflow_pressure': airflow_pressure,
        'visitors': visitors_last_month,
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def generate_pdf_report(request):
    """
    Generates a PDF report based on selected dashboard cards.
    """
    # This view will receive POST data indicating which sections to include
    if request.method == 'POST':
        # Default to include all if no specific cards are selected for simplicity
        include_overview = 'overview' in request.POST
        include_power_analytics = 'power_analytics' in request.POST
        include_detailed_racks = 'detailed_racks' in request.POST
        include_power_distribution = 'power_distribution' in request.POST
        include_connectivity = 'connectivity' in request.POST
        include_environment = 'environment' in request.POST
        include_visitors_log = 'visitors_log' in request.POST

        # Fetch all necessary data, similar to dashboard_view
        current_total_load = sum(rack.used_power_kw for rack in Rack.objects.all())
        all_racks = list(Rack.objects.all())
        pdu_feeds = PDUFeed.objects.all()
        cross_connects = CrossConnect.objects.all()
        visitors_last_month = VisitorLog.objects.filter(
            visit_date__gte=datetime.date.today() - datetime.timedelta(days=30)
        ).order_by('-visit_date')

        # Context for the PDF template
        pdf_context = {
            'report_date': datetime.date.today(),
            'report_time': datetime.datetime.now().strftime('%H:%M %Z'),
            'contracted_power_kw': 17.0,
            'current_total_load': current_total_load,
            'all_racks': all_racks,
            'pdu_feeds': pdu_feeds,
            'cross_connects': cross_connects,
            'visitors': visitors_last_month,
            'room_ambient_temp': 22.5,
            'room_ambient_humidity': 48,
            'crac_unit1_status': "Running",
            'crac_unit2_status': "Standby",
            'airflow_pressure': 15,
            # Flags to control section visibility in PDF
            'include_overview': include_overview,
            'include_power_analytics': include_power_analytics,
            'include_detailed_racks': include_detailed_racks,
            'include_power_distribution': include_power_distribution,
            'include_connectivity': include_connectivity,
            'include_environment': include_environment,
            'include_visitors_log': include_visitors_log,
        }

        # Render the PDF template
        template = get_template('dashboard/pdf_report_template.html')
        html_content = template.render(pdf_context)

        # Generate PDF using WeasyPrint (recommended)
        # You would need to ensure static files are properly served for WeasyPrint
        # to find the CSS if it's external, or embed CSS directly.
        # This is a placeholder as WeasyPrint requires environment setup.
        # pdf_file = HTML(string=html_content, base_url=request.build_absolute_uri('/')).write_pdf(
        #     stylesheets=[CSS(settings.STATIC_ROOT + '/css/pdf.css')]
        # )
        # response = HttpResponse(pdf_file, content_type='application/pdf')
        # response['Content-Disposition'] = 'attachment; filename="DCIM_Report_{}.pdf"'.format(
        #     datetime.date.today().strftime('%Y%m%d')
        # )
        # return response

        # For demo purposes without WeasyPrint installed, we'll return HTML for preview.
        # In a real app, this should be the WeasyPrint block above.
        response = HttpResponse(html_content, content_type='text/html')
        # You'd typically want to redirect or return the PDF, not just HTML here.
        # return redirect('dashboard') # Or a success message

        # Mock PDF generation response (replace with actual PDF generation)
        response = HttpResponse("PDF generation initiated. (Please install WeasyPrint for actual PDF output)", content_type='text/plain')
        response['Content-Disposition'] = 'inline; filename="mock_report.txt"' # Suggest saving as txt
        return response

    # If GET request, show the form to select cards
    return render(request, 'dashboard/pdf_selection_page.html', {})
