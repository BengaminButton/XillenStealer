#include "mutex.h"
#include <Windows.h>

bool Mutex::CreateDynamic(const char* mutexName) {
    HANDLE hMutex = ::CreateMutexA(NULL, TRUE, mutexName);
    if (GetLastError() == ERROR_ALREADY_EXISTS) {
        return false;
    }
    return hMutex != NULL;
}

bool Mutex::CheckExisting(const char* mutexName) {
    HANDLE hMutex = OpenMutexA(MUTEX_ALL_ACCESS, FALSE, mutexName);
    if (hMutex) {
        CloseHandle(hMutex);
        return true;
    }
    return false;
}
