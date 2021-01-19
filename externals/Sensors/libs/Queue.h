#ifndef Queue_h
#define Queue_h

//#include "Arduino.h"

class Queue {
  float *arr;
  int capacity, add_i, rem_i, count;

public:
  // Constructor
  Queue(int len);
  // Destructor
  ~Queue();
  // Remove front element from queue
  float pop();
  // Add item to the queue
  void push(float item);

  float peek(int index);
  int size();
  bool isEmpty();
  bool isFull();
  bool isOverflown();
};

#endif
