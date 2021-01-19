#include "Time_Queue.h"
#include <iostream>

int main() {
    TimeQueue Q = TimeQueue(15.0, 7);
    std::cout << Q.action(1, 0) << std::endl;
    Q.print();
    std::cout << Q.action(2, 5) << std::endl;
    Q.print();
    std::cout << Q.action(3, 10) << std::endl;
    Q.print();
    std::cout << Q.action(4, 13) << std::endl;
    Q.print();
    std::cout << Q.action(5, 15) << std::endl;
    Q.print();
    std::cout << Q.action(8, 20) << std::endl;
    Q.print();
    std::cout << Q.action(-10, 30) << std::endl;
    Q.print();
    return 0;
}
