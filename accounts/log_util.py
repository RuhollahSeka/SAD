import datetime
from projects.models import Log


class Logger:
    @staticmethod
    def create_account(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='create_account', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'New Account Created for ' + str(first_actor) + ' at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def account_update(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='account_update', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'Account Updated by ' + str(first_actor) + ' at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def login(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='login', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'User ' + str(first_actor) + ' Logged Into Account at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def logout(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='login', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'User ' + str(first_actor) + ' Logged Out of Account at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def request_submit(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='request_submit', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'User ' + str(first_actor) + ' Has Submitted a Request for Collaboration Project ' + log_project + \
                          ' to ' + str(second_actor) + ' at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def request_new_ability_type(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='request_new_ability_type', first_actor=first_actor,
                                 second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'User ' + str(first_actor) + ' Has Requested a New Ability Type at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def request_new_ability_tag(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='request_new_ability_tag', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'User ' + str(first_actor) + ' Has Requested a New Ability Tag at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def create_new_project(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='create_new_project', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'Charity ' + str(first_actor) + ' Has Created a New Project at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def update_project(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='update_project', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'Charity ' + str(first_actor) + ' Has Updated a Project at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def financial_contribution(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='financial_contribution', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'User ' + str(first_actor) + ' Logged Out of Account at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def accept_request(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='accept_request', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'User ' + str(first_actor) + ' Has Accepted User ' + str(second_actor) + '\'s Request on ' + log_project \
                          + ' at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def deny_request(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='deny_request', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'User ' + str(first_actor) + ' Has Denied User ' + str(second_actor) + '\'s Request on ' + log_project \
                          + ' at ' + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def submit_score(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='submit_score', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'User ' + str(first_actor) + ' Has Submit a Score for User ' + str(second_actor) + ' at ' \
                          + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def submit_comment(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='submit_comment', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'User ' + str(first_actor) + ' Has Submit a Comment for User ' + str(second_actor) + ' at ' \
                          + str(datetime.datetime.now())
        log.save()

    @staticmethod
    def add_ability_benefactor(first_actor, second_actor, log_project):
        log = Log.objects.create(log_type='add_ability_benefactor', first_actor=first_actor, second_actor=second_actor,
                                 date_time=datetime.datetime.now(), log_project=log_project)
        log.description = 'Benefactor ' + str(first_actor) + ' Has Added a New Ability to His/Her Ability List at ' + str(
            datetime.datetime.now())
        log.save()

    
    create_log = {
        'create_account': create_account,
        'account_update': account_update,
        'login': login,
        'logout': logout,
        'request_submit': request_submit,
        'request_new_ability_type': request_new_ability_type,
        'request_new_ability_tag': request_new_ability_tag,
        'create_new_project': create_new_project,
        'update_project': update_project,
        'financial_contribution': financial_contribution,
        'accept_request': accept_request,
        'deny_request': deny_request,
        'submit_score': submit_score,
        'add_ability_benefactor': add_ability_benefactor,
        'submit_comment': submit_comment,
    }


def add_weekday_report(report, weekday_times):
    for time in weekday_times:
        report += 'از ' + str(datetime.time(time[0], time[1])) + ' تا ' + str(datetime.time(time[2], time[3])) + '\n'
    return report


def create_non_financial_project_report(nonfinancialproject):
    report = ''
    report += 'نام پروژه: ' + nonfinancialproject.project.project_name + '\n'
    report += 'نام سازمان:' + ' ' + nonfinancialproject.project.charity.name + '\n'
    report += 'نام توانمندی مورد نیاز:' + nonfinancialproject.ability_type.name + '\n'
    if nonfinancialproject.project.benefactors is not None and len(nonfinancialproject.project.benefactors) != 0:
        benefactor = nonfinancialproject.project.benefactors[0]
        report += 'نیکوکار:' + benefactor.first_name + ' ' + benefactor.last_name
    else:
        report += 'نیکوکاری این پروژه را قبول نکرده است.' + '\n'
        report += 'شرایط مورد نیاز این پروژه:' + '\n'
        report += 'حداقل سن: ' + nonfinancialproject.min_age
        report += 'حداکثر سن: ' + nonfinancialproject.max_age
        if nonfinancialproject.required_gender is not None:
            report += 'جنسیت: ' + nonfinancialproject.required_gender
        if nonfinancialproject.country is not None:
            report += 'کشور: ' + nonfinancialproject.country
        if nonfinancialproject.province is not None:
            report += 'استان: ' + nonfinancialproject.province
        if nonfinancialproject.city is not None:
            report += 'شهر: ' + nonfinancialproject.city
        report += 'تاریخ شروع: ' + nonfinancialproject.dateinterval.begin_date
        report += 'تاریخ پایان: ' + nonfinancialproject.dateinterval.end_date
        weekly_schedule = nonfinancialproject.dateinterval.from_json()
        report += 'برنامه هفتگی:' + '\n'
        report += 'شنبه:' + '\n'
        report = add_weekday_report(report, weekly_schedule.get('sat'))
        report += 'یک شنبه:' + '\n'
        report = add_weekday_report(report, weekly_schedule.get('sun'))
        report += 'دو شنبه:' + '\n'
        report = add_weekday_report(report, weekly_schedule.get('mon'))
        report += 'سه شنبه:' + '\n'
        report = add_weekday_report(report, weekly_schedule.get('tue'))
        report += 'چهار شنبه:' + '\n'
        report = add_weekday_report(report, weekly_schedule.get('wed'))
        report += 'پنج شنبه:' + '\n'
        report = add_weekday_report(report, weekly_schedule.get('thur'))
        report += 'جمعه:' + '\n'
        report = add_weekday_report(report, weekly_schedule.get('fri'))
    return report


def create_financial_project_report(financialproject):
    report = ''
    report += 'نام پروژه: ' + financialproject.project.project_name + '\n'
    report += 'نام سازمان: ' + ' ' + financialproject.project.charity.name + '\n'
    report += 'تعداد نیکوکارانی که تا به اینجا، کمک نقدی کرده اند: ' + str(
            len(financialproject.project.benefactors)) + '\n'
    report += 'حجم کمک نقدی تا به اینجا: ' + str(financialproject.current_money)
    report += 'مقدار کمک نقدی مورد نیاز: ' + str(financialproject.target_money)
    report += 'جزییات کمک های نقدی: ' + '\n'
    for financialcontribution in financialproject.financialcontribution_set:
        benefactor = financialcontribution.benefactor
        report += 'نام نیکوکار: ' + benefactor.first_name + ' ' + benefactor.last_name + '\n'
        report += 'مقدار کمک نقدی: ' + str(financialcontribution.money) + '\n'
        report += '\n'
    report += 'تاریخ شروع: ' + str(financialproject.start_date) + '\n'
    report += 'تاریخ پایان: ' + str(financialproject.end_date) + '\n'
    return report
