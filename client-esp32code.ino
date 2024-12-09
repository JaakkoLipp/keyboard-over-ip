#include <WiFi.h>
#include <HTTPClient.h>
#include <BleKeyboard.h>

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// Server URL
const char* serverUrl = "http://192.168.1.100:8000/output"; // Replace with your server's IP and port

// Initialize BLE Keyboard
BleKeyboard bleKeyboard;

void setup() {
  Serial.begin(115200);

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi...");
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi!");

  // Initialize BLE Keyboard
  if (!bleKeyboard.isConnected()) {
    bleKeyboard.begin();
    Serial.println("BLE Keyboard initialized. Waiting for connection...");
  }
}

void loop() {
  // Only proceed if connected to Wi-Fi
  if (WiFi.status() == WL_CONNECTED) {
    HTTPClient http;

    // Send GET request to the server
    http.begin(serverUrl);
    int httpResponseCode = http.GET();

    if (httpResponseCode > 0) {
      // Parse response
      String payload = http.getString();
      Serial.println("Response received: " + payload);

      // Extract the "input" value from JSON
      int inputStart = payload.indexOf("\"input\":\"") + 9; // Find start of value
      int inputEnd = payload.indexOf("\"", inputStart);    // Find end of value
      String inputText = payload.substring(inputStart, inputEnd);

      // HID type the input text
      if (bleKeyboard.isConnected() && inputText.length() > 0) {
        Serial.println("Typing: " + inputText);
        bleKeyboard.print(inputText);
      }
    } else {
      Serial.println("Error in HTTP request. Code: " + String(httpResponseCode));
    }

    http.end(); // Close HTTP connection
  } else {
    Serial.println("WiFi not connected!");
  }

  delay(5000); // Wait 5 seconds before the next request
}
