from rest_framework import serializers

from renter.models import Renter


class RenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Renter
        fields = '__all__'

