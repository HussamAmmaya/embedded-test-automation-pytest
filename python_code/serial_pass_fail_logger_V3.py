import serial
import time
import csv
from datetime import datetime


PORT = "COM5"
BAUD_RATE = 9600
TEST_DURATION_SECONDS = 10

LIMITS = {
    "A0": {"min": 300, "max": 700},
    "A1": {"min": 200, "max": 600}
}


def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]


def parse_line(line):
    if "=" in line:
        signal, value_text = line.split("=", 1)
        return signal, value_text
    else:
        return None, None


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

        if value == "OK":
            result = "PASS"
        else:
            result = "FAIL"

        return value, result

    else:
        value = value_text
        result = "UNKNOWN"

        return value, result

def connect_to_arduino():
    try:
        arduino = serial.Serial(PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        arduino.reset_input_buffer()

        print("Arduino connected successfully")
        print("Port:", PORT)
        print("Baud rate:", BAUD_RATE)

        return arduino

    except serial.SerialException:
        print("Arduino not connected")
        print("Check COM port, USB cable, and close Serial Monitor.")
        return None

def create_log_file_path():
    log_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file = rf"D:\Python_Automation_CAN_Portfolio\03_arduino_serial_automation\logs\serial_log_{log_time}.csv"
    return csv_file

def write_header(writer, csv_file):
    writer.writerow(["INFO", "Arduino connected successfully"])
    writer.writerow(["INFO", "Test started"])
    writer.writerow(["INFO", "Port:", PORT])
    writer.writerow(["INFO", "Baud rate:", BAUD_RATE])
    writer.writerow(["INFO", "Limits", str(LIMITS)])
    writer.writerow(["INFO", "Log file", csv_file])
    writer.writerow([])
    writer.writerow(["counter", "timestamp", "signal", "value", "result"])

def write_summary(writer, counter, pass_count, fail_count, unknown_count):
    writer.writerow([])
    writer.writerow(["SUMMARY"])
    writer.writerow(["Total records", counter])
    writer.writerow(["PASS", pass_count])
    writer.writerow(["FAIL", fail_count])
    writer.writerow(["UNKNOWN", unknown_count])

def update_counters(result, pass_count, fail_count, unknown_count):
    if result == "PASS":
        pass_count += 1
    elif result == "FAIL":
        fail_count += 1
    else:
        unknown_count += 1

    return pass_count, fail_count, unknown_count

def run_test():
    arduino = connect_to_arduino()

    if arduino is None:
        return

    csv_file = create_log_file_path()

    counter = 0
    pass_count = 0
    fail_count = 0
    unknown_count = 0

    start_time = time.time()

    print("Test started")
    print("Limits:", LIMITS)
    print("Log file:", csv_file)
    print("-" * 40)

    with open (csv_file, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        write_header(writer, csv_file)
        file.flush()

        print("csv header written")

        while True:
            if time.time() - start_time >= TEST_DURATION_SECONDS:
                break

            line = arduino.readline().decode("utf-8", errors="ignore").strip()

            if line == "":
                continue

            signal, value_text = parse_line(line)

            if signal is None:
                print("Invalid line:", line)
                continue

            value, result = evaluate_signal(signal, value_text)

            counter += 1
            timestamp = get_timestamp()

            pass_count, fail_count, unknown_count = update_counters(
                result,
                pass_count,
                fail_count,
                unknown_count
            )

            print(counter, timestamp, signal, value, result)

            writer.writerow([counter, timestamp, signal, value, result])
            file.flush()

        print("-" * 40)
        print("Test finished")
        print("Total records:", counter)
        print("PASS:", pass_count)
        print("FAIL:", fail_count)
        print("UNKNOWN:", unknown_count)

        write_summary(writer, counter, pass_count, fail_count, unknown_count)
        writer.writerow(["INFO", "Arduino connected closed"])
        file.flush()

    arduino.close()
    print("Arduino connection closed")

run_test()

