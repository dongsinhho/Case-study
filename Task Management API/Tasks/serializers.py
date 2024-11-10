from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    due_date = serializers.DateField(required=False)
    
    STATUS_CHOICES = ["Pending", "Completed"]
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=True)

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'status']

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value