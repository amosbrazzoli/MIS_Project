#include <ArduinoJson.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>


int IN_MESSAGE = 128;
String incoming;
int fan1, fan2, fan3, fan4;
Adafruit_BNO055 bno = Adafruit_BNO055(55);
DynamicJsonDocument doc(1024);
DynamicJsonDocument out_doc(1024);

void set_fan(int pin_int, int on) {
  if (on == 1){
    digitalWriteFast(pin_int, HIGH);
  } else {
    digitalWriteFast(pin_int, LOW);
  }
}

void setup() {
    pinMode(1, OUTPUT);
    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    pinMode(13, OUTPUT);
    
    Serial.begin(115200);
    
    if (!bno.begin()) {
      Serial.print("NO BNO055 Detected!");
      while(1);
    }
    bno.setExtCrystalUse(true);
    while (!Serial){}
    

}

void loop() {

    if (Serial.available() > 0) {
      deserializeJson(doc, Serial);
      if (!doc["fan"].isNull()){
        set_fan(doc["fan"][0], doc["fan"][1]);
      }
    }
    sensors_event_t event; 
    bno.getEvent(&event);
    out_doc["time"] = millis();
    out_doc["ECG"] = analogRead(A0);
    out_doc["pressure1"] = analogRead(A1)*100;
    out_doc["pressure2"] = analogRead(A2)*100;
    out_doc["x"] = event.orientation.x;
    out_doc["y"] = event.orientation.y;
    out_doc["z"] = event.orientation.z;

    serializeJson(out_doc, Serial);
    Serial.write("\n");
}
