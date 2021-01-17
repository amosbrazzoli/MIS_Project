#include <ArduinoJson.h>

int IN_MESSAGE = 128;
String incoming;
bool fan1, fan2, fan3, fan4;



void setup() {
    pinMode(1, OUTPUT);
    pinMode(2, OUTPUT);
    pinMode(3, OUTPUT);
    pinMode(4, OUTPUT);
    
    Serial.begin(115200);
}

void loop() {
    if (Serial.available() > 0) {
        incoming = Serial.readStringUntil("\n");
        DynamicJsonDocument doc(1024);
        deserializeJson(doc, incoming);

        fan1 = doc["fan1"];
        fan2 = doc["fan2"];
        fan3 = doc["fan3"];
        fan4 = doc["fan4"];

        digitalWrite(1, fan1);
        digitalWrite(2, fan2);
        digitalWrite(3, fan3);
        digitalWrite(4, fan4);
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
