from rest_framework import serializers
from core.models import Client, Engineer, Job, Invoice,TimeEntry

# ---------- Client ----------
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'contact_email', 'contact_phone']

# ---------- Engineer ----------
class EngineerSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True, required=False, allow_null=True)

    class Meta:
        model = Engineer
        fields = ['id', 'name', 'phone', 'status', 'country', 
                  'primary_skills', 'certifications', 'education',
                  'work_experience', 'summary', 'image']

# ---------- Job ----------
class JobSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    engineer = EngineerSerializer(read_only=True)

    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source='client', write_only=True
    )
    engineer_id = serializers.PrimaryKeyRelatedField(
        queryset=Engineer.objects.all(), source='engineer', write_only=True, 
        allow_null=True, required=False
    )

    class Meta:
        model = Job
        fields = ['id', 'job_code', 'title', 'status', 'priority',
                  'client', 'client_id', 'engineer', 'engineer_id',
                  'scheduled_date']



# ---------- Invoice ----------


# api/serializers.py
class TimeEntrySerializer(serializers.ModelSerializer):
    hours_worked = serializers.ReadOnlyField()

    class Meta:
        model = TimeEntry
        fields = ['id', 'job', 'engineer', 'start', 'end', 'notes', 'hours_worked']

# api/serializers.py
from rest_framework import serializers
from core.models import Invoice


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'