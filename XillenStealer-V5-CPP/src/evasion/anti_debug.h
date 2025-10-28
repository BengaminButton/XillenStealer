#ifndef ANTI_DEBUG_H
#define ANTI_DEBUG_H

#include <Windows.h>

class AntiDebug {
public:
    static bool IsDebuggerPresent();
    static bool CheckRemoteDebugger();
    static bool CheckParentProcess();
    static bool CloseHandleCheck();
    static bool ExceptionCheck();
    static bool TimingCheck();
    static bool HardwareBreakpointCheck();
    static bool NtSetInformationThread();
    
    static bool RunAllChecks();
};

#endif
