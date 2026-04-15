#include <FastLED.h>
#include "Asset.h"

#define NUM_ASSETS 1
const int LED_COUNTS[NUM_ASSETS] = {10};
Asset<27>* assets[NUM_ASSETS];

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < NUM_ASSETS; i++) {
    assets[i] = new Asset<27>(i, LED_COUNTS[i]);
  }
  assets[0]->setLED(0, 1); // Green
  assets[0]->setLED(1, 2); // Yellow
  assets[0]->setLED(2, 3); // Red
  assets[0]->setLED(3, 4); // Blue
  assets[0]->setLED(4, 1); // Green
  FastLED.show();
}

void loop() {}