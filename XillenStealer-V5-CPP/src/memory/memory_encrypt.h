#ifndef MEMORY_ENCRYPT_H
#define MEMORY_ENCRYPT_H

#include <vector>
#include <cstdint>

class MemoryEncrypt {
public:
    static void EncryptInPlace(std::vector<uint8_t>& data, const uint8_t* key);
    static void DecryptInPlace(std::vector<uint8_t>& data, const uint8_t* key);
};

#endif
