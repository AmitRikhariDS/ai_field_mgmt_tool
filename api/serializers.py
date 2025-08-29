from rest_framework import serializers
from core.models import Client, Engineer, Job, Invoice,TimeEntry

# ---------- Client ----------
# class ClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields = ['id', 'name', 'contact_email', 'contact_phone']
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from core.models import Client

class ClientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = Client
        fields = ['id', 'name', 'contact_email', 'contact_person',
                  'username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        email = validated_data.pop('email', '')

        # Create User
        user = User.objects.create_user(username=username, password=password,
                                        first_name=first_name, last_name=last_name, email=email)
        # Add to Client group
        group, _ = Group.objects.get_or_create(name='Client')
        user.groups.add(group)
        user.save()

        # Create Client profile
        client = Client.objects.create(user=user, **validated_data)
        return client

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

# api/serializers.py
from rest_framework import serializers
from django.contrib.auth.models import User, Group
from core.models import Client

class ClientSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(write_only=True, required=False)

    class Meta:
        model = Client
        fields = ['id', 'name', 'contact_email', 'contact_person',
                  'username', 'password', 'first_name', 'last_name', 'email']

    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        first_name = validated_data.pop('first_name', '')
        last_name = validated_data.pop('last_name', '')
        email = validated_data.pop('email', '')

        # Create User
        user = User.objects.create_user(username=username, password=password,
                                        first_name=first_name, last_name=last_name, email=email)
        # Add to Client group
        group, _ = Group.objects.get_or_create(name='Client')
        user.groups.add(group)
        user.save()

        # Create Client profile
        client = Client.objects.create(user=user, **validated_data)
        return client
