#!/bin/bash

echo "Testing compiler..."
/c/msys64/mingw64/bin/g++.exe --version
echo
echo "Exit code: $?"

echo
echo "Testing simple compilation..."
echo '#include <iostream>
int main() { std::cout << "Hello!"; return 0; }' > /tmp/test.cpp

/c/msys64/mingw64/bin/g++.exe -o /tmp/test.exe /tmp/test.cpp 2>&1
echo "Exit code: $?"
ls -la /tmp/test.exe 2>/dev/null || echo "No executable created"

echo
echo "Testing project compilation..."
cd /c/Users/user/Desktop/XillenStealer-main/XillenStealer-V5-CPP
/c/msys64/mingw64/bin/g++.exe -o xillen_test.exe src/core/main.cpp src/core/stealer.cpp -I. -std=c++20 -v 2>&1 | head -50
echo "Exit code: $?"
ls -la xillen_test.exe 2>/dev/null || echo "No executable created"
