import os
import requests
import json
import time
from datetime import datetime

# URL สำหรับเชื่อมต่อฐานข้อมูลคลาวด์
FIREBASE_URL = "https://สังเกตแอป-default-rtdb.firebaseio.com/obsever_logs.json"

def get_network_usage():
    """ตรวจสอบการรับ-ส่งข้อมูล (Network Tracking)"""
    try:
        with open("/proc/net/dev", "r") as f:
            lines = f.readlines()
            for line in lines:
                if "wlan0" in line or "rmnet_data0" in line:
                    data = line.split()
                    return int(data[1]), int(data[9]) # RX, TX
    except: return 0, 0
    return 0, 0

def run_obsever_v2():
    print("🛰️ [Obsever93 V2] เริ่มปฏิบัติการสแกนและตรวจสอบการรั่วไหล...")
    
    path = "/sdcard/Download"
    files = os.listdir(path) if os.path.exists(path) else []
    found_files = [f for f in files if f.endswith('.apk') or 'track' in f.lower()]
    
    # ดักจับพฤติกรรมการแอบส่งข้อมูล (2 วินาที)
    rx1, tx1 = get_network_usage()
    time.sleep(2)
    rx2, tx2 = get_network_usage()
    
    diff_tx = (tx2 - tx1) / 1024 # ข้อมูลที่ถูกส่งออก (KB)
    leak_status = "Normal" if diff_tx < 50 else "⚠️ SUSPICIOUS DATA LEAK"

    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "witness_status": "Protected",
        "evidence_detected": found_files,
        "data_leak_kb": round(diff_tx, 2),
        "status": leak_status,
        "source": "Obsever93_V2"
    }

    try:
        requests.post(FIREBASE_URL, data=json.dumps(report))
        print(f"✅ บันทึกสำเร็จ! ตรวจพบไฟล์: {len(found_files)} | การแอบส่งข้อมูล: {diff_tx} KB")
    except Exception as e:
        print(f"❌ การเชื่อมต่อถูกขัดขวาง: {e}")

if __name__ == "__main__":
    run_obsever_v2()
