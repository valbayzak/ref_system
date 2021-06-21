from rest_framework import serializers
from .models import Subscriber, Invite


class SubscriberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = ['phone']


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ['sender_subs_id', 'receiver_subs_id']