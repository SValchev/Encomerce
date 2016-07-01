from rest_framework import serializers
from .models import Status
from payments.models import User

class RelatedUserFields(serializers.RelatedField):

    def to_representation(self, value):
        return value.email

    def to_internal_value(self, data):
        return User.objects.get(email=data)


class StatusReportSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    user = serializers.StringRelatedField()
    time_added = serializers.DateTimeField()
    status = serializers.CharField(max_length=200)

    def create(self, validate_data):
        return Status(**validate_data)

    def update(self, instance, validate_data):
        instance.user = validate_data.get('user', instance.user)
        instance.time_added = validate_data.get('time_added', instance.time_added)
        instance.status = validate_data.get('status', instance.status)

        instance.save()
        return instancez
