#define EXIT_FAILURE 1
#include "HardwareSerial.h"

class Queue {
  float *arr;
  int capacity, add_i, rem_i, count;

  public:
    Queue(int size);
    ~Queue();
 
    float pop();
    void push(float x);
    float peek(int index);
    int size();
    bool isEmpty();
    bool isFull();
    bool isOverflown();
};

// Constructor
Queue::Queue(int len){
    arr = new float[len];
    capacity = len;
    add_i = 0;
    rem_i = -1;
    count = 0;
}

// Destructor
Queue::~Queue(){
  delete[] arr;
};

// Add item to the queue
void Queue::push(float item){
  if (isFull()){
    Serial.println("Adding to full");
  } else if (!isOverflown()){
    arr[add_i] = item;
    add_i = (add_i + 1) % capacity;
    count++;
  } else {
    Serial.println("Has overflown");
  }
  
};

// Remove front element from queue
float Queue::pop(){
  if (isEmpty()){
    Serial.println("Removing from empty");
  }

  rem_i = (rem_i + 1) % capacity;
  count--;
  return arr[rem_i];

};

// Inspect an element in the Queue
float Queue::peek(int index){
  if (isEmpty()){
    Serial.println("Peeking into empty");
  }
  return arr[index];
};

int Queue::size(){
  return count;
};

bool Queue::isEmpty(){
  return (size() == 0);
};

bool Queue::isFull(){
  return (size() == capacity);
};

bool Queue::isOverflown(){
  return (size() > capacity);
}
