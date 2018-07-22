from django.db import models
from accounts.models import *

from django.db import models

from django.db import models
from django.utils import timezone
import datetime, math, json


# Create your models here.


class ProjectManager(models.Manager):
    def finished_charity_filter_count(self, charity):
        return super().all().filter(project_state__iexact='finished').filter(charity=charity).count()

    def related_charity_filter_count(self, charity):
        return super().all().filter(charity=charity).count()


class AbilityTypeManager(models.Manager):
    def find_ability_ids(self, ability_name=None, ability_tags=None):
        result_abilities = super().all()
        if ability_name is not None:
            result_abilities = result_abilities.filter(name__icontains=ability_name)
        if ability_tags is not None:
            result_ids = [ability_type.id for ability_type in result_abilities if
                          all(tag in ability_tags for tag in ability_type.get_tag_strings())]
            result_abilities = result_abilities.filter(id__in=result_ids)
        return [ability.id for ability in result_abilities]


class AbilityTag(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)


class AbilityType(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000)
    tags = models.ManyToManyField(AbilityTag)
    objects = AbilityTypeManager()

    def get_tag_strings(self):
        return [tag.name for tag in self.tags.all()]

    def __str__(self):
        return self.name


class Ability(models.Model):
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE)
    ability_type = models.ForeignKey(AbilityType, on_delete=models.CASCADE)
    score = models.IntegerField
    description = models.CharField(max_length=300)


class Project(models.Model):
    project_name = models.CharField(max_length=200)
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE, primary_key=False)
    benefactors = models.ManyToManyField(Benefactor, primary_key=False)
    description = models.CharField(max_length=2000)
    project_state = models.CharField(max_length=50)
    objects = ProjectManager()
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.project_name + "-" + self.type


class FinancialProject(models.Model):
    # TODO set min
    project = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)

    target_money = models.FloatField
    current_money = models.FloatField

    start_date = models.DateField(default=datetime.date(2018, 1, 1))
    end_date = models.DateField(default=datetime.date(2018, 1, 1))

    def progress_in_range(self, min_progress, max_progress):
        return min_progress < self.current_money / self.target_money < max_progress

    def __str__(self):
        return self.project.__str__()


class NonFinancialProject(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE, primary_key=True)

    # TODO im not sure about the on_delete for this field
    ability_type = models.ForeignKey(AbilityType, on_delete=models.DO_NOTHING, primary_key=False)
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    required_gender = models.CharField(max_length=100, null=True)

    country = models.CharField(max_length=30)
    province = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

    def search_filter(self, min_date_overlap, min_required_hours, min_time_overlap, schedule):
        return has_matched_schedule(min_date_overlap, min_required_hours, min_time_overlap, schedule, self.dateinterval)

    def __str__(self):
        return self.project.__str__()


class DateInterval(models.Model):
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, null=True)
    non_financial_project = models.OneToOneField(NonFinancialProject, on_delete=models.CASCADE, null=True)

    begin_date = models.DateField(default=datetime.date(2018, 1, 1))
    end_date = models.DateField(default=datetime.date(2018, 1, 1))
    week_schedule = models.CharField(max_length=200, default='')

    def to_json(self, schedule):
        self.week_schedule = json.dumps(schedule)

    def from_json(self):
        return json.loads(self.week_schedule)


class Request(models.Model):
    sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, primary_key=False,
                               related_name='%(class)s_requests_sender')
    receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, primary_key=False,
                                 related_name='%(class)s_requests_receiver')
    description = models.CharField(max_length=2000)


def search_benefactor(wanted_schedule=None, min_required_hours=0, min_date_overlap=30, min_time_overlap=50, tags=None,
                      ability_name=None, ability_min_score=0, ability_max_score=10, country=None, province=None,
                      city=None, user_min_score=0, user_max_score=10, gender=None, first_name=None, last_name=None):
    if tags is None:
        tags = []

    result_benefactors = Benefactor.objects.all().filter(score__lte=user_max_score).filter(score__gte=user_min_score)
    if first_name is not None:
        result_benefactors = result_benefactors.filter(first_name__icontains=first_name)
    if last_name is not None:
        result_benefactors = result_benefactors.filter(last_name__icontains=last_name)
    if gender is not None:
        result_benefactors = result_benefactors.filter(gender__iexact=gender)
    if wanted_schedule is not None:
        schedule_filtered_ids = \
            [benefactor.id for benefactor in result_benefactors if
             benefactor.search_filter(min_date_overlap, min_required_hours, min_time_overlap, wanted_schedule)]
        result_benefactors = result_benefactors.filter(id__in=schedule_filtered_ids)
    if country is not None:
        result_benefactors = result_benefactors.filter(user__contactinfo__country__iexact=country)
    if province is not None:
        result_benefactors = result_benefactors.filter(user__contactinfo__province__iexact=province)
    if city is not None:
        result_benefactors = result_benefactors.filter(user__contactinfo__city__iexact=city)

    ability_type_ids = AbilityType.objects.find_ability_ids(ability_name, tags)
    result_ids = [benefactor.id for benefactor in result_benefactors if
                  benefactor.has_ability(ability_type_ids, ability_min_score, ability_max_score)]
    result_benefactors = result_benefactors.filter(id__in=result_ids)
    return result_benefactors


