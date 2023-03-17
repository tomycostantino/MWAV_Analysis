import pandas as pd
import typing
from datetime import datetime
import re

regular_expresions = {
    'sms_date_regex': r'\w{3}, \d{1,2} \w{3} at \d{1,2}:\d{2} [ap]m',
    'date_regex': r'\d{2}/\d{2}/\d{4}',
    'start_time_regex': r'\Start time set: ',
    'asked_for_regex': r'asked for: ',
    'swiped_at_regex': r'swiped at: ',
    'end_time_regex': r'End time set: ',
    'base_hours_regex': r'Hours: \d{1,2}.\d{1,2}',
    'ot1_regex': r'OT1: \d{1}.\d{1,2}',
    'ot2_regex': r'OT2: \d{1}.\d{1,2}',
    'sat_regex': r'Sat: \d{1}.\d{1,2}',
    'sun_regex': r'Sun: \d{1}.\d{1,2}',
    'tips_regex': r'Tips: $\d{1,2,3}',
}


def read_file(filename: str) -> str:
    '''
    Read file line by line
    '''

    file = open(filename, 'r')

    lines = file.readlines()

    lines_str = ""

    for line in lines:
        lines_str += line

    return lines_str


def get_regex_span(regex, lines: str):
    '''
    Will return the span of the regex passed if found
    '''
    if re.search(regex, lines) is not None:
        return re.search(regex, lines).span()
    else:
        raise BaseException("Cannot find regex")


def match_date_to_sms(lines: str):
    '''
    This function splits the messages by the regular expresion of the date and
    parses the data into a dataframe
    '''

    spans = []
    for i in re.finditer(regular_expresions['sms_date_regex'], lines):
        spans.append(i.span())

    dates = []
    messages = []

    for idx, span in enumerate(spans):
        if idx + 1 >= len(spans):
            break

        # slice str to capture the date
        dates.append(lines[span[0]:span[1]])
        # slice str to capture the sms that matches the date
        messages.append(lines[span[1]:spans[idx + 1][0]])

    data = {
        'date': dates,
        'message': messages,
    }

    return pd.DataFrame(data)


def drop_empty_lines(df: pd.DataFrame) -> pd.DataFrame:
    '''
    This function checks for messages that contain '\n' as there is some present,
    drops them and then returns the new dataframe
    '''

    to_drop = []
    for idx, sms in enumerate(df['message']):
        if sms == '\n':
            to_drop.append(idx)

    return df.drop(to_drop)


def find_start_end_time(df: pd.DataFrame) -> typing.List[str]:
    target_sms = []

    for sms in df['message']:
        if re.search(regular_expresions['date_regex'], sms):
            target_sms.append(sms)

    return target_sms


def same_day_sms(sms1: str, sms2: str):
    return True if sms1[re.search(regular_expresions['date_regex'], sms1).span()[0]:
                        re.search(regular_expresions['date_regex'], sms1).span()[1]] == \
                   sms2[re.search(regular_expresions['date_regex'], sms2).span()[0]:
                        re.search(regular_expresions['date_regex'], sms2).span()[1]] \
        else False


def get_date(sms):
    date_format = "%d/%m/%Y"
    date_only = "%d/%m/%Y"
    date_obj = datetime.strptime(sms[re.search(regular_expresions['date_regex'], sms).span()[0]:
                                     re.search(regular_expresions['date_regex'], sms).span()[1]],
                                 date_format)
    return datetime.strftime(date_obj, date_only)


def remove_newline_tag(sms: str):
    string = ''
    for s in sms.split('\n'):
        string += s
    return string


def get_start_time(sms):
    time_str = sms[re.search(regular_expresions['start_time_regex'], sms).span()[1]:
                   re.search(regular_expresions['start_time_regex'], sms).span()[1] + 8]
    try:
        time_format = "%H:%M:%S"
        time_obj = datetime.strptime(time_str, time_format)
        return time_obj.time()
    except Exception as e:
        print('This is the value of the text found in the sms:' + time_str + '\nAnd this is the exception:', e)


