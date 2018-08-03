from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.search_util import *
import datetime, json


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
    name = models.CharField(max_length=256, default='')
    description = models.CharField(max_length=1024, default='')

    def get(self, *args, **kwargs):
        try:
            ans = self.objects.get(*args, **kwargs)
            return ans
        except:
            return None


class AbilityType(models.Model):
    name = models.CharField(max_length=256, default='')
    description = models.CharField(max_length=2048, default='')
    tags = models.ManyToManyField(AbilityTag)
    objects = AbilityTypeManager()

    def get_tag_strings(self):
        return [tag.name for tag in self.tags.all()]

    def get(self, *args, **kwargs):
        try:
            ans = self.objects.get(*args, **kwargs)
            return ans
        except:
            return None

    def __str__(self):
        return self.name


class ContactInfo(models.Model):
    country = models.CharField(max_length=30, null=True)
    province = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    postal_code = models.CharField(max_length=30, null=True)
    address = models.CharField(max_length=500, null=True)
    phone_number = models.CharField(max_length=20, null=True)

    def get(self, *args, **kwargs):
        try:
            ans = self.objects.get(*args, **kwargs)
            return ans
        except:
            return None


class User(AbstractUser):
    is_charity = models.BooleanField(default=False)
    is_benefactor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    admin_approved = models.BooleanField(default=False)
    contact_info = models.OneToOneField(ContactInfo, on_delete=models.DO_NOTHING, default='')
    description = models.CharField(max_length=2048, default='', null=True)
    # TODO set initial recover string when creating the user
    email_recover_string = models.CharField(max_length=64, default='')
    activation_string = models.CharField(max_length=64, default='')

    def get(self, *args, **kwargs):
        try:
            ans = self.objects.get(*args, **kwargs)
            return ans
        except:
            return None

    def __str__(self):
        return 'Username: ' + self.username


class Benefactor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default='')

    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=100, default='')
    gender = models.CharField(max_length=40, null=True)
    age = models.IntegerField(null=True)
    credit = models.FloatField(default=0)

    def get(self, *args, **kwargs):
        try:
            ans = self.objects.get(*args, **kwargs)
            return ans
        except:
            return None

    def search_filter(self, min_date_overlap, min_required_hours, min_time_overlap, schedule):
        return has_matched_schedule(min_date_overlap, min_required_hours, min_time_overlap, schedule,
                                    dateinterval_set=self.dateinterval_set)

    def has_ability(self, ability_type_ids, ability_min_score, ability_max_score):
        if self.ability_set.count() == 0:
            return True

        for ability in self.ability_set.all():
            if ability.ability_type.id in ability_type_ids and ability_min_score < ability.score < ability_max_score:
                return True
        return False

    def has_score(self, min_score, max_score):
        score = self.calculate_score()
        if str(score) == '-':
            if min_score == 0:
                return True
            return False
        return min_score < score < max_score

    def calculate_score(self):
        score = 0
        count = 0
        score_list = BenefactorScore.objects.filter(benefactor=self)
        for ability in self.ability_set.all():
            filtered_score_list = score_list.filter(ability_type=ability.ability_type)
            count += filtered_score_list.count()
            for score_obj in filtered_score_list.all():
                score += score_obj.score
        if count <= 0:
            return '-'
        return score / count


class Ability(models.Model):
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, default='')
    ability_type = models.ForeignKey(AbilityType, on_delete=models.CASCADE, default='')
    score = models.IntegerField(default=-1)
    description = models.CharField(max_length=512, default='')


class Charity(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, default='')
    name = models.CharField(max_length=200)
    benefactor_history = models.ManyToManyField(Benefactor)

    def get(self, *args, **kwargs):
        try:
            ans = self.objects.get(*args, **kwargs)
            return ans
        except:
            return None

    def calculate_score(self):
        score = 0
        count = 0
        score_list = CharityScore.objects.filter(charity=self)
        for score_obj in score_list:
            count += 1
            score += score_obj.score
        if count <= 0:
            return '-'
        return score / count


class Notification(models.Model):
    type = models.CharField(max_length=128, default='')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    date_time = models.DateTimeField(default=datetime.datetime(2018, 1, 1, 0, 0))
    description = models.CharField(max_length=2048, null=True)

    def get(self, *args, **kwargs):
        try:
            ans = self.objects.get(*args, **kwargs)
            return ans
        except:
            return None


class AbilityRequest(models.Model):
    type = models.CharField(max_length=64, default='')
    name = models.CharField(max_length=64, default='')
    description = models.CharField(max_length=2048, null=True)

    def get(self, *args, **kwargs):
        try:
            ans = self.objects.get(*args, **kwargs)
            return ans
        except:
            return None



class BenefactorComment(models.Model):
    commenter = models.ForeignKey(Charity, on_delete=models.CASCADE, default='')
    commented = models.ForeignKey(Benefactor, on_delete=models.CASCADE, default='')
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE, default='')
    comment_string = models.CharField(max_length=2048, default='')
    date_time = models.DateTimeField(auto_now=True)


class CharityComment(models.Model):
    commenter = models.ForeignKey(Benefactor, on_delete=models.CASCADE, default='')
    commented = models.ForeignKey(Charity, on_delete=models.CASCADE, default='')
    comment_string = models.CharField(max_length=2048, default='')
    date_time = models.DateTimeField(auto_now=True)

    @staticmethod
    def get(self, *args, **kwargs):
        try:
            ans = self.objects.get(*args, **kwargs)
            return ans
        except:
            return None


class BenefactorScore(models.Model):
    ability = models.ForeignKey(Ability, on_delete=models.CASCADE, default='')
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, default='')
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE, default='')
    score = models.IntegerField(default=-1)

    def get(self, *args, **kwargs):
        try:
            ans = self.objects.get(*args, **kwargs)
            return ans
        except:
            return None

    class Meta:
        unique_together = (('ability', 'benefactor', 'charity'),)


class CharityScore(models.Model):
    benefactor = models.ForeignKey(Benefactor, on_delete=models.CASCADE, default='')
    charity = models.ForeignKey(Charity, on_delete=models.CASCADE, default='')
    score = models.IntegerField(default=-1)

    def get(self, *args, **kwargs):
        try:
            ans = self.objects.get(*args, **kwargs)
            return ans
        except:
            return None

    class Meta:
        unique_together = (('benefactor', 'charity'),)


class GeneralRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    description = models.CharField(max_length=1024)

