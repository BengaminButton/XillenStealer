#ifndef MUTEX_H
#define MUTEX_H

#include <cstdint>

class Mutex {
public:
    static bool CreateDynamic(const char* mutexName);
    static bool CheckExisting(const char* mutexName);
};

#endif
