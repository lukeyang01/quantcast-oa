import sys
import re
from collections import defaultdict

def parse_args(args):
    """Takes args as input, returns filename, date to search for."""

    if len(args) != 4:
        raise ValueError("input arguements must match the following format: 'most_active_cookie [INPUT_FILENAME] -d [TARGET_DATE]'")

    fname = args[1] # input csv filename (required)
    d_tag = args[2] # -d (required)
    date_str = args[3] # YYYY-MM-DD (UTC) (required)

    if d_tag != "-d":
        raise ValueError("input arguements must match the following format: 'most_active_cookie [INPUT_FILENAME] -d [TARGET_DATE]'")

    if fname.split('.')[1] != 'csv':
        raise ValueError(f"{fname} must match the format: 'INPUT_FILENAME.csv'")

    date_pat = r'\d{4}-\d{2}-\d{2}' # YYYY-MM-DD, all digits
    if not re.match(date_pat, date_str):
        raise ValueError(f"{date_str} must match the format: 'YYYY-MM-DD' (UTC timezone)")

    return (fname, date_str)

def parse_file(filename):
    """Takes filename as input, returns lines in form of List[str]."""
    lines = None
    try:
        with open(filename, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: could not open file {filename}")

    return lines

def verify_line(cookie, date, time):
    """Verify single line follows format by specifications."""

    cookie_pat = r'(\w|\d){16}' # any non-special character, 16 chars
    date_pat = r'\d{4}-\d{2}-\d{2}' # YYYY-MM-DD, all digits
    time_pat = r'\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}' # HH:MM:SS+DD:DD, all digits

    if not re.match(cookie_pat, cookie):
        raise TypeError(f"{cookie, date, time} does not match specification: cookie string does not match spec")

    if not re.match(date_pat, date):
        raise TypeError(f"{cookie, date, time} does not match specification: date string does not match spec")

    if not re.match(time_pat, time):
        raise TypeError(f"{cookie, date, time} does not match specification: time string does not match spec")
        
    return True

def calc_cookie(lines:list[str], date_str:str):
    """
    Input:  lines: in format cookie,(date,time), date_str: in format 'YYYY-MM-DD'
            Calculates maximum activity cookies s.t. date == date_str

    Output: Returns list containing maximum activity cookie/cookies, 
                or none message if none match the date
    """
    # Currently only tracking count (int). Can edit to track other info (e.g. timestamp, etc.) with lambda: (0, 0)
    # IF DEFAULTDICT IS NOT ALLOWED: CAN BE REPLACED WITH COMMENTED CODE
    cookie_activity = defaultdict(int)
    # cookie_activity = {}

    for line in lines:
        cookie, timestamp = line.rstrip().split(',')
        date, time = timestamp.split('T')
        if verify_line(cookie, date, time) and date_str == date:
            # if cookie not in cookie_activity:
            #     cookie_activity[cookie] = 0
            cookie_activity[cookie] += 1
    
    # Sorts cookies by cookie_activity count first. Can edit lambda to have further tiebreakers i: (i[1], i[2], etc.)
    sorted_cookies = sorted(cookie_activity.items(), key=lambda i: i[1], reverse=True)

    out = []
    if len(sorted_cookies) == 0:
        out.append(f"No active cookies on {date_str}")
    else:
        most_active = sorted_cookies[0][1]
        for cookie in sorted_cookies:
            if cookie[1] == most_active:
                out.append(cookie[0])
    return out

def main():
    args = sys.argv

    fname, date_str = parse_args(args)
    lines = parse_file(fname)
    
    cookies = calc_cookie(lines, date_str)
    for c in cookies:
        print(c)

if __name__ == "__main__":
    main()

