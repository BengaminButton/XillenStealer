#!/bin/bash

echo "Testing compilation with explicit linking..."

cd /c/Users/user/Desktop/XillenStealer-main/XillenStealer-V5-CPP

echo "Creating object files..."
/c/msys64/mingw64/bin/g++.exe -c -o main.o src/core/main.cpp -I. -std=c++20
echo "main.o created: $?"
ls -la main.o 2>/dev/null || echo "main.o not created"

/c/msys64/mingw64/bin/g++.exe -c -o stealer.o src/core/stealer.cpp -I. -std=c++20
echo "stealer.o created: $?"
ls -la stealer.o 2>/dev/null || echo "stealer.o not created"

echo
echo "Linking..."
/c/msys64/mingw64/bin/g++.exe -o xillen_test2.exe main.o stealer.o 2>&1
echo "Linking exit code: $?"
ls -la xillen_test2.exe 2>/dev/null || echo "xillen_test2.exe not created"

echo
echo "Current directory files:"
ls -la *.exe 2>/dev/null || echo "No exe files found"
ls -la *.o 2>/dev/null || echo "No object files found"
