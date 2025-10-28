#ifndef IMPORT_HIDING_H
#define IMPORT_HIDING_H

#include <Windows.h>

class ImportHiding {
public:
    static FARPROC GetProcAddressByHash(HMODULE hModule, DWORD hash);
    static DWORD HashString(const char* str);
};

#endif
