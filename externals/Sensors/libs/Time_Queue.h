#ifndef Time_Queue_h
#define Time_Queue_h

//#include "Arduino.h"
//#include <iostream>

class TimeQueue {
    float   timespan;
    int     measures;
    int     begin;
    int     end;
    int     max_span;
    float*  data;
    int*    times;

private:
    float diff();

public:
    TimeQueue(float timespan, int max_span);
    ~TimeQueue();
    float action(float read, int timestamp);
    void print();
};

#include "Time_Queue.cpp"

#endif
