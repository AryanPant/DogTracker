import os
import serial
import time

# Configure your Arduino's serial port and baud rate
arduino_port = '/dev/ttyUSB0'  # Update to match your Arduino COM port
baud_rate = 9600

def fetch_location():
    """Fetch location from adb dumpsys."""
    try:
        output = os.popen("adb shell dumpsys location | grep -Eo '[0-9]+\\.[0-9]+,[0-9]+\\.[0-9]+'").read()
        locations = output.strip().split('\n')
        if locations:
            return locations[0]  # Return the latest location
        else:
            print("No location found.")
            return None
    except Exception as e:
        print(f"Error fetching location: {e}")
        return None

def main():
    # Open serial connection to Arduino
    with serial.Serial(arduino_port, baud_rate, timeout=1) as ser:
        print(f"Connected to Arduino on {arduino_port}")
        while True:
            location = fetch_location()
            if location:
                print(f"Sending GPS coordinates: {location}")
                ser.write((location + "\n").encode())  # Send location to Arduino
            time.sleep(2)  # Delay before the next fetch

if __name__ == "__main__":
    main()

