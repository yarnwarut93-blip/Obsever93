import os
import requests
import json
from datetime import datetime

# URL จาก Firebase ของหัวหน้า (ถ้ายังไม่มีให้ใช้ตัวนี้ทดสอบก่อนได้ครับ)
FIREBASE_URL = "https://สังเกตแอป-default-rtdb.firebaseio.com/obsever_logs.json"

def run_obsever():
    print("🛰️ [Obsever93] เริ่มปฏิบัติการสแกนพื้นที่...")
    # ตรวจสอบสิทธิ์การเข้าถึงไฟล์ก่อน
    path = "/sdcard/Download"
    if not os.path.exists(path):
        print("❌ ไม่พบโฟลเดอร์ Download (กรุณารัน termux-setup-storage)")
        return

    try:
        files = os.listdir(path)
        found = [f for f in files if f.endswith('.apk') or 'track' in f.lower()]
        
        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "witness_status": "Protected",
            "evidence_detected": found,
            "source": "Obsever93_Termux"
        }

        # ส่งขึ้น Cloud
        requests.post(FIREBASE_URL, data=json.dumps(report))
        print(f"✅ สำเร็จ: พบไฟล์ต้องสงสัย {len(found)} รายการ และสำรองข้อมูลแล้ว")
    except Exception as e:
        print(f"❌ ข้อผิดพลาด: {e}")

if __name__ == "__main__":
    run_obsever()
