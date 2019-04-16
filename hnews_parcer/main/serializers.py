from rest_framework import serializers
from .models import Posts

class PostSerializer(serializers.HyperlinkedModelSerializer):
    """ Сериалайзер постов """
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    
    class Meta:
        model = Posts
        fields = ('id', 'title', 'url', 'created')