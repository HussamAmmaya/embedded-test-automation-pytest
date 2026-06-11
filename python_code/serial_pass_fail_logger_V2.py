import csv
from datetime import datetime
import serial
import time

PORT = "COM5"
BAUD_RATE = 9600
LOG_TIME = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
CSV_FILE = rf"D:\Python_Automation_CAN_Portfolio\03_arduino_serial_automation\logs\serial_log_{LOG_TIME}.csv"


LIMITS = {
    "A0": {"min": 300, "max": 700},
    "A1": {"min": 200, "max": 600}
}

try:
    arduino = serial.Serial(PORT, BAUD_RATE, timeout=1)
    time.sleep(2)
    arduino.reset_input_buffer() # يمسح البيانات القديمة أو الناقصة قبل بدء التسجيل.
    print("Arduino connected successfully")
    print("Test started")
    print("Port:", PORT)
    print("Baud rate:", BAUD_RATE)
    print("Limits:", LIMITS)
    print("-" * 40)
except serial.SerialException:
    print("Arduino not connected")
    print("Check COM port, USB Cable, and close Serial Monitor.")
    exit()

last_value = ""
counter = 0
pass_count = 0
fail_count = 0
unknown_count = 0

with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    writer.writerow(["INFO", "Arduino connected successfully"])
    writer.writerow(["INFO", "Test started"])
    writer.writerow(["INFO", "Port", PORT])
    writer.writerow(["INFO", "Baud rate", BAUD_RATE])
    writer.writerow(["INFO", "Limits", str(LIMITS)])
    writer.writerow(["counter", "timestamp", "sensor", "value", "result"])
    file.flush()

    try:
        while True:
            line = arduino.readline().decode("utf-8", errors="ignore").strip()

            if line == "":
                continue

            if line != last_value and "=" in line:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

                signal, value_text = line.split("=")

                if signal in LIMITS:
                    value = float(value_text)

                    min_value = LIMITS[signal]["min"]
                    max_value = LIMITS[signal]["max"]

                    if min_value <= value <= max_value:
                        result = "PASS"
                    else:
                        result = "FAIL"

                elif signal == "STATUS":
                    value = value_text

                    if value == "OK":
                        result = "PASS"
                    else:
                        result = "FAIL"

                else:
                    value = value_text
                    result = "UNKNOWN"

                counter += 1

                if result == "PASS":
                    pass_count += 1
                elif result == "FAIL":
                    fail_count += 1
                else:
                    unknown_count += 1

                print(counter, timestamp, signal, value, result)
                writer.writerow([counter, timestamp, signal, value, result])
                file.flush()

                last_value = line


    except KeyboardInterrupt:
            print("-" * 40)
            print("Test stopped")
            print("Total records:", counter)
            print("PASS:", pass_count)
            print("FAIL:", fail_count)
            print("UNKNOWN:", unknown_count)

            writer.writerow([])
            writer.writerow(["SUMMARY"])
            writer.writerow(["Total records", counter])
            writer.writerow(["PASS", pass_count])
            writer.writerow(["FAIL", fail_count])
            writer.writerow(["UNKNOWN", unknown_count])
            file.flush()

            arduino.close()
