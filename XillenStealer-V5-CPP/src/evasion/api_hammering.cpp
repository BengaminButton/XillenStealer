#include "api_hammering.h"
#include <Windows.h>
#include <ctime>

void APIHammering::RandomAPICall() {
    GetSystemMetrics(SM_CXSCREEN);
    GetSystemTime(nullptr);
    GetTickCount();
}
