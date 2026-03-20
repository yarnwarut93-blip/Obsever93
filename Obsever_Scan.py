import os, requests, json, time
from datetime import datetime

# 🔗 ฐานข้อมูลหลัก (Firebase)
FIREBASE_URL = "https://สังเกตแอป-default-rtdb.firebaseio.com/obsever_logs.json"

def get_network_usage():
    try:
        with open("/proc/net/dev", "r") as f:
            for line in f:
                if "wlan0" in line or "rmnet_data0" in line:
                    data = line.split()
                    return int(data[1]), int(data[9])
    except: pass
    return 0, 0

def run_sentinel():
    print("🛰️ [Obsever93] เริ่มปฏิบัติการสแกนและตรวจจับข้อมูลรั่วไหล...")
    
    # 1. ตรวจสอบไฟล์ในเครื่อง
    path = "/sdcard/Download"
    files = os.listdir(path) if os.path.exists(path) else []
    found_evidence = [f for f in files if f.endswith('.apk') or 'track' in f.lower()]
    
    # 2. ตรวจจับการแอบส่งข้อมูล (2 วินาที)
    r1, t1 = get_network_usage()
    time.sleep(2)
    r2, t2 = get_network_usage()
    diff_tx = round((t2 - t1) / 1024, 2)
    
    # 3. วิเคราะห์สถานะ
    status = "Normal" if diff_tx < 50 else "⚠️ SUSPICIOUS DATA LEAK"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    report = {
        "timestamp": now,
        "witness_status": "Protected Witness",
        "evidence": found_evidence,
        "data_leak_kb": diff_tx,
        "status": status,
        "source": "Termux_Sentinel_V2.5"
    }

    try:
        # ส่งรายงานไป Firebase
        requests.post(FIREBASE_URL, data=json.dumps(report))
        # สั่ง Git Push อัตโนมัติ (เพื่อบันทึกประวัติบน GitHub ทันที)
        os.system(f'git add . && git commit -m "Sentinel Report: {now}" && git push -u origin main --force > /dev/null 2>&1')
        print(f"✅ ภารกิจสำเร็จ: บันทึกหลักฐานเรียบร้อย | Data Out: {diff_tx} KB")
    except Exception as e:
        print(f"❌ ระบบถูกขัดขวาง: {e}")

if __name__ == "__main__":
    run_sentinel()
