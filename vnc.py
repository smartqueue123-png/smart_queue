
import time
import math
import requests
import RPi.GPIO as GPIO
import spidev  # For LDR via MCP3008 ADC

# ThingSpeak Setup
THINGSPEAK_API_KEY = "GPF52ZQ1SQE08TVC"  # Replace with your actual key

# Serving time per person
serving_time = 1.5  # minutes per person

# Sensor pins
sensors = {
    "Ultrasonic": {"TRIG": 25, "ECHO": 27},  # Ultrasonic TRIG=25, ECHO=27
    "IR": 17,                                # IR OUT on GPIO17
    "LDR": 0                                 # LDR on MCP3008 channel 0
}

TRIGGER_DISTANCE = 30  # cm for ultrasonic
CONFIRMATION_TIME = 5  # seconds to confirm presence

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(sensors["Ultrasonic"]["TRIG"], GPIO.OUT)
GPIO.setup(sensors["Ultrasonic"]["ECHO"], GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(sensors["IR"], GPIO.IN)

# Setup SPI for MCP3008 (LDR)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000


def readadc(adcnum):
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, (8 + adcnum) << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data


def measure_distance(TRIG, ECHO, timeout=0.03):
    """Return distance in cm, or None if timeout."""
    GPIO.output(TRIG, False)
    time.sleep(0.0002)

    # trigger pulse
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    start = time.time()
    deadline = start + timeout
    while GPIO.input(ECHO) == 0:
        start = time.time()
        if start > deadline:
            return None

    end = time.time()
    deadline = end + timeout
    while GPIO.input(ECHO) == 1:
        end = time.time()
        if end > deadline:
            return None

    elapsed = end - start
    return round((elapsed * 34300.0) / 2.0, 2)


<<<<<<< HEAD
def confirm_presence(sensor_type):
    """Confirm presence: observe for 10s and require 5s continuous detection, with noise tolerance."""
=======
# Confirm presence: 10s observation, 5s continuous detection
def confirm_presence(sensor_type):
>>>>>>> 8044efb98b705c08fe6e3e9961ce06626cacc640
    start_time = time.time()
    detection_start = None
    total_window = 10
    required_time = 5
<<<<<<< HEAD
    last_value = None
    bad_count = 0
    tolerance = 3  # allow up to 3 noisy readings before reset

    while time.time() - start_time < total_window:
=======

    while time.time() - start_time < total_window:  # runs for 10 seconds
>>>>>>> 8044efb98b705c08fe6e3e9961ce06626cacc640
        detected = False

        if sensor_type == "Ultrasonic":
            distance = measure_distance(
                sensors["Ultrasonic"]["TRIG"],
                sensors["Ultrasonic"]["ECHO"]
            )
<<<<<<< HEAD
            last_value = distance
            if distance is not None and distance <= TRIGGER_DISTANCE:
                detected = True

        elif sensor_type == "IR":
            ir_state = GPIO.input(sensors["IR"])
            last_value = ir_state
            if ir_state == 0:
                detected = True

        elif sensor_type == "LDR":
            ldr_value = readadc(sensors["LDR"])
            last_value = ldr_value
            threshold = 200
            if ldr_value < threshold:
                detected = True

        # handle detection logic with tolerance
        if detected:
            if detection_start is None:
                detection_start = time.time()
            bad_count = 0
            if time.time() - detection_start >= required_time:
                return True, last_value
        else:
            if detection_start is not None:
                bad_count += 1
                if bad_count > tolerance:
                    detection_start = None
                    bad_count = 0

        time.sleep(0.1)

    return False, last_value


# ===========================
# Main Loop
# ===========================
=======
            if distance <= TRIGGER_DISTANCE: # TRIGGER_DISTANCE = 30
                detected = True

        elif sensor_type == "IR":
            # IR detects when GPIO LOW (object detected)
            if GPIO.input(sensors["IR"]) == 0:
                detected = True

        elif sensor_type == "LDR":
            # LDR: read from MCP3008 channel 0, threshold to detect presence
            ldr_value = readadc(sensors["LDR"])
            threshold = 200  # make sure threshold is between with and without hand readings (note: the darker the env, the lower the reading)
            if ldr_value < threshold:
                detected = True

        if detected:
            if detection_start is None:
                detection_start = time.time()   # start counting continuous detection (5sec)
            elif time.time() - detection_start >= required_time:
                return True  # confirmed presence
        else:
            detection_start = None # reset if detection breaks

        time.sleep(0.1)

    return False


# Confirm presence function (for multiple stalls)
# def confirm_presence(stall, sensor_type):
#     start_time = time.time()
#     detection_start = None
#     total_window = 10
#     required_time = 5

#     while time.time() - start_time < total_window:
#         detected = False

#         if sensor_type == "Ultrasonic":
#             distance = measure_distance(
#                 stall["Ultrasonic"]["TRIG"],
#                 stall["Ultrasonic"]["ECHO"]
#             )
#             if distance <= TRIGGER_DISTANCE:
#                 detected = True

#         elif sensor_type == "IR":
#             if GPIO.input(stall["IR"]) == 0:
#                 detected = True

#         elif sensor_type == "LDR":
#             ldr_value = readadc(stall["LDR"])
#             if ldr_value < stall["ldr_threshold"]:
#                 detected = True

#         if detected:
#             if detection_start is None:
#                 detection_start = time.time()
#             elif time.time() - detection_start >= required_time:
#                 return True
#         else:
#             detection_start = None

#         time.sleep(0.1)

#     return False


>>>>>>> 8044efb98b705c08fe6e3e9961ce06626cacc640
try:
    while True:     
        # Check all sensors and collect raw values
        ir_trigger, ir_val = confirm_presence("IR")
        ldr_trigger, ldr_val = confirm_presence("LDR")
        u_trigger, u_val = confirm_presence("Ultrasonic")
        

        print("\n--- Sensor Status ---")
        print(f"IR Sensor: {'TRIGGERED' if ir_trigger else 'clear'} | Raw = {ir_val} (0=object,1=clear)")
        print(f"LDR Sensor: {'TRIGGERED' if ldr_trigger else 'clear'} | Value = {ldr_val}")
        print(f"Ultrasonic Sensor: {'TRIGGERED' if u_trigger else 'clear'} | Distance = {u_val}")
        

        # Determine estimated queue length
        if (ir_trigger and not ldr_trigger and not u_trigger) or (ir_trigger and not ldr_trigger and u_trigger):
            est_queue_length = 5
        elif ir_trigger and ldr_trigger and not u_trigger:
            est_queue_length = 10
        elif ir_trigger and ldr_trigger and u_trigger:
            est_queue_length = 15
        else:
            est_queue_length = 0

        waiting_time = math.ceil(est_queue_length * serving_time)

        # Queue category
        if waiting_time == 0:
            category = 0
        elif waiting_time <= 5:
            category = 1
        elif waiting_time <= 10:
            category = 2
        else:
            category = 3

        print("\n--- Queue Summary ---")
        print(f"Estimated People in Queue: {est_queue_length}")
        print(f"Estimated Waiting Time: {waiting_time}")
        print(f"Queue Category: {category}")

        # Send to ThingSpeak
        try:
            url = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}&field1={est_queue_length}&field2={waiting_time}&field3={category}"
            response = requests.get(url, timeout=5)
            print(f"ThingSpeak response: {response.text}")
        except requests.exceptions.RequestException as e:
            print("Failed to send to ThingSpeak:", e)

    # ===========================
    # Multiple Stall Logic (Commented Out Example)
    # ===========================
    #
    # stalls = [
    #     {
    #         "name": "Stall 1",
    #         "Ultrasonic": {"TRIG": 25, "ECHO": 27},
    #         "IR": 17,
    #         "LDR": 0,
    #         "ldr_threshold": 200,
    #         "fields": (1, 2, 3)
    #     },
    #     {
    #         "name": "Stall 2",
    #         "Ultrasonic": {"TRIG": 22, "ECHO": 23},
    #         "IR": 24,
    #         "LDR": 1,
    #         "ldr_threshold": 220,
    #         "fields": (4, 5, 6)
    #     }
    # ]
    #
    # try:
    #     while True:
    #         for stall in stalls:
    #             triggered = {
    #                 "Ultrasonic": confirm_presence("Ultrasonic"),
    #                 "IR": confirm_presence("IR"),
    #                 "LDR": confirm_presence("LDR")
    #             }
    #
    #             print(f"\n--- {stall['name']} Sensor Status ---")
    #             for label, is_triggered in triggered.items():
    #                 status = "TRIGGERED" if is_triggered else "clear"
    #                 print(f"{label} Sensor: {status}")
    #
    #             # Queue logic same as single-stall
    #             u, ir, ldr = triggered["Ultrasonic"], triggered["IR"], triggered["LDR"]
    #
    #             if (u and not ir and not ldr) or (u and not ir and ldr):
    #                 est_queue_length = 5
    #             elif u and ir and not ldr:
    #                 est_queue_length = 10
    #             elif u and ir and ldr:
    #                 est_queue_length = 15
    #             else:
    #                 est_queue_length = 0
    #
    #             waiting_time = math.ceil(est_queue_length * serving_time)
    #
    #             if waiting_time == 0:
    #                 category = 0
    #             elif waiting_time <= 5:
    #                 category = 1
    #             elif waiting_time <= 10:
    #                 category = 2
    #             else:
    #                 category = 3
    #
    #             print(f"\n{stall['name']} Queue Summary:")
    #             print(f"Estimated People in Queue: {est_queue_length}")
    #             print(f"Estimated Waiting Time: {waiting_time}")
    #             print(f"Queue Category: {category}")
    #
    #             # Send to ThingSpeak
    #             try:
    #                 f1, f2, f3 = stall["fields"]
    #                 url = (f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}"
    #                        f"&field{f1}={est_queue_length}&field{f2}={waiting_time}&field{f3}={category}")
    #                 response = requests.get(url, timeout=5)
    #                 print(f"ThingSpeak response: {response.text}")
    #             except requests.exceptions.RequestException as e:
    #                 print("Failed to send to ThingSpeak:", e)
    #

