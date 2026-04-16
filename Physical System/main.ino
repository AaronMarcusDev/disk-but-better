#include <FastLED.h>
#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include "Asset.h"

// --- WiFi Settings ---
const char *ssid = "3Disk_WiFi";
const char *password = "disk-but-better";

WebServer server(80);

// --- LED Setup ---
#define NUM_ASSETS 1
const int LED_COUNTS[NUM_ASSETS] = {10};
Asset<27> *assets[NUM_ASSETS];

// --- Web Routes ---
// void handleSet() {
//   if (!server.hasArg("a") || !server.hasArg("l") || !server.hasArg("s")) {
//     server.send(400, "text/plain", "Missing args. Use ?a=0&l=0&s=1");
//     return;
//   }
//   int a = server.arg("a").toInt();
//   int l = server.arg("l").toInt();
//   int s = server.arg("s").toInt();

//   if (a < 0 || a >= NUM_ASSETS) {
//     server.send(400, "text/plain", "Invalid asset ID");
//     return;
//   }

//   assets[a]->setLED(l, s);
//   FastLED.show();

//   server.send(200, "text/plain", "OK");
// }

void handleCode()
{
  if (!server.hasArg("code"))
  {
    server.send(400, "text/plain", "Missing ?code=");
    return;
  }

  String code = server.arg("code");
  Serial.println("Received code: " + code);

  // Reset all LEDs first
  for (int l = 0; l < LED_COUNTS[0]; l++)
  {
    assets[0]->setLED(l, 0);
  }

  // Match the code and light the right LEDs
  if (code == "03G-301")
  {
    assets[0]->setLED(0, 3); // Red
    assets[0]->setLED(1, 2);
    assets[0]->setLED(2, 2);
    assets[0]->setLED(3, 3);
  }
  else if (code == "00B-1111")
  {
    assets[0]->setLED(0, 1); // Green
    assets[0]->setLED(1, 2);
    assets[0]->setLED(2, 1);
    assets[0]->setLED(3, 3);
    assets[0]->setLED(4, 4);
  }
  else if (code == "WARN") // For testing purposes and to show when it is connected.
  {
    assets[0]->setLED(0, 2); // Yellow
    assets[0]->setLED(1, 2);
    assets[0]->setLED(2, 2);
    assets[0]->setLED(3, 2);
    assets[0]->setLED(4, 2);
    assets[0]->setLED(5, 2);
    assets[0]->setLED(6, 2);
    assets[0]->setLED(7, 2);
  }
  else if (code == "12C-1212")
  {
    assets[0]->setLED(0, 3);
    assets[0]->setLED(1, 2);
    assets[0]->setLED(2, 4);
    assets[0]->setLED(3, 2);
    assets[0]->setLED(4, 1);
  }

  else if (code == "00A-1234")
  {                          // De knoop
    assets[0]->setLED(0, 3); // Yellow
    assets[0]->setLED(1, 1);

    assets[0]->setLED(3, 2);
    assets[0]->setLED(4, 2);
  }
  else
  {
    server.send(400, "text/plain", "Unknown code");
    return;
  }

  FastLED.show();
  server.send(200, "text/plain", "OK: " + code);
}

void setup()
{
  Serial.begin(115200);

  // Init assets
  for (int i = 0; i < NUM_ASSETS; i++)
  {
    assets[i] = new Asset<27>(i, LED_COUNTS[i]);
  }
  FastLED.show();

  // Start access point
  WiFi.mode(WIFI_AP);
  WiFi.softAP(ssid, password);
  Serial.print("AP IP: ");
  Serial.println(WiFi.softAPIP()); // 192.168.4.1

  // Route
  //   server.on("/set", handleSet);
  server.on("/code", handleCode);
  server.begin();
  Serial.println("Server started");
}

void loop()
{
  server.handleClient();
}