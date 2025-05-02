from django.shortcuts import render
from .serializer import PhotographerSerializer
from rest_framework import viewsets,permissions
from .models import Photographer
from .permissions import IsAuthenticatedOrViewOnly

# Create your views here.
class PhotographerViewSet(viewsets.ModelViewSet):
    """
    API endpoint to view or manage Photographers.
    """
    queryset = Photographer.objects.all()
    serializer_class  = PhotographerSerializer
    permission_classes = [IsAuthenticatedOrViewOnly]
    

        
