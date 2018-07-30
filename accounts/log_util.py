def add_weekday_report(report, weekday_times):
    pass


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
        report += '' + nonfinancialproject.min_age
        report += '' + nonfinancialproject.max_age
        report += '' + nonfinancialproject.required_gender
        report += '' + nonfinancialproject.country
        report += '' + nonfinancialproject.province
        report += '' + nonfinancialproject.city
        report += '' + nonfinancialproject.dateinterval.begin_date
        report += '' + nonfinancialproject.dateinterval.end_date
        weekly_schedule = nonfinancialproject.dateinterval.from_json()
        report += 'برنامه هفتگی:' + '\n'
        report += 'شنبه:' + '\n'
        add_weekday_report(report, weekly_schedule.get('sat'))
    pass


def create_financial_project_report(project):
    pass
