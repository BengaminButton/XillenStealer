#ifndef CHACHA20_H
#define CHACHA20_H

#include <vector>
#include <cstdint>

class ChaCha20 {
public:
    static std::vector<uint8_t> Encrypt(const uint8_t* data, size_t dataLen, const uint8_t* key, const uint8_t* nonce);
    static std::vector<uint8_t> Decrypt(const uint8_t* data, size_t dataLen, const uint8_t* key, const uint8_t* nonce);
};

#endif
