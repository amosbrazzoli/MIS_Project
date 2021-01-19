#include "Time_Queue.h"

TimeQueue::TimeQueue(float timespan, int max_span) {
    this->timespan = timespan;
    this->measures = 0;
    this->begin = 0;
    this->end = 0;
    this->max_span = max_span;
    data = new float[max_span];
    times = new int[max_span];
}

TimeQueue::~TimeQueue() {
    delete[] data;
    delete[] times; 
};

float TimeQueue::diff() {
    /*
    std::cout << data[begin] << " "
                << data[end] << " "
                << measures << " "
                << timespan << " "
                << std::endl;
    */
    //std::cout << (data[begin] - data[end]) << "//" << (measures * timespan) << std::endl;
    return (data[end] - data[begin])/(times[end] - times[begin]);
};

float TimeQueue::action(float read, int timestamp) {
    while (timestamp - times[begin] >= timespan) {
        begin++;
        begin = begin % max_span;
    } 
    end++;
    end = end % max_span;
    measures++;
    measures = (measures < max_span)?measures: max_span;
    data[end] = read;
    times[end] = timestamp;
    return diff();
};

void TimeQueue::print() {
    //std::cout << begin << end << std::endl;
    for (int i = 0; i < max_span; i++) {
        //std::cout << "\t" << data[i] << ", " << times[i] << std::endl;
    }
};