def get_asked_for(sms):
    if re.search(regular_expresions['asked_for_regex'], sms):
        time_str = sms[re.search(regular_expresions['asked_for_regex'], sms).span()[1]:
                       re.search(regular_expresions['asked_for_regex'], sms).span()[1] + 8]
    else:
        time_str = sms[re.search(regular_expresions['swiped_at_regex'], sms).span()[1]:
                       re.search(regular_expresions['swiped_at_regex'], sms).span()[1] + 8] if re.search(
            regular_expresions['swiped_at_regex'], sms) else '00:00:00'
    try:
        time_format = "%H:%M:%S"
        time_obj = datetime.strptime(time_str, time_format)
        return time_obj.time()
    except Exception as e:
        print('This is the value of the text found in the sms:' + time_str + '\nAnd this is the exception:', e)


def get_swiped_at(sms):
    if re.search(regular_expresions['swiped_at_regex'], sms):
        time_str = sms[re.search(regular_expresions['swiped_at_regex'], sms).span()[1]:
                       re.search(regular_expresions['swiped_at_regex'], sms).span()[1] + 8]
    else:
        time_str = '00:00:00'

    try:
        time_format = "%H:%M:%S"
        time_obj = datetime.strptime(time_str, time_format)
        return time_obj.time()
    except Exception as e:
        print('This is the value of the text found in the sms:' + time_str + '\nAnd this is the exception:', e)


def get_end_time(sms):
    if re.search(regular_expresions['end_time_regex'], sms):
        time_str = sms[re.search(regular_expresions['end_time_regex'], sms).span()[1]:
                       re.search(regular_expresions['end_time_regex'], sms).span()[1] + 8]

    else:
        time_str = ''

    try:
        time_format = "%H:%M:%S"
        time_obj = datetime.strptime(time_str, time_format)
        return time_obj.time()
    except Exception as e:
        print('This is the value of the text found in the sms:' + time_str + '\nAnd this is the exception:', e)


def get_base_hours(sms):
    time_str = ''
    try:

        if re.search(regular_expresions['end_time_regex'], sms):
            time_str = sms[re.search(regular_expresions['base_hours_regex'], sms).span()[0]+7:
                           re.search(regular_expresions['base_hours_regex'], sms).span()[1]]
            return float(time_str)
    except Exception as e:
        print('This is the value of the text found in the sms:' + time_str + '\nAnd this is the exception:', e)

    else:
        return 0.0


def create_dataset(filename: str):
    '''
    Will create clean dataset
    '''

    # columns dataset will contain
    date = []
    start_time = []
    asked_for = []
    swiped_at = []
    end_time = []
    base_hours = []
    sat = []
    sun = []
    OT1 = []
    OT2 = []
    tips = []

    # Open txt file
    lines = read_file(filename)

    # create partial dataframe
    temp_df = match_date_to_sms(lines)
    temp_df = drop_empty_lines(temp_df)

    to_split = find_start_end_time(temp_df)

    # create sub-dataframe
    for idx, sms in enumerate(to_split):
        if idx + 1 >= len(to_split):
            break

        if same_day_sms(sms, to_split[idx + 1]):
            date.append(get_date(sms))
            start_time.append(get_start_time(remove_newline_tag(sms)))
            asked_for.append(get_asked_for(remove_newline_tag(sms)))
            swiped_at.append(get_swiped_at(remove_newline_tag(sms)))
            end_time.append(get_end_time(remove_newline_tag(to_split[idx+1])))
            base_hours.append(get_base_hours(remove_newline_tag(to_split[idx+1])))

    data = {
        'start_time': start_time,
        'asked_for': asked_for,
        'swiped_at': swiped_at,
        'end_time': end_time,
        'base_hours': base_hours,
    }

    return pd.DataFrame(data, index=date)


def main():
    print(create_dataset('messages.txt').tail(20))


if __name__ == '__main__':
    main()
