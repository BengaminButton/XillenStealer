#ifndef HASH_H
#define HASH_H

#include <vector>
#include <cstdint>

class Hash {
public:
    static std::vector<uint8_t> SHA256(const uint8_t* data, size_t len);
};

#endif