except KeyboardInterrupt:
    print("\nStopping...")
    GPIO.cleanup()






# # Using sample data (fake sensor readings)
# # ===============================================

# import time
# import math
# import requests
# import random

# THINGSPEAK_API_KEY = "GPF52ZQ1SQE08TVC"  # Replace with your actual key
# serving_time = 1.5  # minutes per person


# """Main loop for queue monitoring + sending data to ThingSpeak."""
# try:
#     while True:
#             # Random queue length: either 0, 5, 10, or 15
#         est_queue_length = random.choice([0, 5, 10, 15])

#         # Calculate waiting time
#         waiting_time = math.ceil(est_queue_length * serving_time)

#         # Determine queue category
#         if waiting_time == 0:
#             category = 0
#         elif waiting_time <= 5:
#             category = 1
#         elif waiting_time <= 10:
#             category = 2
#         else:
#             category = 3

#         print("\n--- Queue Summary ---")
#         print(f"Estimated People in Queue: {est_queue_length}")
#         print(f"Estimated Waiting Time: {waiting_time}")
#         print(f"Queue Category: {category}")

#         # Send to ThingSpeak
#         try:
#             url = f"https://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}&field1={est_queue_length}&field2={waiting_time}&field3={category}"
#             response = requests.get(url, timeout=5)
#             print(f"ThingSpeak response: {response.text}")
#         except requests.exceptions.RequestException as e:
#             print("Failed to send to ThingSpeak:", e)

#         time.sleep(15)  # wait before sending again

# except KeyboardInterrupt:
#     print("\nStopping vnc.py...")
