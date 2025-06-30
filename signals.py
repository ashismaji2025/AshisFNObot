# signals.py

from datetime import datetime

def generate_demo_signal():
    now = datetime.now().strftime("%H:%M:%S")
    
    return f"📢 *Buy on dips* Nifty Future-July 💹\n" \
           f"*CMP:* 23450\n" \
           f"*Stop Loss:* 23320\n" \
           f"*Time:* {now}"
