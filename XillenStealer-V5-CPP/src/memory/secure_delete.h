#ifndef SECURE_DELETE_H
#define SECURE_DELETE_H

#include <cstdint>

class SecureDelete {
public:
    static void WipeMemory(void* ptr, size_t size);
};

#endif
