import datetime, json


def sub_time(time_1, time_2):
    more_hour_sub = 1 if time_1[0] > time_2[0] else 0
    result = (time_1[0] - time_2[0] - more_hour_sub, abs(time_1[1] - time_2[1]))
    return result


def add_time(time_1, time_2):
    result = (time_1[0] + time_2[0], time_1[1], time_2[1])
    if result[1] >= 60:
        result[1] -= 60
        result[0] += 1
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
            overlap_amount = sub_time(min_time_overlap(end, current_end), max_time(start, current_start))
            overlapped_hours = add_time(overlapped_hours, overlap_amount)
        if percent_time(overlapped_hours, diff) > min_time_overlap:
            all_overlapped_hours = add_time(all_overlapped_hours, overlapped_hours)
    return all_overlapped_hours


def find_all_overlapped_hours(overlapped_dateintervals, weekly_schedule, min_time_overlap=50):
    required_schedule = json.loads(weekly_schedule)
    all_overlapped_time = (0, 0)

    for weekday, times in required_schedule.items():
        for current_schedule in overlapped_dateintervals:
            all_overlapped_time += find_single_overlapped_hours(current_schedule[weekday], times, min_time_overlap)

    return all_overlapped_time


def find_overlapped_dateintervals_days(dateinterval_set, start_date, end_date):
    date_diff_days = (end_date - start_date).days
    all_overlapped_days = 0
    useful_dateintervals = []

    for dateinterval in dateinterval_set:
        if end_date < dateinterval.begin_date or start_date > dateinterval.end_date:
            continue
        else:
            overlapped_days = (min(end_date, dateinterval.end_date) - max(start_date, dateinterval.begin_date)).days
            all_overlapped_days += overlapped_days
            useful_dateintervals.append((dateinterval.from_json(), overlapped_days))

    for useful_dateinterval in useful_dateintervals:
        useful_dateinterval[1] /= all_overlapped_days

    return useful_dateintervals, all_overlapped_days / date_diff_days


def has_matched_schedule(min_date_overlap, min_required_hours, min_time_overlap, schedule,
                  dateinterval_set=None, dateinterval=None):
    wanted_start_date = schedule[0]
    wanted_end_date = schedule[1]
    weekly_schedule = schedule[2]

    if dateinterval is not None:
        dateinterval_set = [dateinterval]

    (overlapped_dateintervals, overlapped_days) = find_overlapped_dateintervals_days(dateinterval_set,
                                                                                     wanted_start_date,
                                                                                     wanted_end_date)
    if overlapped_days < min_date_overlap:
        return False
    overlapped_hours = find_all_overlapped_hours(overlapped_dateintervals, weekly_schedule, min_time_overlap)
    return True if overlapped_hours == max_time(overlapped_hours, min_required_hours) else False
