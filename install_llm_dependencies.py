#!/usr/bin/env python3
"""
installmultimodelProvidesproviderdependenciestranslated
"""
import subprocess
import sys
import os

def install_package(package):
    """installPythonPackage"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ succeededinstall {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ install {package} failed: {e}")
        return False

def main():
    """translated"""
    print("🚀 translatedinstallmultimodelProvidesproviderdependencies...")
    
    # translatedinstall'sPackage
    packages = [
        "openai>=1.0.0",           # OpenAI
        "google-genai>=1.0.0",     # Google Gemini (translatedonetranslated GenAI SDK)
        "requests>=2.25.0",        # translated (HTTPtranslated)
        "dashscope>=1.10.0",       # translated (iftranslatedinstall)
    ]
    
    success_count = 0
    total_count = len(packages)
    
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 installtranslated: {success_count}/{total_count}  Packageinstallsucceeded")
    
    if success_count == total_count:
        print("🎉 translateddependenciesinstalltranslated！translatedincantranslatedusemultimodelProvidesproviderfeaturetranslated。")
        print("\n📝 usetranslated:")
        print("1. startSystem: python backend/main.py")
        print("2. translatedSettings pagetranslatedconfigAPIkey")
        print("3. Selectselecttranslated'sAImodelProvidesprovider")
        print("4. translateduseAIAuto Clippingfeature")
    else:
        print("⚠️  translateddependenciesinstallfailed，translatedchecktranslatedconnectorManual Installationfailed'sPackage。")
        print("Manual Installationtranslated:")
        for package in packages:
            print(f"  pip install {package}")

if __name__ == "__main__":
    main()
