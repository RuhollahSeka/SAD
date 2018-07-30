import datetime


def add_weekday_report(report, weekday_times):
    for time in weekday_times:
        report += 'از ' + str(datetime.time(time[0], time[1])) + ' تا ' + str(datetime.time(time[2], time[3])) + '\n'
    return report


def create_non_financial_project_report(nonfinancialproject):
    report = ''
    report += 'نام پروژه: ' + nonfinancialproject.project.project_name + '\n'
    report += 'نام سازمان:' + ' ' + nonfinancialproject.project.charity.name + '\n'
    report += '' + nonfinancialproject.ability_type.name + '\n'
    if nonfinancialproject.project.benefactors is not None and len(nonfinancialproject.project.benefactors) != 0:
        benefactor = nonfinancialproject.project.benefactors[0]
        report += '' + benefactor.first_name + ' ' + benefactor.last_name
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
    report += 'نام سازمان:' + ' ' + financialproject.project.charity.name + '\n'
    report += '' + str(len(financialproject.project.benefactors)) + '\n'
    report += '' + str(financialproject.current_money)
    report += '' + str(financialproject.target_money)
    report += 'جزییات کمک های نقدی:' + '\n'
    for financialcontribution in financialproject.financialcontribution_set:
        benefactor = financialcontribution.benefactor
        report += '' + benefactor.first_name + ' ' + benefactor.last_name + '\n'
        report += '' + str(financialcontribution.money) + '\n'
        report += '\n'
    report += '' + str(financialproject.start_date) + '\n'
    report += '' + str(financialproject.end_date) + '\n'
    pass
