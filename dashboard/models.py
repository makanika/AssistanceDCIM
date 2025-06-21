from django.db import models

class Rack(models.Model):
    """
    Represents a single rack in the data center.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Unique name for the rack (e.g., 'Comm Rack', 'Servers Rack')")
    location = models.CharField(max_length=200, blank=True, null=True, help_text="Physical location within the data center")
    total_units = models.IntegerField(default=42, help_text="Total rack units (U) available in this rack")
    max_power_capacity_kw = models.DecimalField(max_digits=5, decimal_places=2, default=4.0, help_text="Maximum power capacity (kW) of the rack")

    def __str__(self):
        return self.name

    @property
    def used_power_kw(self):
        """
        Calculates the current total power draw for this rack from its sensor data.
        """
        # This is simplified; in a real scenario, you might average recent readings
        # or get the very last reading. For demo, we'll sum relevant sensor types.
        # Assuming 'Power Draw' sensor type directly reflects rack power
        total_power = self.sensordata_set.filter(
            sensor_type='Power Draw'
        ).aggregate(models.Sum('value'))['value__sum']
        return total_power if total_power is not None else 0.0

    @property
    def power_utilization_percentage(self):
        """
        Calculates the power utilization percentage for this rack.
        """
        if self.max_power_capacity_kw > 0:
            return (self.used_power_kw / self.max_power_capacity_kw) * 100
        return 0.0

    @property
    def current_inlet_temp(self):
        """
        Gets the latest inlet temperature for this rack.
        """
        latest_temp = self.sensordata_set.filter(
            sensor_type='Inlet Temp'
        ).order_by('-timestamp').first()
        return latest_temp.value if latest_temp else None

    @property
    def current_humidity(self):
        """
        Gets the latest humidity reading for this rack.
        """
        latest_humidity = self.sensordata_set.filter(
            sensor_type='Humidity'
        ).order_by('-timestamp').first()
        return latest_humidity.value if latest_humidity else None

    @property
    def used_units(self):
        """
        Placeholder for used rack units. In a real app, this would be derived
        from installed equipment models.
        """
        # For demo, we'll hardcode based on rack name
        if "Comm" in self.name: return 38
        if "Servers" in self.name: return 40
        if "Storage" in self.name: return 30
        if "DC/Fibre" in self.name: return 15 # Less units for rectifier/fibre
        return 0


class SensorData(models.Model):
    """
    Stores sensor readings for various parameters within a rack.
    """
    SENSOR_CHOICES = [
        ('Power Draw', 'Power Draw (kW)'),
        ('Inlet Temp', 'Inlet Temperature (°C)'),
        ('Humidity', 'Humidity (% RH)'),
        ('CPU Load', 'CPU Load (%)'),
        ('Disk I/O', 'Disk I/O (%)'),
        ('Network Traffic', 'Network Traffic (%)'),
        ('Airflow Pressure', 'Airflow Pressure (Pa)'),
        ('DC Output Voltage', 'DC Output Voltage (V)'),
        ('Rectifier Temp', 'Rectifier Temperature (°C)'),
        # Add other relevant sensor types
    ]
    rack = models.ForeignKey(Rack, on_delete=models.CASCADE)
    sensor_type = models.CharField(max_length=50, choices=SENSOR_CHOICES)
    value = models.DecimalField(max_digits=8, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rack.name} - {self.sensor_type}: {self.value} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-timestamp'] # Order by latest timestamp by default


class PDUFeed(models.Model):
    """
    Represents a Power Distribution Unit (PDU) feed.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Name of the PDU feed (e.g., 'PDU Feed 1 (Active)')")
    status = models.CharField(max_length=50, default='Online', help_text="Current status (e.g., 'Online', 'Standby', 'Offline')")
    capacity_kw = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Capacity of the PDU feed in kW")
    # A PDU feed might power multiple racks, but for simplicity, we keep it general.

    def __str__(self):
        return self.name

class CrossConnect(models.Model):
    """
    Details about network and fibre cross-connections.
    """
    name = models.CharField(max_length=200, help_text="Descriptive name of the cross-connect (e.g., 'Fibre ODF - Rack 1')")
    source = models.CharField(max_length=100, help_text="Source port/device")
    destination = models.CharField(max_length=100, help_text="Destination port/device")
    connection_type = models.CharField(max_length=50, help_text="Type of connection (e.g., '10 GbE', 'Fibre Channel')")
    status = models.CharField(max_length=50, default='Active', help_text="Status of the connection (e.g., 'Active', 'Inactive')")

    def __str__(self):
        return f"{self.name} ({self.connection_type}) - {self.status}"


