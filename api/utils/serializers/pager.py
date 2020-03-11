from rest_framework import serializers

from api import models


class PagerSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Role
        fields = "__all__"