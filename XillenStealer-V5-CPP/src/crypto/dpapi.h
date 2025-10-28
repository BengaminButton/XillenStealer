#ifndef DPAPI_H
#define DPAPI_H

#include <vector>
#include <cstdint>
#include <string>

class DPAPI {
public:
    static std::vector<uint8_t> Decrypt(const uint8_t* encryptedData, size_t dataLen);
    static std::string ExtractMasterKey(const std::string& localStatePath);
    static std::vector<uint8_t> Base64Decode(const std::string& input);
};

#endif
