from rest_framework import serializers
from .models import *


class AbilityTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbilityTag
        fields = ('name', 'description', 'abilitytype_set')


class AbilityTypeSerializer(serializers.ModelSerializer):
    tags = AbilityTagSerializer(many=True)

    class Meta:
        model = AbilityType
        fields = ('name', 'description', 'tags', 'ability_set', 'nonfinancialproject_set')


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ('country', 'province', 'city', 'postal_code', 'address', 'phone_number')


class UserSerializer(serializers.ModelSerializer):
    contact_info = ContactInfoSerializer()

    class Meta:
        model = User
        fields = ('is_charity', 'is_benefactor', 'is_admin', 'contact_info', 'username', 'password', 'is_authenticated',
                  'notification_set', 'log_first_actor', 'log_second_actor')


class BenefactorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Benefactor
        fields = ('first_name', 'last_name', 'gender', 'age', 'credit', 'score', 'charity_set', 'benefactorscore_set',
                  'charityscore_set', 'cooperationrequest_set', 'user', 'ability_set', 'project_set',
                  'dateinterval_set', 'financialcontribution_set')


class CharitySerializer(serializers.ModelSerializer):
    user = UserSerializer()
    benefactor_history = BenefactorSerializer(many=True)

    class Meta:
        model = Charity
        fields = ('name', 'score', 'benefactor_history', 'benefactorscore_set', 'charityscore_set',
                  'cooperationrequest_set', 'user', 'project_set')


class NotificationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Notification
        fields = ('type', 'user', 'date_time', 'description')


class BenefactorScoreSerializer(serializers.ModelSerializer):
    ability_type = AbilityTypeSerializer()
    benefactor = BenefactorSerializer()
    charity = CharitySerializer()

    class Meta:
        model = BenefactorScore
        fields = ('ability_type', 'benefactor', 'charity', 'score')


class CharityScoreSerializer(serializers.ModelSerializer):
    benefactor = BenefactorSerializer()
    charity = CharitySerializer()

    class Meta:
        model = CharityScore
        fields = ('benefactor', 'charity', 'score')


class AbilityRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbilityRequest
        fields = ('type', 'name', 'description')


class CooperationRequestSerializer(serializers.ModelSerializer):
    benefactor = BenefactorSerializer()
    charity = CharitySerializer()

    class Meta:
        model = CooperationRequest
        fields = ('type', 'state', 'benefactor', 'charity', 'description', 'nonfinancialproject_set')
