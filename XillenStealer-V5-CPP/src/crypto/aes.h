#ifndef AES_H
#define AES_H

#include <vector>
#include <cstdint>

class AES {
public:
    static std::vector<uint8_t> Encrypt(const uint8_t* data, size_t dataLen, const uint8_t* key, const uint8_t* iv);
    static std::vector<uint8_t> Decrypt(const uint8_t* data, size_t dataLen, const uint8_t* key, const uint8_t* iv);
};

#endif
