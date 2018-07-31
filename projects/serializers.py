from rest_framework import serializers
from .models import *
from accounts.models import *
from accounts.serializers import *


class AbilitySerializer(serializers.ModelSerializer):
    benefactor = BenefactorSerializer()
    ability_type = AbilityTypeSerializer()

    class Meta:
        model = Ability
        fields = ('benefactor', 'ability_type', 'score', 'description')


class ProjectSerializer(serializers.ModelSerializer):
    charity = CharitySerializer()
    benefactors = BenefactorSerializer(many=True)

    class Meta:
        model = Project
        fields = ('project_name', 'charity', 'benefactors', 'description', 'project_state', 'type', 'financialproject',
                  'nonfinancialproject', 'log_set')


class FinancialProjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()

    class Meta:
        model = FinancialProject
        fields = ('project', 'target_money', 'current_money', 'start_date', 'end_date', 'financialcontribution_set',
                  'cooperationrequest_set')


class NonFinancialProjectSerializer(serializers.ModelSerializer):
    project = ProjectSerializer()
    ability_type = AbilityTypeSerializer()

    class Meta:
        model = NonFinancialProject
        fields = ('project', 'ability_type', 'min_age', 'max_age', 'required_gender', 'country', 'province', 'city',
                  'dateinterval')


class DateIntervalSerializer(serializers.ModelSerializer):
    benefactor = BenefactorSerializer()
    non_financial_project = NonFinancialProjectSerializer()

    class Meta:
        model = DateInterval
        fields = ('benefactor', 'non_financial_project', 'begin_date', 'end_date', 'week_schedule')


class FinancialContributionSerializer(serializers.ModelSerializer):
    benefactor = BenefactorSerializer()
    financial_project = FinancialProjectSerializer()

    class Meta:
        model = FinancialContribution
        fields = ('benefactor', 'financial_project', 'money')


class LogSerializer(serializers.ModelSerializer):
    first_actor = UserSerializer()
    second_actor = UserSerializer()
    log_project = ProjectSerializer()

    class Meta:
        model = Log
        fields = ('log_type', 'first_actor', 'second_actor', 'log_project', 'date_time', 'description')


class CooperationRequestSerializer(serializers.ModelSerializer):
    benefactor = BenefactorSerializer()
    charity = CharitySerializer()
    project = ProjectSerializer()

    class Meta:
        model = CooperationRequest
        fields = ('type', 'state', 'benefactor', 'charity', 'description', 'project')