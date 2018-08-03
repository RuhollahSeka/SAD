from django.test import TestCase
from projects.models import *
from accounts.models import *
import json, datetime


# Create your tests here.

def create_user(username='pkms', password='password', email='r.sekaleshfar@gmail.com', is_benefactor=False,
                is_charity=False, description=None,
                country='iran', province='tehran', city='tehran', postal_code='1234567810', address='nowhere',
                phone_number='09123456789'):
    contact_info = ContactInfo(country=country, province=province, city=city, postal_code=postal_code, address=address,
                               phone_number=phone_number)
    contact_info.save()
    user = User(username=username, password=password, is_benefactor=is_benefactor, is_charity=is_charity, email=email,
                contact_info=contact_info, description=description)
    user.save()
    return user, contact_info


def create_benefactor(username='pkms', password='password', description=None, email='r.sekaleshfar@gmail.com',
                      country='iran', province='tehran',
                      city='tehran', postal_code='1234567810', address='nowhere', phone_number='09123456789',
                      first_name='ruhollah', last_name='sekaleshfar', gender='male', age=20, credit=0):
    (user, contact_info) = create_user(username=username, password=password, is_benefactor=True, email=email,
                                       description=description, country=country, province=province, city=city,
                                       postal_code=postal_code, address=address, phone_number=phone_number)
    benefactor = Benefactor(user=user, first_name=first_name, last_name=last_name, gender=gender, age=age,
                            credit=credit)
    benefactor.save()
    return benefactor, user, contact_info


def create_dateinterval(start_date=datetime.date(2018, 1, 1), end_date=datetime.date(2018, 1, 1), schedule=None):
    if schedule is None:
        schedule = {
            'sat': [[9, 30, 12, 30], [14, 0, 16, 0]],
            'mon': [[10, 45, 13, 15]],
            'fri': [[17, 30, 22, 0], [1, 15, 5, 0], [12, 0, 15, 0]]
        }

    dateinterval = DateInterval(begin_date=start_date, end_date=end_date)
    dateinterval.to_json(schedule)
    return dateinterval


def create_charity(username='pk-charity', password='password', email='azed.lol@gmail.com', description=None,
                   country='iran', province='tehran',
                   city='tehran', postal_code='1234567810', address='nowhere', phone_number='09123456789',
                   charity_name='my charity'):
    (user, contact_info) = create_user(username=username, password=password, is_charity=True, email=email,
                                       description=description, country=country, province=province, city=city,
                                       postal_code=postal_code, address=address, phone_number=phone_number)
    charity = Charity(user=user, name=charity_name)
    charity.save()
    return charity, user, contact_info


def create_project(charity, type, project_name='my project', description='this is my project', project_state='open'):
    project = Project(charity=charity, type=type, project_name=project_name, description=description,
                      project_state=project_state)
    project.save()
    return project


def create_non_financial_project(ability_type, charity, project_name='my project', description='this is my project',
                                 project_state='open', min_age=0, max_age=200, required_gender=None, country=None,
                                 province=None, city=None):
    project = create_project(charity, 'non-financial', project_name, description, project_state)
    non_financial_project = NonFinancialProject(project=project, ability_type=ability_type, min_age=min_age,
                                                max_age=max_age, required_gender=required_gender, country=country,
                                                province=province, city=city)
    non_financial_project.save()
    return non_financial_project, project


def create_financial_project(charity, target_money, project_name='my project', description='this is my project',
                             project_state='open', current_money=0, start_date=datetime.date(2018, 1, 1),
                             end_date=datetime.date(2018, 1, 1)):
    project = create_project(charity, 'financial', project_name, description, project_state)
    financial_project = FinancialProject(project=project, target_money=target_money, current_money=current_money,
                                         start_date=start_date, end_date=end_date)
    financial_project.save()
    return financial_project, project


def create_ability_tag(name, description):
    tag = AbilityTag(name=name, description=description)
    tag.save()
    return tag


def create_ability_type(name, description, tags=None):
    ability_type = AbilityType(name=name, description=description)
    ability_type.save()
    for tag in tags:
        ability_type.tags.add(tag)
    return ability_type


