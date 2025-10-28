#ifndef JSON_BUILDER_H
#define JSON_BUILDER_H

#include <string>

class JsonBuilder {
public:
    static std::string BuildReport(const std::string& browser, const std::string& data);
    static std::string EscapeJson(const std::string& str);
};

#endif
