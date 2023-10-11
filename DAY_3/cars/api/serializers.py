from rest_framework import serializers
from ..models import Car

class CarSerializer(serializers.ModelSerializer):
    image = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Car
        fields = '__all__'

    def create(self, validated_data):
        image_id = self.context['view'].kwargs.get('imageId')
        validated_data['image'] = [image_id] if image_id else []
        return super().create(validated_data)
    

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        image = representation.get('image')
        if image:
            representation['image']=[image]
        else:
            representation['image']=[]

        return representation