class SearchTestCase(TestCase):
    def setUp(self):
        (benefactor, user, contact_info) = create_benefactor()
        dateinterval = create_dateinterval(start_date=datetime.date(2018, 1, 5), end_date=datetime.date(2018, 3, 25))
        dateinterval.benefactor = benefactor
        dateinterval.save()

        dateinterval = create_dateinterval(start_date=datetime.date(2018, 3, 26), end_date=datetime.date(2018, 5, 1))
        dateinterval.benefactor = benefactor
        dateinterval.save()

        (charity, user, contact_info) = create_charity()
        tag = create_ability_tag('tag-1', 'cool tag')
        ability_type = create_ability_type('type-1', 'cool type', [tag])
        (non_financial_project, project) = create_non_financial_project(ability_type, charity)
        non_financial_project.save()

    def test_benefactor_search_schedule_days(self):
        dateinterval = create_dateinterval(start_date=datetime.date(2018, 1, 1), end_date=datetime.date(2018, 1, 5))
        start_date = dateinterval.begin_date
        end_date = dateinterval.end_date
        schedule = dateinterval.from_json()
        results = search_benefactor([start_date, end_date, schedule])
        self.assertEqual(len(results), 0)

        dateinterval = create_dateinterval(start_date=datetime.date(2018, 1, 5), end_date=datetime.date(2018, 1, 26))
        start_date = dateinterval.begin_date
        end_date = dateinterval.end_date
        schedule = dateinterval.from_json()
        results = search_benefactor([start_date, end_date, schedule])
        self.assertEqual(len(results), 1)

    def test_benefactor_search_schedule_hours(self):
        start_date = datetime.date(2018, 1, 5)
        end_date = datetime.date(2018, 1, 10)
        schedule = {
            'tue': [],
            'thur': [[0, 0, 23, 45]]
        }
        results = search_benefactor([start_date, end_date, schedule], min_required_hours=4)
        self.assertEqual(len(results), 0)

        schedule = {
            'sat': [[9, 30, 12, 30]],
            'mon': [[10, 45, 11, 45]]
        }
        results = search_benefactor([start_date, end_date, schedule], min_required_hours=4)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][5], 5)
        self.assertEqual(results[0][6], 240)

        schedule = {
            'sat': [[9, 30, 12, 30]],
            'mon': [[10, 45, 11, 45]]
        }
        results = search_benefactor([start_date, end_date, schedule], min_required_hours=5)
        self.assertEqual(len(results), 0)

        schedule = {
            'sat': [[9, 30, 12, 30]],
            'mon': [[10, 45, 11, 45]]
        }
        results = search_benefactor([start_date, end_date, schedule], min_required_hours=4)
        self.assertEqual(len(results), 1)

        schedule = {
            'sat': [[15, 30, 17, 0]],
            'mon': [[10, 45, 11, 15]]
        }
        results = search_benefactor([start_date, end_date, schedule], min_required_hours=2)
        self.assertEqual(len(results), 0)

    def test_delete_user(self):
        user = User.objects.filter(is_benefactor=True)[0]
        user.delete()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Benefactor.objects.count(), 0)

        user = User.objects.filter(is_charity=True)[0]
        user.delete()
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Charity.objects.count(), 0)

        self.assertEqual(AbilityTag.objects.count(), 1)
        self.assertEqual(AbilityType.objects.count(), 1)

        self.assertEqual(ContactInfo.objects.count(), 0)

    def test_non_financial_project_search_schedule(self):
        user = User.objects.filter(username__iexact='pkms')[0]

        non_financial_project = NonFinancialProject.objects.filter(project__project_name__iexact='my project')[0]
        start_date = datetime.date(2018, 3, 24)
        end_date = datetime.date(2018, 3, 30)
        schedule = {
            'fri': [[14, 0, 17, 0]]
        }
        dateinterval = create_dateinterval(start_date, end_date, schedule)
        dateinterval.non_financial_project = non_financial_project
        dateinterval.save()
        results = search_non_financial_project(user_id=user.id)
        self.assertEqual(len(results), 1)

        results = search_non_financial_project(user_id=user.id, min_required_hours=1)
        self.assertEqual(len(results), 0)

        schedule = {
            'fri': [[12, 0, 15, 0]]
        }
        dateinterval.to_json(schedule)
        dateinterval.save(update_fields=['week_schedule'])
        results = search_non_financial_project(user_id=user.id, min_required_hours=3)
        self.assertEqual(len(results), 1)

    def test_non_financial_project_search_ability(self):
        results = search_non_financial_project(tags=['tag-1'])
        self.assertEqual(len(results), 1)

        results = search_non_financial_project(ability_name='type')
        self.assertEqual(len(results), 1)

        results = search_non_financial_project(tags='lel')
        self.assertEqual(len(results), 0)

        results = search_non_financial_project(ability_name='ability')
        self.assertEqual(len(results), 0)

    def test_delete_non_financial_project(self):
        project = Project.objects.all()[0]
        project.delete()
        self.assertEqual(Project.objects.count(), 0)
        self.assertEqual(NonFinancialProject.objects.count(), 0)
        self.assertEqual(AbilityType.objects.count(), 1)
        self.assertEqual(AbilityTag.objects.count(), 1)
