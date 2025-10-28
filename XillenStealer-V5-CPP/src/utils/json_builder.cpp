#include "json_builder.h"

std::string JsonBuilder::BuildReport(const std::string& browser, const std::string& data) {
    return "{\"browser\":\"" + browser + "\",\"data\":\"" + EscapeJson(data) + "\"}";
}

std::string JsonBuilder::EscapeJson(const std::string& str) {
    std::string result;
    for (char c : str) {
        if (c == '"' || c == '\\') {
            result += '\\';
        }
        result += c;
    }
    return result;
}
