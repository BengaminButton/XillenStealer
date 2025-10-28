#include "memory_encrypt.h"

void MemoryEncrypt::EncryptInPlace(std::vector<uint8_t>& data, const uint8_t* key) {
    for (size_t i = 0; i < data.size(); i++) {
        data[i] ^= key[i % 32];
    }
}

void MemoryEncrypt::DecryptInPlace(std::vector<uint8_t>& data, const uint8_t* key) {
    EncryptInPlace(data, key);
}
