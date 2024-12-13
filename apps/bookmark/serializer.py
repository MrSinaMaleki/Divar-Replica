from rest_framework import serializers
from apps.account.models import User
from apps.bookmark.models import Bookmark


class FavoriteAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = ['posts']

    def create(self, validated_data):
        # print("user => ",self.context['request'].user)
        user = User.objects.get(id=self.context['request'].user.id)
        try:
            favorite = Bookmark.objects.get(products_id=validated_data['products'].id, user=user)
            favorite.is_active = False
            favorite.is_delete = True
            favorite.save()
        except Bookmark.DoesNotExist:
            Bookmark.objects.create(user=user, products_id=validated_data['products'].id)
        return validated_data

