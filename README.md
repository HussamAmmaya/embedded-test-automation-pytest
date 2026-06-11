# Arduino Serial Automation

## Goal

Arduino sends sensor data to Python.
Python reads the data, checks PASS or FAIL, and saves the result in a CSV file.

## Hardware

- Arduino UNO
- USB cable
- Analog input A0

## Software

- Arduino IDE
- Python
- PyCharm
- pyserial

## How it works

1. Arduino reads value from A0.
2. Arduino sends data like this:

A0=523

3. Python reads the data from Serial.
4. Python checks the value:
   - PASS if value is between 300 and 700
   - FAIL if value is lower than 300 or higher than 700
5. Python saves the result in a CSV file.

## Example result

timestamp,sensor,value,result
2026-05-14 16:10:05,A0,523,PASS
2026-05-14 16:10:06,A0,850,FAIL

## Skills

- Arduino Serial communication
- Python automation
- CSV logging
- PASS FAIL test logic
- Basic test automation

## Version 2

Arduino now sends multiple signals:

A0=523
A1=410
STATUS=OK

Python can handle:
- numeric signals: A0 and A1
- text signal: STATUS

Test logic:
- A0 and A1 are PASS if value is between 300 and 700
- STATUS is PASS if value is OK

Version 2 completed: multi-signal logging with PASS/FAIL evaluation, timestamp in milliseconds, automatic CSV filename, input buffer reset, and test summary.

## Version 3 - Functions Refactor

In Version 3, the Python script was refactored into separate functions.

Main functions:

- `connect_to_arduino()`  
  Connects Python to Arduino using the configured COM port and baud rate.

- `create_log_file_path()`  
  Creates a new CSV log file name with date and time.

- `parse_line()`  
  Splits incoming Serial data into signal name and value.

- `evaluate_signal()`  
  Applies PASS/FAIL logic depending on the signal.

- `update_counters()`  
  Counts PASS, FAIL and UNKNOWN results.

- `write_header()`  
  Writes test information into the CSV file.

- `write_summary()`  
  Writes the final test summary into the CSV file.

- `run_test()`  
  Runs the full test sequence.

### V3 Result

The project now has a cleaner structure and is easier to understand, test and extend.