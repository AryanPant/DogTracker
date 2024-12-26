#include <SoftwareSerial.h>

// Define software serial pins for RYLR998 communication
#define RX_PIN 11 // Arduino pin connected to RYLR998 TX
#define TX_PIN 10 // Arduino pin connected to RYLR998 RX
SoftwareSerial LoRa(RX_PIN, TX_PIN);

// Initial Fake GPS Coordinates
float latitude = 29.864590;
float longitude = 77.900346;
const char *altitude = "250"; // Static altitude in meters

void setup() {
  // Initialize hardware and software serial
  Serial.begin(9600);       // For debugging via Serial Monitor
  LoRa.begin(9600);         // For RYLR998 communication
  Serial.println("LoRa Module Initialized");

  // Send a test command to ensure communication
  sendCommand("AT");
}

void loop() {
  // Update latitude and longitude for dynamic change
  updateCoordinates();

  // Construct a fake GPS message
  String fakeGPSMessage = createFakeNMEA(latitude, longitude, altitude);

  // Transmit the message via LoRa
  Serial.println("Transmitting Fake GPS Data:");
  Serial.println(fakeGPSMessage);
  sendCommand("AT+SEND=1," + String(fakeGPSMessage.length()) + "," + fakeGPSMessage);

  // Wait before sending the next message
  delay(2000);
}

void sendCommand(const String &command) {
  // Clear any residual data in the buffer
  while (LoRa.available()) {
    LoRa.read();
  }

  // Send the command
  LoRa.println(command);
  delay(100); // Short delay for module processing

  // Print the response from the LoRa module
  unsigned long startMillis = millis();
  while (millis() - startMillis < 500) { // Timeout after 500ms
    if (LoRa.available()) {
      char c = LoRa.read();
      Serial.write(c);
    }
  }
  Serial.println(); // Newline for readability
}

String createFakeNMEA(float lat, float lon, const char *alt) {
  // Build an NMEA sentence for GPS fix data
  String message = "$GPGGA,"; // NMEA header
  message += "123519,";       // Fixed example time (hhmmss.ss format)
  message += String(lat, 6) + ",N,"; // Latitude with hemisphere
  message += String(lon, 6) + ",E,"; // Longitude with hemisphere
  message += "1,";            // Fix quality (1 = GPS fix, 0 = no fix)
  message += "08,";           // Number of satellites (fixed example)
  message += "0.9,";          // Horizontal dilution of position
  message += String(alt) + ",M,"; // Altitude with units (M = meters)
  message += "46.9,M,";       // Height of geoid above WGS84 ellipsoid
  message += "0000*47";       // Checksum (static example)
  return message;
}

void updateCoordinates() {
  // Increment latitude and longitude slightly to simulate movement
  latitude += random(-1, 2) * 0.0001; // Random change in latitude
  longitude += random(-1, 2) * 0.0001; // Random change in longitude

  // Ensure coordinates stay in valid GPS range
  if (latitude > 90.0) latitude = -90.0 + (latitude - 90.0);
  if (latitude < -90.0) latitude = 90.0 + (latitude + 90.0);
  if (longitude > 180.0) longitude = -180.0 + (longitude - 180.0);
  if (longitude < -180.0) longitude = 180.0 + (longitude + 180.0);
}

