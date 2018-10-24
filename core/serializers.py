from rest_framework import serializers

from .models import Request, Feedback, Seller, User, Category


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name',)


class SellerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Seller
        fields = ('name', 'category', 'tag')



class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ('title', 'category', 'dscr', 'status')

    def create(self, validated_data):
        return Request.objects.create(**validated_data) #?



class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = ('message', 'score', 'receiver')

    def create(self, validated_data):
        seller = validated_data['receiver']
        seller.rate(validated_data['score'])
        return Feedback.objects.create(**validated_data)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'parent')