def search_charity(name=None, min_score=0, max_score=10, min_related_projects=0, max_related_projects=math.inf,
                   min_finished_projects=0, max_finished_projects=math.inf, related_benefactor=None, country=None
                   , province=None, city=None):
    result_charities = Charity.objects.all().filter(score__lte=min_score).filter(score__gte=max_score)
    filtered_ids = [charity.id for charity in result_charities if
                    max_related_projects >
                    Project.objects.related_charity_filter_count(charity) > min_related_projects and
                    max_finished_projects >
                    Project.objects.finished_charity_filter_count(charity) > min_finished_projects]
    result_charities = result_charities.filter(id__in=filtered_ids)
    if name is not None:
        result_charities = result_charities.filter(name__icontains=name)
    if country is not None:
        result_charities = result_charities.filter(user__contactinfo__country__iexact=country)
    if province is not None:
        result_charities = result_charities.filter(user__contactinfo__province__iexact=province)
    if city is not None:
        result_charities = result_charities.filter(user__contactinfo__city__iexact=city)
    if related_benefactor is not None:
        filtered_ids = [charity.id for charity in result_charities if
                        related_benefactor.charity_set.filter(pk=charity.pk).exists()]
        result_charities = result_charities.filter(id__in=filtered_ids)
    return result_charities


def filter_projects(current_projects, project_name, charity_name, benefactor, project_state):
    if project_name is not None:
        current_projects = current_projects.filter(project__project_name__iexact=project_name)
    if charity_name is not None:
        current_projects = current_projects.filter(project__charity__name=charity_name)
    if project_state is not None:
        current_projects = current_projects.filter(project__project_state__iexact=project_state)
    if benefactor is not None:
        filtered_ids = [project.id for project in current_projects if
                        benefactor.project_set.filter(pk=project.project.pk).exists()]
        current_projects = current_projects.filter(id__in=filtered_ids)
    return current_projects


def search_financial_project(project_name=None, charity_name=None, benefactor=None, project_state=None,
                             min_progress=0, max_progress=100, min_deadline_date=None, max_deadline_date=None):
    filtered_ids = [financial_project.id for financial_project in FinancialProject.objects.all() if
                    financial_project.progress_in_range(min_progress, max_progress)]
    result_financial_projects = FinancialProject.objects.all().filter(id__in=filtered_ids)
    result_financial_projects = result_financial_projects.filter(end_date__gte=min_deadline_date) \
        .filter(end_date__lte=max_deadline_date)
    return filter_projects(result_financial_projects, project_name, charity_name, benefactor, project_state)


def search_non_financial_project(project_name=None, charity_name=None, benefactor=None, project_state=None,
                                 ability_name=None, tags=None, wanted_schedule=None, min_required_hours=0,
                                 min_date_overlap=30, min_time_overlap=50, age=None, gender=None, country=None,
                                 province=None, city=None):
    result_projects = NonFinancialProject.objects.all()
    result_projects = filter_projects(result_projects, project_name, charity_name, benefactor, project_state)

    if age is not None:
        result_projects = result_projects.filter(min_age__lte=age).filter(max_age__gte=age)
    if gender is not None:
        result_projects = result_projects.filter(required_gender__iexact=gender)
    if country is not None:
        result_projects = result_projects.filter(country__iexact=country)
    if province is not None:
        result_projects = result_projects.filter(province__iexact=province)
    if city is not None:
        result_projects = result_projects.filter(city__iexact=city)
    if wanted_schedule is not None:
        filter_ids = [project.id for project in result_projects if
                      project.search_filter(min_date_overlap, min_required_hours, min_time_overlap, wanted_schedule)]
        result_projects = result_projects.filter(id__in=filter_ids)
    ability_type_ids = AbilityType.objects.find_ability_ids(ability_name, tags)
    filter_ids = [project.id for project in result_projects if project.ability_type.id in ability_type_ids]
    result_projects = result_projects.filter(id__in=filter_ids)
    return result_projects
