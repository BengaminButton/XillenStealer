import os
import sys
import subprocess
import json
from pathlib import Path

class BuilderCompiler:
    def __init__(self):
        self.project_root = Path.cwd()
        self.builder_dir = self.project_root / "electron_builder"
        self.dist_dir = self.builder_dir / "dist"
        
    def check_node(self):
        print("Проверка Node.js...")
        try:
            result = subprocess.run(['node', '--version'], 
                                  capture_output=True, text=True)
            print(f"OK Node.js {result.stdout.strip()}")
            return True
        except FileNotFoundError:
            print("ERROR Node.js не найден!")
            print("\nУстанови Node.js:")
            print("https://nodejs.org/")
            return False
    
    def check_dependencies(self):
        print("Проверка зависимостей...")
        node_modules = self.builder_dir / "node_modules"
        if not node_modules.exists():
            print("Установка зависимостей...")
            subprocess.run(['npm', 'install'], 
                         cwd=self.builder_dir, check=True)
            print("OK Зависимости установлены")
        else:
            print("OK Зависимости найдены")
    
    def build_exe(self):
        print("\n" + "="*50)
        print("Сборка Builder.exe...")
        print("="*50 + "\n")
        
        build_cmd = ['npm', 'run', 'dist']
        
        result = subprocess.run(build_cmd, cwd=self.builder_dir, 
                              capture_output=False)
        
        if result.returncode != 0:
            print("\nERROR Ошибка сборки!")
            return False
        
        exe_files = list(self.dist_dir.glob("XillenStealer Builder Setup *.exe"))
        
        if exe_files:
            exe_path = exe_files[0]
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\nOK Builder.exe создан!")
            print(f"Путь: {exe_path}")
            print(f"Размер: {size_mb:.1f} MB")
            return True
        else:
            print("\nERROR EXE не найден")
            return False
    
    def run(self):
        print("="*60)
        print("  XillenStealer Builder - Компилятор")
        print("="*60 + "\n")
        
        if not self.check_node():
            return False
        
        os.chdir(self.builder_dir)
        
        try:
            self.check_dependencies()
            
            if self.build_exe():
                print("\n" + "="*60)
                print("ГОТОВО!")
                print("="*60)
                print("\nBuilder.exe готов к релизу!")
                print("\nСледующие шаги:")
                print("1. Проверь EXE в папке electron_builder/dist/")
                print("2. Загрузи в GitHub Releases")
                print("3. Пользователи смогут скачать и использовать без установки!\n")
                return True
            else:
                return False
                
        except Exception as e:
            print(f"\nERROR Ошибка: {e}")
            return False

def main():
    compiler = BuilderCompiler()
    success = compiler.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
