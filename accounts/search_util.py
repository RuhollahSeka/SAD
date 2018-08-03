import datetime, json, re


def sub_time(time_1, time_2):
    more_hour_sub = 1 if time_1[1] < time_2[1] else 0
    result = (time_1[0] - time_2[0] - more_hour_sub,
              time_1[1] - time_2[1] if more_hour_sub == 0 else time_1[1] + time_2[1] - 60)
    return result


def add_time(time_1, time_2, const=1):
    minutes = time_2[0] * 60 + time_2[1]
    minutes *= const
    time_2 = divmod(minutes, 60)

    result = (time_1[0] + time_2[0], time_1[1] + time_2[1])
    if result[1] >= 60:
        result = (result[0] + 1, result[1] - 60)
    return result


def max_time(time_1, time_2):
    if time_1[0] > time_2[0]:
        return time_1
    elif time_1[0] == time_2[0]:
        if time_1[1] > time_2[1]:
            return time_1
        return time_2
    else:
        return time_2


def min_time(time_1, time_2):
    if time_1[0] < time_2[0]:
        return time_1
    elif time_1[0] == time_2[0]:
        if time_1[1] < time_2[1]:
            return time_1
        return time_2
    else:
        return time_2


def percent_time(time_1, time_2):
    first_minutes = time_1[0] * 60 + time_1[1]
    second_minutes = time_2[0] * 60 + time_2[1]
    if second_minutes == 0:
        return 100
    return 100 * (first_minutes / second_minutes)


def find_single_overlapped_hours(current_times, required_times, min_time_overlap):
    all_overlapped_hours = (0, 0)

    for required_time in required_times:
        overlapped_hours = (0, 0)
        start = (required_time[0], required_time[1])
        end = (required_time[2], required_time[3])
        diff = sub_time(end, start)
        for current_time in current_times:
            current_start = (current_time[0], current_time[1])
            current_end = (current_time[2], current_time[3])
            if current_end == min(current_end, start) or current_start == max(current_start, end):
                continue
            overlap_amount = sub_time(min_time(end, current_end), max_time(start, current_start))
            overlapped_hours = add_time(overlapped_hours, overlap_amount)
        if percent_time(overlapped_hours, diff) > min_time_overlap:
            all_overlapped_hours = add_time(all_overlapped_hours, overlapped_hours)
    return all_overlapped_hours


def find_all_overlapped_hours(overlapped_dateintervals, weekly_schedule, min_time_overlap=50):
    # required_schedule = json.loads(weekly_schedule)
    all_overlapped_time = (0, 0)

    for weekday, times in weekly_schedule.items():
        for current_dateinterval in overlapped_dateintervals:
            current_schedule = current_dateinterval[0]
            current_times = current_schedule.get(weekday)
            if current_times is None:
                continue
            const = current_dateinterval[1]
            all_overlapped_time = add_time(all_overlapped_time, find_single_overlapped_hours(current_times,
                                                                                             times, min_time_overlap),
                                           const)

    return all_overlapped_time


def find_overlapped_dateintervals_days(dateinterval_set, start_date, end_date):
    date_diff_days = (end_date - start_date).days
    all_overlapped_days = 0
    useful_dateintervals = []

    for dateinterval in dateinterval_set.all():
        if end_date < dateinterval.begin_date or start_date > dateinterval.end_date:
            continue
        else:
            overlapped_days = (min(end_date, dateinterval.end_date) - max(start_date, dateinterval.begin_date)).days
            all_overlapped_days += overlapped_days
            useful_dateintervals.append([dateinterval.from_json(), overlapped_days])

    if all_overlapped_days == 0:
        return useful_dateintervals, 0

    for useful_dateinterval in useful_dateintervals:
        useful_dateinterval[1] /= all_overlapped_days

    return useful_dateintervals, all_overlapped_days * 100 / date_diff_days, date_diff_days


def has_matched_schedule(min_date_overlap, min_required_hours, min_time_overlap, schedule,
                         dateinterval_set=None, dateinterval=None):
    wanted_start_date = schedule[0]
    wanted_end_date = schedule[1]
    weekly_schedule = schedule[2]

    if dateinterval is not None:
        dateinterval_set = [dateinterval]

    (overlapped_dateintervals, overlapped_days, schedule_day_diff) = find_overlapped_dateintervals_days(dateinterval_set,
                                                                                     wanted_start_date,
                                                                                     wanted_end_date)
    if overlapped_days < min_date_overlap:
        return False, 0, 0
    overlapped_hours = find_all_overlapped_hours(overlapped_dateintervals, weekly_schedule, min_time_overlap)
    if overlapped_hours[0] >= min_required_hours:
        weekly_overlap_minutes = overlapped_hours[0] * 60 + overlapped_hours[1]
        return True, overlapped_days * schedule_day_diff / 100, weekly_overlap_minutes
    return False, 0, 0


def create_query_schedule(ui_schedule):
    schedule = json.loads(ui_schedule)
    result = {}
    for key, value in schedule.items():
        result[key] = []
        intervals = value.split(',')
        for interval in intervals:
            result[key].append(re.split('[-:]+', interval))
    return result
