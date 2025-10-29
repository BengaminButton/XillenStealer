#ifndef HOLLOWING_ADVANCED_H
#define HOLLOWING_ADVANCED_H

#include <Windows.h>
#include <winnt.h>

class HollowingAdvanced {
public:
    // Advanced process hollowing
    static bool PerformHollowing(const wchar_t* targetPath);
    
    // PE parser
    static PVOID ParsePE(HMODULE hModule);
    
    // Section injection
    static bool InjectSection(HANDLE hProcess, PVOID pPayload, SIZE_T payloadSize);
    
    // EBPF manipulation
    static void ManipulateEBPF();
};

#endif
