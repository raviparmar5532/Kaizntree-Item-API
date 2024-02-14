from rest_framework import serializers
from .models import Item, Tag
from django.contrib.auth.models import User


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['tag']

class ItemSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    
    class Meta:
        model = Item
        exclude = ['user']
        # fields = '__all__'
        # fields = [
        #     'id',
        #     'SKU',
        #     'name',
        #     'description',
        #     'tags',
        #     'category',
        #     'in_stock',
        #     'available_stock'
        # ]


    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        item = Item.objects.create(**validated_data, user = self.context['request'].user)

        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(tag=tag_data['tag'])
            item.tags.add(tag)
        return item

    def update(self, instance, validated_data):
        print(validated_data)
        instance.SKU = validated_data.get('SKU', instance.SKU)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.category = validated_data.get('category', instance.category)
        instance.in_stock = validated_data.get('in_stock', instance.in_stock)
        instance.available_stock = validated_data.get('available_stock', instance.available_stock)

        tags_data = validated_data.pop('tags', [])
        instance.tags.clear()
        for tag_data in tags_data:
            tag, created = Tag.objects.get_or_create(tag=tag_data['tag'])
            instance.tags.add(tag)
        instance.save()
        return instance
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        