import pandas as pd
import typing
from datetime import datetime
import re


regular_expresions = {
    'sms_date_regex': r'\w{3}, \d{1,2} \w{3} at \d{1,2}:\d{2} [ap]m',
    'date_regex': r'\d{2}/\d{2}/\d{4}',
    'start_time_regex': r'\Start time set: \d{2}:\d{2}:\d{2}',
    'asked_for_regex': r'asked for: \d{2}:\d{2}:\d{2}',
    'swiped_at_regex': r'swiped at:',
    'end_time_regex': r'End time set: \d{2}:\d{2}:\d{2}',
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


def get_regex_spans(regex, lines: str) -> typing.List[tuple]:
    '''
    Will return the span of the regex passed if found
    '''
    
    spans = []
    for i in re.finditer(regex, lines):
        spans.append(i.span())
    return spans


def match_date_to_sms(lines: str) -> pd.DataFrame:
    '''
    This function splits the messages by the regular expresion of the date and
    parses the data into a dataframe
    '''
    
    spans = get_regex_spans(regular_expresions['sms_date_regex'],lines)
    dates = []
    messages = []
    
    for idx, span in enumerate(spans):
        if idx+1 >= len(spans):
            break
        
        # slice str to capture the date
        dates.append(lines[span[0]:span[1]])    
        # slice str to capture the sms that matches the date
        messages.append(lines[span[1]:spans[idx+1][0]])

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
    return True if sms1[re.search(regular_expresions['date_regex'], sms1).span()[0]:re.search(regular_expresions['date_regex'], sms1).span()[1]] == \
            sms2[re.search(regular_expresions['date_regex'], sms2).span()[0]:re.search(regular_expresions['date_regex'], sms2).span()[1]] \
                else False
     
     
def get_date(sms):
    date_format = "%d/%m/%Y"
    date_only = "%d/%m/%Y"
    date_obj = datetime.strptime(sms[re.search(regular_expresions['date_regex'], sms).span()[0]:re.search(regular_expresions['date_regex'], sms).span()[1]],
                             date_format)
    return datetime.strftime(date_obj, date_only)


def get_start_time(sms):
    time_str = sms[re.search(regular_expresions['start_time_regex'], sms).span()[0]:re.search(regular_expresions['start_time_regex'], sms).span()[1]]
    time_format = "%H:%M:%S"
    time_obj = datetime.strptime(time_str, time_format)
    print(time_obj.time())
    return time_obj.time()


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
    
    for idx, sms in enumerate(to_split):
        if idx+1 >= len(to_split):
            break
        
        if same_day_sms(sms, to_split[idx+1]):
            date.append(get_date(sms))
            #start_time.append(get_start_time)
    
    
def main():
    create_dataset('messages.txt')
    

if __name__ == '__main__':
    main()