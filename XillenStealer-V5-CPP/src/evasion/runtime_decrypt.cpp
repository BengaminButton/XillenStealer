#include "runtime_decrypt.h"

std::string RuntimeDecrypt::DecryptString(const uint8_t* data, size_t size, uint8_t key) {
    std::string result;
    result.reserve(size);
    for (size_t i = 0; i < size; i++) {
        result += (char)(data[i] ^ key);
    }
    return result;
}
