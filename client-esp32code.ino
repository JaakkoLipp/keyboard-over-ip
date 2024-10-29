#include "USB.h"
#include "USBHIDKeyboard.h"
#include <WiFi.h>
#include <HTTPClient.h>

USBHIDKeyboard keyboard;

// WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// API endpoint
const char* apiEndpoint = "YOUR_API_ENDPOINT";

void setup() {
  Serial.begin(115200);
  keyboard.begin();
  USB.begin();
  
  // Connect to WiFi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

String fetchDataFromAPI() {
  HTTPClient http;
  String payload = "";
  
  if (WiFi.status() == WL_CONNECTED) {
    http.begin(apiEndpoint);
    int httpCode = http.GET();
    
    if (httpCode > 0) {
      payload = http.getString();
    } else {
      Serial.println("Error on HTTP request");
    }
    
    http.end();
  }
  
  return payload;
}

void typeString(String text) {
  for (size_t i = 0; i < text.length(); i++) {
    keyboard.write(text.charAt(i));
    delay(50); // Add delay between keystrokes
  }
  keyboard.write('\n'); // Add newline at the end
}

void loop() {
  String data = fetchDataFromAPI();
  
  if (data.length() > 0) {
    Serial.println("Typing: " + data);
    typeString(data);
  }
  
  delay(5000); // Wait 5 seconds before next API call
}
