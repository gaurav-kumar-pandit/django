from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name')

class BaseSerializer(serializers.ModelSerializer):
    eid = serializers.UUIDField(read_only=True)

class SubRedditSerializer(BaseSerializer):
    posts = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)
    moderators = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all(), required=True, read_only=False)

    class Meta:
        model = SubReddit
        fields = ('eid', 'name', 'cover_image_url', 'posts', 'moderators')
    
    def validate_moderators(self, value):
        if not value or len(value) == 0:
            raise serializers.ValidationError('Need to include at least one moderator!')
        return value

    def create(self, validated_data):

        user = self.context['request'].user
        moderators = validated_data.pop('moderators')
        if user not in moderators: moderators.append(user)
        subreddit = SubReddit.objects.create(**validated_data)
        for mod in moderators: subreddit.moderators.add(mod)
        return subreddit
        


    