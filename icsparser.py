from typing import TextIO
from Generate import generate_event_str
days = {'MO': 'M',
        'TU': 'T',
        'WE': 'W',
        'TH': 'R',
        'FR': 'F',
        'SA': 'S',
        'SU': 'U',}
def import_ics(file_path: str) -> list:
    file: TextIO = open(file_path, "rt")
    text_string: str = file.read()
    text_list: list = text_string.split('\n')
    return text_list

def sep_events(event_list) -> dict:
    searching_start = True
    searching_end = False
    event_dict = {}
    event_num = 0
    event = 'event#0'
    for index, item in enumerate(event_list):
        item_split = item.split(':')
        if item_split[0] == 'BEGIN' and searching_start and item_split[1] == 'VEVENT':
            searching_start, searching_end = False, True
            event_dict[event] = []
            event_dict[event].append(event)
        elif item_split[0] == 'END' and searching_end:
            searching_start, searching_end = True, False
            event_dict[event].append(item)
            event_num += 1
            event = f"event#{event_num}"
            event_dict[event] = []
        elif searching_end:
            event_dict[event].append(item)
    return event_dict

def parse_time(time: str,am_pm: bool):
    if am_pm:
        hour = 12 if int(time[0:2]) == 12 else int(time[0:2]) % 12
        day_period = 'PM' if int(time[0:2]) // 12 == 1 else 'AM'
    else:
        hour = time[0:2]
        day_period = None
    minute = time[2:4]
    return hour, minute, day_period

def parse_date(date: str):
    return date[0:4], date[4:6], date[6:]

def parse_event(event: list, am_pm: bool = False) -> dict:
    info_container = {'name': None,
                      'start_day': {'year':None, 'month': None, 'day': None},
                      'end_day': {'year': None, 'month': None, 'day': None},
                      'weekly': None,
                      'happen_days': [],
                      'start_time': {'hour': None, 'minute': None, 'am_pm': None},
                      'end_time': {'hour': None, 'minute': None, 'am_pm': None},
                      'location': None,
                      'description': None,
                      'allday': False}
    for item in event:
        split = item.split(':')
        if split[0] == 'SUMMARY':
            info_container['name'] = split[1]
        elif split[0] == 'DESCRIPTION':
            info_container['description'] = split[1]

        elif split[0] == 'LOCATION':
            info_container['location'] = split[1]

        elif split[0] == 'RRULE':
            div = split[1].split(';')
            for attribute in div:
                try:
                    attrib_name, attrib_val = attribute.split('=')[0], attribute.split('=')[1]
                except IndexError:
                    attrib_name, attrib_val = None, None
                if attrib_name == 'FREQ' and attrib_val == 'WEEKLY':
                    info_container['weekly'] = 'recurring'
                elif attrib_name == 'BYDAY':
                    info_container['happen_days'].append(days[attrib_val])
                elif attrib_name == 'UNTIL':
                    date_end = attrib_val.split('T')[0]
                    (info_container['end_day']['year'], info_container['end_day']['month'],
                     info_container['end_day']['day']) = parse_date(date_end)

        elif split[0].split(';')[0] == 'DTSTART':
            date_start, time_start = split[1].split('T')[0], split[1].split('T')[1]
            (info_container['start_day']['year'], info_container['start_day']['month'],
            info_container['start_day']['day']) = parse_date(date_start)
            time_parsed_start = parse_time(time_start, am_pm)
            (info_container['start_time']['hour'], info_container['start_time']['minute'],
             info_container['start_time']['am_pm']) = time_parsed_start
        elif split[0].split(';')[0] == 'DTEND':
            time_end = split[1].split('T')[1]
            time_parsed_end = parse_time(time_end, am_pm)
            (info_container['end_time']['hour'], info_container['end_time']['minute'],
             info_container['end_time']['am_pm']) = time_parsed_end
    return info_container

def combine_events(event_dict_list : list) -> dict:
    name_list = []
    event_list = event_dict_list.copy()
    for item in event_dict_list:
        name_list.append(item['name'])
    name_set = set(name_list)
    final_dict = {name: None for name in name_set}
    to_remove = []
    for name in name_set:
        for obj in to_remove:
            event_list.remove(obj)
        to_remove.clear()
        found = False
        for item in event_list:
            if item['name'] == name:
                if not found:
                    final_dict[name] = item
                    found = True
                    to_remove.append(item)
                else:
                    final_dict[name]['happen_days'] += item['happen_days']
                    to_remove.append(item)
    return final_dict

def main() -> int:
    event_list = []
    ics_path = str(input('What is the file you would like to parse: '))
    exp_path = str(input('Where would you like your events to be exported to: '))
    try:
        ics_file = import_ics(ics_path)
    except (OSError, FileNotFoundError):
        print('Invalid File')
        return
    split = sep_events(ics_file)
    for value in split.values():
        parsed_event = parse_event(value, False)
        event_list.append(parsed_event)
    combination = combine_events(event_list)
    for value in combination.values():
        md_file = generate_event_str(value, '24hr', 'ymd')
        file_name = value['name']
        try:
            file = open(f'{exp_path}/{file_name}.md', 'wt')
        except FileNotFoundError:
            print('Invalid Directory')
            return
        file.write(md_file)
        file.close()

if __name__ == '__main__':
    main()

