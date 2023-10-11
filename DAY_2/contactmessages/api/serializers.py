from rest_framework import serializers
from contactmessages.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if self.context['request'].path == "/contactmessage/visitors/":
            return {"message": "Succesfully created message", "success": True}
        return data