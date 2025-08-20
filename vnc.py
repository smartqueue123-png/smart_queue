# #import RPi.GPIO as GPIO
# import time
# import math
# import requests

# # ThingSpeak Setup
# THINGSPEAK_API_KEY = "GPF52ZQ1SQE08TVC"  # Replace with your actual key
# THINGSPEAK_URL = "https://api.thingspeak.com/update"

# # person_width = 50     # cm
# # gap_between = 20      # cm
# serving_time = 1.5      # minutes per person (varies for different food stalls)

# # Setup
# #GPIO.setmode(GPIO.BCM)

# # Sensor GPIO Pins
# sensors = {
#     "A": {"TRIG": 2, "ECHO": 3},
#     "B": {"TRIG": 4, "ECHO": 17},
#     "C": {"TRIG": 27, "ECHO": 22}
# }

# TRIGGER_DISTANCE = 30  # cm (if someone is within 30cm from sensor, sensor is considered triggered)

# # # Setup GPIO pins
# # for s in sensors.values():
# #     GPIO.setup(s["TRIG"], GPIO.OUT)
# #     GPIO.setup(s["ECHO"], GPIO.IN)

# # #Function to measure distance
# # def measure_distance(TRIG, ECHO):
# #     GPIO.output(TRIG, False)
# #     time.sleep(0.05)

# #     GPIO.output(TRIG, True)
# #     time.sleep(0.00001)
# #     GPIO.output(TRIG, False)

# #     while GPIO.input(ECHO) == 0:
# #         pulse_start = time.time()
# #     while GPIO.input(ECHO) == 1:
# #         pulse_end = time.time()

# #     pulse_duration = pulse_end - pulse_start
# #     distance = round(pulse_duration * 17150, 2)  # in cm
# #     return distance


# try:
#     while True:
#         # # Measure distance from all sensors
#         # distances = {}
#         # # for reference: 'A': {"TRIG": 2, "ECHO": 3}
#         # for label, pins in sensors.items():
#         #     dist = measure_distance(pins["TRIG"], pins["ECHO"])
#         #     distances[label] = dist

#         # ============= SAMPLE DATA (FOR CHECKING) ==============
#         distances = {
#             "A": 30,
#             "B": 100,
#             "C": 100
#         }

#         # Print distances (for checking)
#         print("\n--- Distance Readings ---")
#         for label, dist in distances.items():
#             print(f"Sensor {label}: {dist} cm")

#         # Determine triggered sensors
#         triggered = {
#             label: dist <= TRIGGER_DISTANCE for label, dist in distances.items()
#         }

#         print("\n--- Sensor Status ---")
#         for label, is_triggered in triggered.items():
#             status = "TRIGGERED" if is_triggered else "clear"
#             print(f"Sensor {label}: {status}")
        

#         ## A/A&C/B/C/B&C : <= 5 people
#         ## A&B : <= 10 people
#         ## A&B&C : <= 15 people
#         if (triggered["A"] and not triggered["B"] and not triggered["C"]) \
#         or (not triggered["A"] and triggered["B"] and not triggered["C"]) \
#         or (not triggered["A"] and not triggered["B"] and triggered["C"]) \
#         or (triggered["A"] and not triggered["B"] and triggered["C"]) \
#         or (not triggered["A"] and triggered["B"] and triggered["C"]):
#             est_queue_length = 5
#             #category = "Short"

#         elif triggered["A"] and triggered["B"] and not triggered["C"]:
#             est_queue_length = 10
#             #category = "Medium"

#         elif triggered["A"] and triggered["B"] and triggered["C"]:
#             est_queue_length = 15
#             #category = "Long"

#         elif (not triggered["A"] and not triggered["B"] and not triggered["C"]):
#             est_queue_length = 0
#             #category = "No Queue"

#         print(f"\nEstimated Queue Length: {est_queue_length} people")


#         # Count triggered sensors
#         #triggered_count = sum(triggered.values())

#         # Estimate actual number of people in a queue (rough)
#         ## queue number can be either 5, 10, or 15
#         #est_queue_length = triggered_count * 2


#         # Calculate waiting time
#         waiting_time = math.ceil(est_queue_length * serving_time)  # in minutes

