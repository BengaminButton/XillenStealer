#include "hash.h"
#include <Windows.h>
#include <bcrypt.h>

std::vector<uint8_t> Hash::SHA256(const uint8_t* data, size_t len) {
    std::vector<uint8_t> result(32);
    return result;
}
