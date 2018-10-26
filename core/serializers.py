from rest_framework import serializers

from .models import Request, Feedback, Seller, User, Category, Tag


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('name',)

class TagSerializer(serializers.ModelSerializer):

    # seller = SellerSerializer

    class Meta:
        model = Tag
        fields = ('name', 'seller')

class SellerSerializer(serializers.ModelSerializer):

    # tag = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    # tag = TagSerializer(read_only=True, many=True)

    class Meta:
        model = Seller
        fields = ('name', 'category', 'tag')

    def update(self, instance, validated_data):
        # print(validated_data)
        # if validated_data['tag']:
        if validated_data.get('tag'):
            tag_data = validated_data.get('tag')
            # print(tag_data.get())
            tag = Tag.objects.get(name=tag_data.pop())
            instance.tag.add(tag)
        if validated_data.get('category'):
            category_data = validated_data.pop('category')
            category = Category.objects.get(name=category_data.pop())
            instance.category.add(category)
        instance.save()
        return instance
    # def update(self, validated_data):
    #     tag_data = validated_data.pop('tag')
    #     seller = Seller.objects.get(**validated_data)
    #     for track_data in tracks_data:
    #         Track.objects.create(album=album, **track_data)
    #     return seller






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