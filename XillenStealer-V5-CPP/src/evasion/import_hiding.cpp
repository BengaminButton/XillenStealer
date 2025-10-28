#include "import_hiding.h"
#include <winternl.h>

DWORD ImportHiding::HashString(const char* str) {
    DWORD hash = 0;
    while (*str) {
        hash = ((hash << 25) | (hash >> 7));
        hash ^= *str++;
    }
    return hash;
}

FARPROC ImportHiding::GetProcAddressByHash(HMODULE hModule, DWORD hash) {
    PIMAGE_DOS_HEADER dosHeader = (PIMAGE_DOS_HEADER)hModule;
    PIMAGE_NT_HEADERS ntHeaders = (PIMAGE_NT_HEADERS)((BYTE*)hModule + dosHeader->e_lfanew);
    PIMAGE_EXPORT_DIRECTORY exportDir = (PIMAGE_EXPORT_DIRECTORY)((BYTE*)hModule + 
        ntHeaders->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_EXPORT].VirtualAddress);
    
    DWORD* functions = (DWORD*)((BYTE*)hModule + exportDir->AddressOfFunctions);
    DWORD* names = (DWORD*)((BYTE*)hModule + exportDir->AddressOfNames);
    WORD* ordinals = (WORD*)((BYTE*)hModule + exportDir->AddressOfNameOrdinals);
    
    for (DWORD i = 0; i < exportDir->NumberOfNames; i++) {
        const char* funcName = (const char*)((BYTE*)hModule + names[i]);
        if (HashString(funcName) == hash) {
            WORD ordinal = ordinals[i];
            return (FARPROC)((BYTE*)hModule + functions[ordinal]);
        }
    }
    return NULL;
}
