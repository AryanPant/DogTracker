import serial
import subprocess
import time

# Set the serial port for Arduino
arduino_port = '/dev/ttyACM0'  # Update with your Arduino serial port (e.g., COM3 on Windows)
baud_rate = 9600  # Baud rate matching Arduino setup

# Initialize serial communication with Arduino
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)

# Store the last sent location
last_location = "29.864590,77.900346"  # Set an initial default location

# Function to fetch coordinates from Android device using adb
def fetch_location():
    # Run adb command to get the GPS location
    command = "adb shell dumpsys location | grep -Eo '[0-9]+\\.[0-9]+,[0-9]+\\.[0-9]+'"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    # Extract latitude and longitude from the first line of the result
    if result.returncode == 0 and result.stdout.strip():
        location = result.stdout.splitlines()[0].strip()  # Get the first line of location data
        return location
    else:
        print("Error fetching location or no valid GPS data received")
        return None

# Function to send coordinates to Arduino
def send_to_arduino(location):
    if location:
        arduino.write(location.encode())  # Send location string to Arduino
        print(f"Sent location: {location}")
    else:
        print("No location to send")

# Main loop to fetch location and send it to Arduino
try:
    while True:
        # Fetch the location
        location = fetch_location()

        # Use last location if no new location is fetched
        if location:
            last_location = location

        # Send the last location (either updated or previous)
        send_to_arduino(last_location)

        # Wait before sending the next location
        time.sleep(2)

except KeyboardInterrupt:
    print("Program terminated by user.")
finally:
    arduino.close()  # Close the serial port connection

