from rest_framework import serializers
from .models import Patient, Doctor, PatientDoctorMapping


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for Patient model
    """
    created_by = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'email', 'phone', 'date_of_birth', 
            'gender', 'address', 'medical_history', 'created_by',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_by', 'created_at', 'updated_at')
    
    def validate_phone(self, value):
        """
        Validate phone number format
        """
        if not value.replace('+', '').replace('-', '').replace(' ', '').isdigit():
            raise serializers.ValidationError("Phone number must contain only digits, +, -, and spaces")
        return value


class DoctorSerializer(serializers.ModelSerializer):
    """
    Serializer for Doctor model
    """
    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'email', 'phone', 'specialization',
            'license_number', 'years_of_experience', 'consultation_fee',
            'available_from', 'available_to', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')
    
    def validate_years_of_experience(self, value):
        """
        Validate years of experience
        """
        if value < 0:
            raise serializers.ValidationError("Years of experience cannot be negative")
        if value > 50:
            raise serializers.ValidationError("Years of experience seems unrealistic")
        return value
    
    def validate_consultation_fee(self, value):
        """
        Validate consultation fee
        """
        if value < 0:
            raise serializers.ValidationError("Consultation fee cannot be negative")
        return value


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    """
    Serializer for PatientDoctorMapping model
    """
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization', read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'patient_name', 'doctor_name',
            'doctor_specialization', 'assigned_at', 'notes', 'is_active'
        ]
        read_only_fields = ('id', 'assigned_at', 'patient_name', 'doctor_name', 'doctor_specialization')
    
    def validate(self, attrs):
        """
        Validate patient-doctor mapping
        """
        patient = attrs.get('patient')
        doctor = attrs.get('doctor')
        
        # Check if mapping already exists
        if PatientDoctorMapping.objects.filter(
            patient=patient, 
            doctor=doctor, 
            is_active=True
        ).exists():
            raise serializers.ValidationError(
                "This patient is already assigned to this doctor"
            )
        
        return attrs


class PatientDoctorMappingDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for PatientDoctorMapping with nested objects
    """
    patient = PatientSerializer(read_only=True)
    doctor = DoctorSerializer(read_only=True)
    
    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'patient', 'doctor', 'assigned_at', 'notes', 'is_active']