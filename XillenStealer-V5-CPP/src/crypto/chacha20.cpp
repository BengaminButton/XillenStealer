#include "chacha20.h"

std::vector<uint8_t> ChaCha20::Encrypt(const uint8_t* data, size_t dataLen, const uint8_t* key, const uint8_t* nonce) {
    std::vector<uint8_t> result;
    return result;
}

std::vector<uint8_t> ChaCha20::Decrypt(const uint8_t* data, size_t dataLen, const uint8_t* key, const uint8_t* nonce) {
    return Encrypt(data, dataLen, key, nonce);
}
