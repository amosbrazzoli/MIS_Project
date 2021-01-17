#include <ArduinoJson.h>

int IN_MESSAGE = 128;
String incoming;
bool fan1, fan2, fan3, fan4;

void set_fan(int pin_int, int on) {
  if (on == 1){
    digitalWrite(pin_int, HIGH);
  } else {
    digitalWrite(pin_int, LOW);
  }
}

void setup() {
    pinMode(1, OUTPUT);
    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    
    Serial.begin(115200);
}

void loop() {
    if (Serial.available() > 0) {
        // If there is a command read it
        DynamicJsonDocument doc(1024);
        incoming = Serial.readStringUntil("\n");


        deserializeJson(doc, incoming);
        int pin_id = doc["fan"][0];
        int state = doc["fan"][1];

        set_fan(pin_id, state);
    }

    DynamicJsonDocument out_doc(1024);
    
    out_doc["time"] = millis();
    out_doc["ECG"] = 45.56;
    out_doc["pressure"] = 650;
    out_doc["x"] = 157.4;
    out_doc["y"] = 82.6;
    out_doc["z"] = 483.2;

    serializeJson(out_doc, Serial);
    Serial.println();
}
