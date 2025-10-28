#ifndef MEMORY_ARCHIVE_H
#define MEMORY_ARCHIVE_H

#include <vector>
#include <cstdint>
#include <string>

class MemoryArchive {
public:
    static std::vector<uint8_t> CreateZIP(const std::vector<uint8_t>& data, const std::string& filename);
};

#endif
