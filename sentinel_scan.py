import os
def storage_scan():
    print("🛡️ [Sentinel SCE] กำลังเริ่มสแกนพื้นที่จัดเก็บข้อมูล...")
    path = "/sdcard/Download" 
    suspicious_ext = [".apk", ".log", ".tmp", ".exe"]
    found_files = []
    try:
        files = os.listdir(path)
        for f in files:
            if any(ext in f.lower() for ext in suspicious_ext) or "track" in f.lower():
                found_files.append(f)
        if found_files:
            print(f"⚠️ ตรวจพบไฟล์ที่ควรตรวจสอบ ({len(found_files)} รายการ):")
            for item in found_files:
                print(f"  - {item}")
        else:
            print("✅ ไม่พบไฟล์ต้องสงสัยในโฟลเดอร์ Download")
    except Exception as e:
        print(f"❌ เข้าถึงไฟล์ไม่ได้: {e}")
if __name__ == "__main__":
    storage_scan()
