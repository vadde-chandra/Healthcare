from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Patient, Doctor, PatientDoctorMapping
from .serializers import (
    PatientSerializer, DoctorSerializer, 
    PatientDoctorMappingSerializer, PatientDoctorMappingDetailSerializer
)


class PatientListCreateView(generics.ListCreateAPIView):
    """
    List all patients for the authenticated user or create a new patient
    """
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a patient instance
    """
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Patient.objects.filter(created_by=self.request.user)


class DoctorListCreateView(generics.ListCreateAPIView):
    """
    List all doctors or create a new doctor
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class DoctorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete a doctor instance
    """
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]


class PatientDoctorMappingListCreateView(generics.ListCreateAPIView):
    """
    List all patient-doctor mappings or create a new mapping
    """
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(is_active=True)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def patient_doctors_list(request, patient_id):
    """
    Get all doctors assigned to a specific patient
    """
    try:
        patient = get_object_or_404(Patient, id=patient_id, created_by=request.user)
        mappings = PatientDoctorMapping.objects.filter(
            patient=patient, 
            is_active=True
        ).select_related('doctor')
        
        serializer = PatientDoctorMappingDetailSerializer(mappings, many=True)
        return Response({
            'patient': PatientSerializer(patient).data,
            'doctors': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Failed to retrieve patient doctors',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_patient_doctor_mapping(request, mapping_id):
    """
    Remove a doctor from a patient (soft delete)
    """
    try:
        mapping = get_object_or_404(PatientDoctorMapping, id=mapping_id)
        
        # Check if the user owns the patient
        if mapping.patient.created_by != request.user:
            return Response({
                'error': 'Permission denied'
            }, status=status.HTTP_403_FORBIDDEN)
        
        mapping.is_active = False
        mapping.save()
        
        return Response({
            'message': 'Doctor removed from patient successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Failed to remove doctor from patient',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_stats(request):
    """
    Get dashboard statistics for the authenticated user
    """
    try:
        total_patients = Patient.objects.filter(created_by=request.user).count()
        total_doctors = Doctor.objects.count()
        total_mappings = PatientDoctorMapping.objects.filter(
            patient__created_by=request.user,
            is_active=True
        ).count()
        
        return Response({
            'total_patients': total_patients,
            'total_doctors': total_doctors,
            'total_active_mappings': total_mappings
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'error': 'Failed to retrieve dashboard stats',
            'details': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)