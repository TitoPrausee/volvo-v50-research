#pragma once
// ============================================================
// African Queen Lite — Rotary Encoder Handler v2.0
// Honda NX650 Dominator RFVC
// ============================================================
//
// Handles a KY-040 rotary encoder for mode switching while riding.
// The encoder provides:
//   - CW rotation: next mode (or next display page)
//   - CCW rotation: previous mode (or previous display page)
//   - Press: toggle between mode-select and page-select
//
// Using encoder instead of two buttons for safer one-handed operation.
// Encoder is more intuitive: twist forward = next, twist back = previous.

#include "modes.h"
#include <Arduino.h>

enum EncoderAction : uint8_t {
    ACTION_NONE = 0,
    ACTION_MODE_UP = 1,    // Next ride mode
    ACTION_MODE_DOWN = 2,  // Previous ride mode
    ACTION_PAGE_UP = 3,   // Next display page
    ACTION_PAGE_DOWN = 4,  // Previous display page
    ACTION_PRESS = 5       // Encoder button press
};

class RotaryEncoder {
public:
    RotaryEncoder() : last_a_(HIGH), position_(0),
                      mode_select_(true),  // true = mode select, false = page select
                      pressed_(false), last_press_ms_(0),
                      last_action_ms_(0) {}

    void begin() {
        pinMode(Pin::ENCODER_A, INPUT_PULLUP);
        pinMode(Pin::ENCODER_B, INPUT_PULLUP);
        pinMode(Pin::ENCODER_BTN, INPUT_PULLUP);

        last_a_ = digitalRead(Pin::ENCODER_A);
        Serial.println("[ENCODER] Rotary encoder initialized (Mode Select mode)");
    }

    // Call in main loop — returns action if any
    EncoderAction update() {
        unsigned long now = millis();
        EncoderAction action = ACTION_NONE;

        // Read encoder
        int a = digitalRead(Pin::ENCODER_A);
        int b = digitalRead(Pin::ENCODER_B);

        if (a != last_a_ && (now - last_action_ms_ > ENCODER_DEBOUNCE_MS)) {
            last_action_ms_ = now;
            if (a == LOW) {  // Falling edge
                if (b == HIGH) {
                    // CW rotation
                    action = mode_select_ ? ACTION_MODE_UP : ACTION_PAGE_UP;
                } else {
                    // CCW rotation
                    action = mode_select_ ? ACTION_MODE_DOWN : ACTION_PAGE_DOWN;
                }
            }
        }
        last_a_ = a;

        // Read button
        if (digitalRead(Pin::ENCODER_BTN) == LOW) {
            if (!pressed_ && (now - last_press_ms_ > DEBOUNCE_MS)) {
                pressed_ = true;
                last_press_ms_ = now;
                action = ACTION_PRESS;
            }
        } else {
            pressed_ = false;
        }

        return action;
    }

    // Toggle between mode-select and page-select
    void toggleMode() {
        mode_select_ = !mode_select_;
        Serial.printf("[ENCODER] Switched to %s mode\n",
            mode_select_ ? "RIDE MODE" : "DISPLAY PAGE");
    }

    bool isModeSelect() const { return mode_select_; }

private:
    int last_a_;
    int position_;
    bool mode_select_;  // true = mode select, false = page select
    bool pressed_;
    unsigned long last_press_ms_;
    unsigned long last_action_ms_;
};