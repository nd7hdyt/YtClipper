#!/usr/bin/env python3
"""
InstallENDependenciesScript
"""
import subprocess
import sys
import os

def install_package(package):
    """InstallPythonEN"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ SuccessInstall {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Install {package} Failed: {e}")
        return False

def main():
    """EN"""
    print("🚀 ENInstallENDependencies...")
    
    # NeedInstallEN
    packages = [
        "openai>=1.0.0",           # OpenAI
        "google-genai>=1.0.0",     # Google Gemini (EN GenAI SDK)
        "requests>=2.25.0",        # EN (HTTPPleaseEN)
        "dashscope>=1.10.0",       # EN (IfENInstall)
    ]
    
    success_count = 0
    total_count = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 InstallEN: {success_count}/{total_count} ENInstallSuccess")
    
    if success_count == total_count:
        print("🎉 AllDependenciesInstallCompleted！EN。")
        print("\n📝 EN:")
        print("1. StartSystem: python backend/main.py")
        print("2. ENConfigAPIEN")
        print("3. ENAIEN")
        print("4. ENAIAutoEN")
    else:
        print("⚠️  ENDependenciesInstallFailed，PleaseCheckENManualInstallFailedEN。")
        print("ManualInstallEN:")
        for package in packages:
            print(f"  pip install {package}")

if __name__ == "__main__":
    main()
