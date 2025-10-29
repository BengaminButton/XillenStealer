#include "emulator_collector.h"
#include <Windows.h>
#include <shlobj.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <vector>

std::string EmulatorCollector::CollectEmulatorData() {
    std::ostringstream result;
    result << "\n=== EMULATORS ===\n";
    
    char localappdata[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_LOCAL_APPDATA, NULL, SHGFP_TYPE_CURRENT, localappdata);
    
    std::vector<std::pair<std::string, std::string>> emulators = {
        {"BlueStacks", std::string(localappdata) + "\\BlueStacks"},
        {"NoxPlayer", std::string(localappdata) + "\\NoxPlayer"},
        {"LDPlayer", std::string(localappdata) + "\\LDPlayer"},
        {"MEmu", std::string(localappdata) + "\\MEmu"},
        {"GameLoop", std::string(localappdata) + "\\GameLoop"},
        {"Android Studio", std::string(localappdata) + "\\Google\\AndroidStudio"},
        {"Genymotion", std::string(localappdata) + "\\Genymobile\\Genymotion"}
    };
    
    int found = 0;
    for (const auto& [name, path] : emulators) {
        if (std::filesystem::exists(path)) {
            result << name << ": FOUND\n";
            found++;
        }
    }
    
    result << "Total emulators found: " << found << "\n";
    
    return result.str();
}
