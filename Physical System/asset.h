#ifndef ASSET_INO
#define ASSET_INO

#include <Arduino.h>
#include <FastLED.h> // This is a requirement!

template <uint8_t PIN>
class Asset
{
private:
    int id;
    int count;
    CRGB *leds;

public:
    Asset(int id, int count)
    {
        this->id = id;
        this->count = count;
        leds = new CRGB[count];
        FastLED.addLeds<WS2812B, PIN, GRB>(leds, count);
        for (int i = 0; i < count; i++)
        {
            leds[i] = CRGB::Black;
        }
        FastLED.show();
    }
    void setLED(int ledID, int state)
    {
        if (ledID < 0 || ledID >= count)
            return;
        switch (state)
        {
        case 0:
            leds[ledID] = CRGB::Black;
            break;
        case 1:
            leds[ledID] = CRGB::Green;
            break;
        case 2:
            leds[ledID] = CRGB::Yellow;
            break;
        case 3:
            leds[ledID] = CRGB::Red;
            break;
        case 4:
            leds[ledID] = CRGB::Blue;
            break;
        case 5:
            leds[ledID] = CRGB::DarkOrange break;
        default:
            leds[ledID] = CRGB::Black;
            break;
        }
    }
};

#endif