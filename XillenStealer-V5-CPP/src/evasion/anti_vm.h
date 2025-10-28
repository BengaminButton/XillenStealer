#ifndef ANTI_VM_H
#define ANTI_VM_H

#include <Windows.h>

class AntiVM {
public:
    static bool CheckRegistry();
    static bool CheckMAC();
    static bool CheckBIOS();
    static bool CheckCPU();
    static bool CheckDrivers();
    static bool CheckProcesses();
    static bool CheckMemory();
    
    static bool RunAllChecks();
};

#endif
