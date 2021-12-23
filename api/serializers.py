from rest_framework import serializers


class SkiInputSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    id = serializers.RegexField(r'^\w+$', max_length=6, min_length=6)
    last_name = serializers.RegexField(r'^[A-Za-z]+$', min_length=1)
