@echo off
echo Removing V5 files from repository...

git rm -r "XillenStealer-V5-CPP"
git rm "README_V5.md"
git rm "README_V5_FINAL.md" 
git rm "README_V5_ULTIMATE.md"
git rm "V4_VS_V5.md"
git rm "compile_v5.py"
git rm "compile_v5_ultimate.py"
git rm "stealer_v5.py"
git rm "stealer_v5_ultimate.py"
git rm "test_v5_safe.py"

echo V5 files removed from git index
pause
