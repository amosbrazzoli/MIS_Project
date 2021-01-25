#include <ArduinoJson.h>


DynamicJsonDocument doc(1024);


void set_fan(int pin_int, int on) {
  if (on == 1){
    digitalWrite(pin_int, HIGH);
  } else {
    digitalWrite(pin_int, LOW);
  }
}

void setup() {
    // fans
    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(5, OUTPUT);
    
    Serial.begin(115200);
    while (!Serial){}
    

}

void loop() {
  // Serial Reading
  if (Serial.available() > 0) {
    deserializeJson(doc, Serial);
    if (!doc["fan"].isNull()){
      set_fan(doc["fan"][0], doc["fan"][1]);
    }
  }
}