#         # Determine queue category
#         if waiting_time == 0:
#             category = 0  # No queue
#         elif waiting_time <= 5:
#             category = 1  # Short
#         elif waiting_time <= 10:
#             category = 2  # Medium
#         else:
#             category = 3  # Long

#         print("\n--- Queue Summary ---")
#         print(f"Estimated People in Queue: {est_queue_length}")
#         print(f"Estimated waiting time: {waiting_time}")
#         print(f"Queue Category: {category}")


#         # Send to ThingSpeak (estimated number of people in queue, category, waiting time) using GET URL
#         try:
#             url = "https://api.thingspeak.com/update?api_key=%s&field1=%s&field2=%s&field3=%s" % (
#                 THINGSPEAK_API_KEY,
#                 est_queue_length,
#                 waiting_time, 
#                 category
#             )
#             response = requests.get(url, timeout=5)
#             print(f"\nThingSpeak response: {response.text}")
#         except requests.exceptions.RequestException as e:
#             print("Failed to send to ThingSpeak:", e)

            
#         break

#         #time.sleep(5)  # delay before next scan

# except KeyboardInterrupt:
#     print("\nStopping...")
#     GPIO.cleanup()




# ## problem
# ## we are only demoing for one food stall, how to amend code that will check the rest of the stalls?














# import time
# import math
# import requests
# import RPi.GPIO as GPIO 
# import spidev             # Added for LDR via MCP3008 ADC

# # ThingSpeak Setup
# THINGSPEAK_API_KEY = "GPF52ZQ1SQE08TVC"  # Replace with your actual key

# # Serving time per person
# serving_time = 1.5  # minutes per person

# # Sensor pins
# sensors = {
#     "Ultrasonic": {"TRIG": 25, "ECHO": 27},  # Ultrasonic TRIG=25, ECHO=27
#     "IR": 17,                                # IR OUT on GPIO17
#     "LDR": 0                                 # LDR on MCP3008 channel 0
# }

# TRIGGER_DISTANCE = 10  # cm for ultrasonic
# CONFIRMATION_TIME = 5  # seconds to confirm presence

# # Setup GPIO (uncomment when running on Pi)
# GPIO.setmode(GPIO.BCM)
# GPIO.setwarnings(False)
# GPIO.setup(sensors["Ultrasonic"]["TRIG"], GPIO.OUT)
# GPIO.setup(sensors["Ultrasonic"]["ECHO"], GPIO.IN)
# GPIO.setup(sensors["IR"], GPIO.IN)

# # Setup SPI for MCP3008 (LDR)
# spi = spidev.SpiDev()
# spi.open(0, 0)
# spi.max_speed_hz = 1350000

# def readadc(adcnum):
#     if adcnum > 7 or adcnum < 0:
#         return -1
#     r = spi.xfer2([1, (8 + adcnum) << 4, 0])
#     data = ((r[1] & 3) << 8) + r[2]
#     return data

# # Measure distance using ultrasonic sensor
# def measure_distance(TRIG, ECHO):
#     GPIO.output(TRIG, 1)
#     time.sleep(0.00001)
#     GPIO.output(TRIG, 0)

#     StartTime = time.time()
#     StopTime = time.time()
#     while GPIO.input(ECHO) == 0:
#         StartTime = time.time()
#     while GPIO.input(ECHO) == 1:
#         StopTime = time.time()

#     ElapsedTime = StopTime - StartTime
#     Distance = (ElapsedTime * 34300) / 2  # cm
#     return Distance

# # # def confirm_presence(sensor_type):
# # #     """Return True if sensor detects a person for CONFIRMATION_TIME seconds"""
# # #     start_time = time.time()
# # #     while time.time() - start_time < CONFIRMATION_TIME:
# # #         if sensor_type == "Ultrasonic":
# # #             # distance = measure_distance(sensors["Ultrasonic"]["TRIG"], sensors["Ultrasonic"]["ECHO"])
# # #             distance = 25  # SAMPLE DATA for testing
# # #             if distance <= TRIGGER_DISTANCE:
# # #                 return True
# # #         elif sensor_type == "IR":
# # #             # if GPIO.input(sensors["IR"]) == GPIO.HIGH:
# # #             ir_status = True  # SAMPLE DATA
# # #             if ir_status:
# # #                 return True
# # #         elif sensor_type == "LDR":
# # #             # if GPIO.input(sensors["LDR"]) == GPIO.LOW:  # assuming LOW = blocked/light blocked
# # #             ldr_status = True  # SAMPLE DATA
# # #             if ldr_status:
# # #                 return True
# # #         time.sleep(0.1)
# # #     return False


