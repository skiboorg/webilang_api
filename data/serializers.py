from rest_framework import serializers
from .models import *

class TariffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tariff
        fields = '__all__'

class TariffCategorySerializer(serializers.ModelSerializer):
    tariffs = TariffSerializer(many=True, required=False, read_only=True)
    class Meta:
        model = TariffCategory
        fields = '__all__'



class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

