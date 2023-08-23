def generate_event_str(info: dict, time_style: str, date_style: str):
    if time_style == 'am_pm':
        start_time = f"{info['start_time']['hour']}:{info['start_time']['minute']} {info['start_time']['am_pm']}"
        end_time = f"{info['end_time']['hour']}:{info['end_time']['minute']} {info['end_time']['am_pm']}"
    else:
        start_time = f"{info['start_time']['hour']}:{info['start_time']['minute']}"
        end_time = f"{info['end_time']['hour']}:{info['end_time']['minute']}"
    if date_style == 'ydm':
        start_day = f"{info['start_day']['year']}-{info['start_day']['day']}-{info['start_day']['month']}"
        end_day = f"{info['end_day']['year']}-{info['end_day']['day']}-{info['end_day']['month']}"
    elif date_style == 'ymd':
        start_day = f"{info['start_day']['year']}-{info['start_day']['month']}-{info['start_day']['day']}"
        end_day = f"{info['end_day']['year']}-{info['end_day']['month']}-{info['end_day']['day']}"
    else:
        start_day = None
        end_day = None
    text_string = (
    f'---\n'
    f'{conditional_generate("title", info["name"])}\n'
    f'{conditional_generate("allDay", info["allday"])}\n'
    f'{conditional_generate("type", info["weekly"])}\n'
    f'{conditional_generate("daysOfWeek", info["happen_days"])}\n'
    f'{conditional_generate("startRecur", start_day)}\n'
    f'{conditional_generate("endRecur", end_day)}\n'
    f'{conditional_generate("startTime", start_time)}\n'
    f'{conditional_generate("endTime", end_time)}\n'
    f'---\n'
    f'Location: {info["location"]}\n'
    f'{info["description"]}'
    )
    return text_string

def conditional_generate(text, value = None):
    if value is not None:
        return f"{text}: {value}"
    else:
        return ''