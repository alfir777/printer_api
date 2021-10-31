from rest_framework.viewsets import ModelViewSet

from .models import Check
from .serializers import ChecksSerializer


class CheckViewSet(ModelViewSet):
    queryset = Check.objects.all()
    serializer_class = ChecksSerializer
