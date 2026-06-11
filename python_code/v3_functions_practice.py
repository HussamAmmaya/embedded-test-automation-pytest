from datetime import datetime


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


LIMITS = {
    "A0": {"min": 300, "max": 700},
    "A1": {"min": 200, "max": 600}
}

def evaluate_signal(signal, value_text):
    if signal in LIMITS:
        value = float(value_text)

        min_value = LIMITS[signal]["min"]
        max_value = LIMITS[signal]["max"]

        if min_value <= value <= max_value:
            result = "PASS"
        else:
            result = "FAIL"

        return value, result

    elif signal == "STATUS":
        value = value_text

        if value =="OK":
            result = "PASS"
        else:
            result = "FAIL"
        return value, result

    else:
        value = value_text
        result = "UNKNOWN"

        return value, result

def parse_line(line):
    if "=" in line:
        signal, value_text = line.split("=", 1)
        return signal, value_text
    else:
        return None, None

timestamp = get_timestamp()
print(timestamp)