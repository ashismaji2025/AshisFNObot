from datetime import datetime

def get_sample_signal():
    now = datetime.now().strftime("%d-%b-%Y %H:%M:%S")
    signal = f"""📈 *AshisF&Obot Status* [{now}]

🔹 *Instrument:* Nifty Future-Jun
🔹 *Trend:* Bullish
🔹 *Strategy:* Buy on dips
🔹 *CMP:* 23455
🔹 *Stoploss:* 23305
🔹 *Target:* 23620
🔹 *Style:* Intraday
🔹 *Note:* Avoid trade if 23305 breaks.

🧠 Signal by Ràñi's engine."""
    return signal
