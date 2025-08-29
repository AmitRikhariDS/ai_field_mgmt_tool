from rest_framework import serializers
from core.models import Client, Engineer, Job, Invoice

# ---------- Client ----------
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ["id", "name"]


# ---------- Engineer ----------
class EngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engineer
        fields = ["id", "name", "status"]


# ---------- Job ----------
class JobSerializer(serializers.ModelSerializer):
    # Read-only nested
    client = ClientSerializer(read_only=True)
    engineer = EngineerSerializer(read_only=True)

    # Write-only IDs
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source="client", write_only=True
    )
    engineer_id = serializers.PrimaryKeyRelatedField(
        queryset=Engineer.objects.all(), source="engineer", write_only=True,
        allow_null=True, required=False
    )

    class Meta:
        model = Job
        fields = [
            "id", "job_code", "title", "status", "priority",
            "client", "client_id", "engineer", "engineer_id",
            "scheduled_date", "created_at"
        ]


# ---------- Invoice ----------
class InvoiceSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all(), source="client", write_only=True
    )

    class Meta:
        model = Invoice
        fields = [
            "id", "invoice_no", "amount", "paid",
            "client", "client_id", "created_at"
        ]
