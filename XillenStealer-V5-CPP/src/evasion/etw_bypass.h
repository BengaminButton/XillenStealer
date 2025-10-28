#ifndef ETW_BYPASS_H
#define ETW_BYPASS_H

#include <Windows.h>

class EtwBypass {
public:
    static bool PatchEtwEventWrite();
    static bool PatchEtwEventWriteEx();
    static bool PatchEtwEventWriteFull();
    static bool DisableEtwProvider();
    static bool BypassEtwHardware();
    
private:
    static bool PatchFunction(const char* dllName, const char* functionName, BYTE* patch, SIZE_T patchSize);
};

#endif
