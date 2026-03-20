import os
import subprocess

def scan():
    print("🛡️ [Sentinel SCE] กำลังเริ่มสแกน...")
    try:
        # ตรวจสอบแพ็กเกจที่อาจเป็นอันตราย
        packages = subprocess.check_output("pm list packages", shell=True).decode()
        suspicious = ["spy", "track", "monitor", "remote", "control"]
        found = [p for p in suspicious if p in packages.lower()]
        if found:
            print(f"⚠️ ตรวจพบ: {found}")
        else:
            print("✅ ระบบแพ็กเกจเบื้องต้นปลอดภัย")
    except Exception as e:
        print(f"❌ ระบบถูกบล็อคการเข้าถึง: {e}")

if __name__ == "__main__":
    scan()
