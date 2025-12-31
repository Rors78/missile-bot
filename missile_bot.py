import requests, time, sys
from datetime import datetime

# =======================
# CONFIG
# =======================
REFRESH_INTERVAL    = 10   # seconds
TOP_N               = 10
BINANCE_API         = "https://api.binance.us/api/v3"
ATR_PERIOD          = 14
INITIAL_ATR_MULT    = 2.0
TRAILING_STEP_MULT  = 1.0

# Terminal colors
RESET  = "\033[0m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
FLASH  = "\033[5m"

# =======================
# API
# =======================
def fetch_binance_pairs():
    try:
        r = requests.get(f"{BINANCE_API}/exchangeInfo", timeout=5)
        data = r.json()
        return [s['symbol'] for s in data['symbols']
                if s['quoteAsset']=='USDT' and s['status']=='TRADING']
    except:
        return []

def fetch_binance_klines(symbol, interval="1m", limit=100):
    try:
        r = requests.get(f"{BINANCE_API}/klines?symbol={symbol}"
                         f"&interval={interval}&limit={limit}", timeout=5)
        return r.json()
    except:
        return []

# =======================
# INDICATORS
# =======================
def calc_atr(candles, period=ATR_PERIOD):
    trs = []
    for i in range(1, len(candles)):
        high = float(candles[i][2])
        low  = float(candles[i][3])
        prev_close = float(candles[i-1][4])
        tr = max(high-low, abs(high-prev_close), abs(low-prev_close))
        trs.append(tr)
    if len(trs) < period:
        return sum(trs)/len(trs)
    return sum(trs[-period:]) / period

# =======================
# ANALYSIS
# =======================
def calc_breakout_score(candles):
    if len(candles) < 5:
        return 0, "→", "neutral"
    closes = [float(c[4]) for c in candles]
    volumes = [float(c[5]) for c in candles]
    price_change = (closes[-1] - closes[0]) / closes[0]
    slope = (closes[-1] - closes[-4]) / closes[-4] if len(closes)>=4 else 0
    recent_vol = sum(volumes[-3:])
    prev_vol   = sum(volumes[:-3]) / max(len(volumes)-3,1)
    vol_ratio  = recent_vol / max(prev_vol,1)
    score = round((price_change * 100) * vol_ratio, 2)
    arrow = "↗" if slope>0.005 and vol_ratio>2 else ("↘" if slope< -0.005 else "→")
    if score>10 and slope>0.01 and vol_ratio>3:
        status="blast"
    elif score>4 and slope>0.005 and vol_ratio>2:
        status="warn"
    else:
        status="neutral"
    return score, arrow, status

# =======================
# TP ENGINE (ATR-BASED)
# =======================
class TPEngine:
    def __init__(self, entry_price, atr):
        self.entry      = entry_price
        self.atr        = atr
        self.initial_tp = entry_price + INITIAL_ATR_MULT * atr
        self.step       = TRAILING_STEP_MULT * atr
        self.best_high  = entry_price
        self.current_tp = self.initial_tp

    def update(self, price):
        if price > self.best_high:
            self.best_high = price
            steps = int((self.best_high - self.entry) // self.step)
            new_tp = self.entry + steps * self.step
            if new_tp > self.current_tp:
                self.current_tp = new_tp
        return self.current_tp

# =======================
# MAIN LOOP
# =======================
def main():
    print(f"{BOLD}{CYAN}🚀 Sentinel XΩ V5150+ – Breakout Radar + Smart ATR-TP{RESET}\n")
    pairs = fetch_binance_pairs()
    if not pairs:
        print(f"{RED}❌ No Binance pairs found. Exiting.{RESET}")
        sys.exit(1)

    tp_engine = None

    while True:
        scores = []
        for symbol in pairs:
            candles = fetch_binance_klines(symbol)
            if not candles:
                continue
            score, arrow, status = calc_breakout_score(candles)
            scores.append((symbol, score, arrow, status, candles))

        scores.sort(key=lambda x: x[1], reverse=True)
        top_scores = scores[:TOP_N]
        missile = top_scores[0] if top_scores else (None,0,"→","neutral",[])

        sys.stdout.write("\033[2J\033[H")  # clear
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{BOLD}{CYAN}=== Sentinel XΩ V5150+ Breakout Radar ==={RESET}")
        print(now)
        print(f"Scanning {len(pairs)} USDT pairs | Top {TOP_N}\n")

        symbol, score, arrow, status, candles = missile
        color = GREEN+FLASH if status=="blast" else (YELLOW+FLASH if status=="warn" else RESET)
        print(f"{color}{BOLD}💥 Missile of the Moment: {symbol} ({score}) {arrow}{RESET}\n")

        # initialize on new entry
        latest_price = float(candles[-1][4])
        if tp_engine is None or tp_engine.entry != latest_price:
            atr = calc_atr(candles[-50:])
            tp_engine = TPEngine(latest_price, atr)

        current_tp = tp_engine.update(latest_price)

        print(f"{BOLD}Entry:{RESET}       {tp_engine.entry:.4f}")
        print(f"{BOLD}ATR:{RESET}         {tp_engine.atr:.4f}")
        print(f"{BOLD}Initial TP:{RESET}  {tp_engine.initial_tp:.4f}")
        print(f"{BOLD}Current TP:{RESET}  {current_tp:.4f}"
              f"  (+{(current_tp-tp_engine.entry)/tp_engine.entry*100:.2f}%)


")
        print(f"{BOLD}Rank  Symbol        Score    Status      Trajectory{RESET}")
        for i, (sym, sc, ar, st, _) in enumerate(top_scores, 1):
            c = GREEN if st=="blast" else (YELLOW if st=="warn" else RESET)
            stat = "BLAST" if st=="blast" else ("WARN" if st=="warn" else "")
            print(f"{i:<5} {sym:<12} {c}{sc:<8}{stat:<10}{ar}{RESET}")

        time.sleep(REFRESH_INTERVAL)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExiting...")
