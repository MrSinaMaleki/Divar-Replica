from rest_framework import serializers
from apps.account.models import User
from apps.bookmark.models import Bookmark
from apps.post.serializers import PostSerializer


class FavoriteAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['posts']

    def create(self, validated_data):
        # print("user => ",self.context['request'].user)
        user = User.objects.get(id=self.context['request'].user.id)
        try:
            favorite = Bookmark.objects.get(posts_id=validated_data['posts'].id, user=user)
            favorite.is_active = False
            favorite.is_delete = True
            favorite.save()
        except Bookmark.DoesNotExist:
            Bookmark.objects.create(user=user, posts_id=validated_data['posts'].id)
        return validated_data


class MyFavoriteSerializer(serializers.ModelSerializer):
    posts = PostSerializer(read_only=True)
    class Meta:
        model = Bookmark
        fields = ['id','user','posts']

