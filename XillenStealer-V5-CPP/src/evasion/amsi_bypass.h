#ifndef AMSI_BYPASS_H
#define AMSI_BYPASS_H

#include <Windows.h>

class AmsiBypass {
public:
    static bool PatchAmsi();
    static bool DisableAmsi();
    static bool HookAmsiScanBuffer();
    static bool BypassAmsiHardware();
    
private:
    static bool PatchAmsiScanBuffer();
    static bool PatchAmsiUacInit();
};

#endif
