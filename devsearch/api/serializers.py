from rest_framework import serializers 
from projects.models import Project


#Serializer convers python dict to json 
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'