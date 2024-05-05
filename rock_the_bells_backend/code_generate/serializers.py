from rest_framework.serializers import ModelSerializer

from .models import CodeModel


class CodeSerializer(ModelSerializer):
    class Meta:
        model = CodeModel
        fields = '__all__'

