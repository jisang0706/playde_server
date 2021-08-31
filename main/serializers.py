
from rest_framework import serializers

from rest_framework.serializers import (
      ModelSerializer,
)

from .models import User


class imageSerializer(ModelSerializer):
   big_image = serializers.ImageField()
   class Meta:
      model = User
      fields = ('id', 'big_image')