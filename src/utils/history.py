import json
import os
from datetime import datetime

# ✅ Absolute path (IMPORTANT FIX)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
HISTORY_FILE = os.path.join(BASE_DIR, "outputs", "history.json")

MAX_HISTORY = 100  # keep last 100 entries


def save_history(entry):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)

    # 🔒 Ensure entry has timestamp
    if "timestamp" not in entry:
        entry["timestamp"] = datetime.now().isoformat()

    # 🛡️ Safe read
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r") as f:
                data = json.load(f)
        else:
            data = []
    except:
        print("[History Warning]: Corrupted file, resetting...")
        data = []

    # ➕ Add new entry
    data.append(entry)

    # 🔥 Limit size
    data = data[-MAX_HISTORY:]

# 💾 Save safely
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        print("✅ History saved at:", HISTORY_FILE)
    except Exception as save_error:
        print("❌ History save FAILED:", str(save_error))
        import traceback
        traceback.print_exc()



def get_history_data():
    try:
        if not os.path.exists(HISTORY_FILE):
            return []

        with open(HISTORY_FILE, "r") as f:
            return json.load(f)

    except:
        print("[History Error]: Failed to read history")
        return []
    

def clear_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "w") as f:
            json.dump([], f)