# # Confirm presence: 10s observation, 5s continuous detection
# def confirm_presence(sensor_type):
#     start_time = time.time()
#     detection_start = None
#     total_window = 10
#     required_time = 5

#     while time.time() - start_time < total_window:  # runs for 10 seconds
#         detected = False

#         if sensor_type == "Ultrasonic":
#             distance = measure_distance(
#                 sensors["Ultrasonic"]["TRIG"],
#                 sensors["Ultrasonic"]["ECHO"]
#             )
#             if distance <= TRIGGER_DISTANCE:
#                 detected = True

#         elif sensor_type == "IR":
#             # IR detects when GPIO LOW (object detected)
#             if GPIO.input(sensors["IR"]) == 0:
#                 detected = True

#         elif sensor_type == "LDR":
#             # LDR: read from MCP3008 channel 0, threshold to detect presence
#             ldr_value = readadc(sensors["LDR"])
#             threshold = 500  # adjust based on your environment
#             if ldr_value < threshold:
#                 detected = True

#         if detected:
#             if detection_start is None:
#                 detection_start = time.time()   # start counting continuous detection (5sec)
#             elif time.time() - detection_start >= required_time:
#                 return True  # confirmed presence
#         else:
#             detection_start = None # reset if detection breaks

#         time.sleep(0.1)

#     return False


# try:
#     while True:
#         # Check all sensors
#         triggered = {
#             "Ultrasonic": confirm_presence("Ultrasonic"),
#             "IR": confirm_presence("IR"),
#             "LDR": confirm_presence("LDR")
#         }

#         print("\n--- Sensor Status ---")
#         for label, is_triggered in triggered.items():
#             status = "TRIGGERED" if is_triggered else "clear"
#             print(f"{label} Sensor: {status}")

#         # Determine estimated queue length (same logic as before)
#         u, ir, ldr = triggered["Ultrasonic"], triggered["IR"], triggered["LDR"]
#         if (u and not ir and not ldr) or (not u and ir and not ldr) or (not u and not ir and ldr) \
#            or (u and not ir and ldr) or (not u and ir and ldr):
#             est_queue_length = 5
#         elif u and ir and not ldr:
#             est_queue_length = 10
#         elif u and ir and ldr:
#             est_queue_length = 15
#         else:  # none triggered
#             est_queue_length = 0


#         Determine estimated queue length based on new logic
#         u, ir, ldr = triggered["Ultrasonic"], triggered["IR"], triggered["LDR"]

#         if u and not ir and not ldr | u and not ir and ldr:
#             est_queue_length = 5
#         elif u and ir:
#             est_queue_length = 10
#         elif u and ir and ldr:
#             est_queue_length = 15
#         else:
#             est_queue_length = 0


#         # Determine estimated queue length based on new logic
#         u, ir, ldr = triggered["Ultrasonic"], triggered["IR"], triggered["LDR"]

#         if (u and not ir and not ldr) or (u and not ir and ldr):
#             est_queue_length = 5
#         elif u and ir and not ldr:
#             est_queue_length = 10
#         elif u and ir and ldr:
#             est_queue_length = 15
#         else:
#             est_queue_length = 0


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

#         #break  # for testing, remove for continuous loop

# except KeyboardInterrupt:
#     print("\nStopping...")
#     GPIO.cleanup()







import time
import math
import requests

THINGSPEAK_API_KEY = "GPF52ZQ1SQE08TVC"  # Replace with your actual key
serving_time = 1.5  # minutes per person

def run_vnc():
    """Main loop for queue monitoring + sending data to ThingSpeak."""
    try:
        while True:
             # Random queue length: either 0, 5, 10, or 15
            est_queue_length = random.choice([0, 5, 10, 15])

            # Calculate waiting time
            waiting_time = math.ceil(est_queue_length * serving_time)

            # Determine queue category
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

            time.sleep(15)  # wait before sending again

    except KeyboardInterrupt:
        print("\nStopping vnc.py...")






