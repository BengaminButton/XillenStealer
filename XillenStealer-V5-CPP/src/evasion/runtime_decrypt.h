#ifndef RUNTIME_DECRYPT_H
#define RUNTIME_DECRYPT_H

#include <string>
#include <cstdint>

class RuntimeDecrypt {
public:
    static std::string DecryptString(const uint8_t* data, size_t size, uint8_t key);
};

#endif
