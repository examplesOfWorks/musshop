def format_phone(phone):
    digits = ''.join(filter(str.isdigit, phone))
    if digits.startswith(('7', '8')):
        digits = digits[1:]
        if len(digits) < 10:
            return phone
        return f'+7({digits[:3]}) {digits[3:6]}-{digits[6:]}'
    return ''


def clean_phone(phone):
    digits = ''.join(filter(str.isdigit, phone))
    if digits.startswith('7'):
        digits = digits[1:]
    return f'+7{digits}' if digits else ''