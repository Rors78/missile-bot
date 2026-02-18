# Missile Bot - Explosive Breakout Scanner

A real-time cryptocurrency scanner that detects explosive breakout moves with volume confirmation and ATR-based trailing profit targets.

## Overview

Missile Bot continuously scans Binance.US for "missile" movements - rapid price breakouts accompanied by high volume spikes. The bot uses ATR (Average True Range) based trailing stops to lock in profits as the price continues to move.

## Key Features

- **Real-Time Scanning**: Monitors all USDT pairs on Binance.US
- **Breakout Detection**: Identifies explosive price moves with volume confirmation
- **ATR-Based Targets**: Dynamic profit targets using Average True Range
- **Trailing System**: Automatically trails stops as price advances
- **Visual Alerts**: Color-coded terminal output with flashing alerts
- **Top Movers**: Displays top 10 strongest signals
- **Lightweight**: No API keys required (public data only)

## Breakout Detection Algorithm

The bot calculates a **breakout score** based on:

1. **Price Change**: Percentage move from recent levels
2. **Volume Spike**: Recent volume vs. historical average
3. **Momentum**: Price slope (trending direction)
4. **Composite Score**: (Price Change % × Volume Ratio)

### Signal Categories

**🚀 BLAST** (Missile Detected!):
- Score > 10
- Strong upward slope (>1%)
- Volume spike >3x average
- **Action**: Prime entry opportunity

**⚠️ WARN** (Warming Up):
- Score > 4
- Moderate slope (>0.5%)
- Volume spike >2x average
- **Action**: Watch for acceleration

**→ NEUTRAL**:
- Below thresholds
- Normal trading activity
- **Action**: Monitor only

## Trailing Profit Target System

### ATR-Based TP Engine

When a position is entered:

1. **Initial Target**: Entry + (2.0 × ATR)
2. **Trailing Step**: 1.0 × ATR
3. **Lock-In Logic**:
   - As price makes new highs, TP advances by ATR steps
   - Never moves down (only up)
   - Locks in profits while allowing room for continuation

### Example
```
Entry: $100
ATR: $2
Initial TP: $104 (100 + 2×2)

Price hits $103: TP stays at $104
Price hits $105: New high! TP advances to $106 (100 + 3×2)
Price hits $107: New high! TP advances to $108 (100 + 4×2)
Price drops to $106: TP stays at $108 (trailing stop)
```

## Installation

### Requirements
- Python 3.7+
- requests library

**Windows:**
```powershell
pip install requests
```

**Linux/macOS:**
```bash
pip3 install requests
```

## Usage

### Basic Run
**Windows:**
```powershell
python missile_bot.py
```

**Linux/macOS:**
```bash
python3 missile_bot.py
```

### Windows
```batch
launch_missile_bot.bat
```

### Terminal Output

```
=== MISSILE BOT === 2025-12-31 00:10:45
Scanning 150 pairs... Refresh: 10s

TOP 10 MISSILES:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 Pair        Price    Score  Arrow  Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀BTCUSDT   42,150   15.8   ↗      BLAST ⚡
 ETHUSDT     2,245    8.3   ↗      WARN
 XRPUSDT     0.615    6.2   ↗      WARN
 ...
```

## Configuration

Edit the constants at the top of `missile_bot.py`:

```python
REFRESH_INTERVAL    = 10    # Scan frequency (seconds)
TOP_N               = 10    # Show top N movers
ATR_PERIOD          = 14    # ATR calculation period
INITIAL_ATR_MULT    = 2.0   # Initial TP distance (2x ATR)
TRAILING_STEP_MULT  = 1.0   # Trailing step size (1x ATR)
```

### Customization Examples

**More Aggressive (Faster Signals)**:
```python
INITIAL_ATR_MULT    = 1.5   # Closer TP
TRAILING_STEP_MULT  = 0.75  # Smaller steps
```

**More Conservative (Stronger Confirmation)**:
```python
INITIAL_ATR_MULT    = 3.0   # Wider TP
TRAILING_STEP_MULT  = 1.5   # Larger steps
```

## How It Works

### Scan Cycle

1. **Fetch Pairs**: Get all active USDT trading pairs
2. **Get Candles**: Retrieve 1-minute klines for each pair
3. **Calculate Metrics**:
   - ATR (volatility measure)
   - Price change
   - Volume ratio
   - Momentum slope
4. **Score & Rank**: Calculate breakout scores and sort
5. **Display**: Show top signals with color-coded status
6. **Repeat**: Wait REFRESH_INTERVAL and scan again

### Indicators Used

**ATR (Average True Range)**:
- Measures volatility
- Used for setting realistic profit targets
- Adapts to each coin's movement characteristics

**Volume Analysis**:
- Compares recent 3-candle volume to historical average
- Filters false breakouts (requires volume confirmation)

**Price Slope**:
- Calculates rate of change
- Identifies trending vs. ranging movements

## Visual Indicators

### Colors
- 🟢 **GREEN**: BLAST status (strong signal)
- 🟡 **YELLOW**: WARN status (moderate signal)
- ⚪ **WHITE**: NEUTRAL status
- 🔴 **RED**: (reserved for errors)

### Arrows
- **↗** : Upward momentum
- **→** : Sideways/neutral
- **↘** : Downward momentum

### Status Badges
- **⚡ BLAST**: Flashing indicator for strongest signals
- **WARN**: Caution - building momentum
- **neutral**: Normal activity

## Use Cases

### 1. Scalping Scanner
Monitor for explosive 1-minute breakouts to catch quick moves.

### 2. Entry Finder
Identify coins showing unusual activity for deeper analysis.

### 3. Volatility Monitor
Track which pairs are most active at any given time.

### 4. Alert System
Run in background to catch opportunities as they develop.

## Trading Integration

**Manual Trading**:
1. Bot flags potential moves
2. Trader confirms setup on exchange
3. Enter position
4. Use bot's TP levels for exit planning

**Automated Trading** (Advanced):
The TP Engine class can be integrated into trading bots:
```python
# Example integration
tp = TPEngine(entry_price=100, atr=2)
current_tp = tp.update(current_price=105)
# Use current_tp for your sell order
```

## Performance Tips

### Reduce API Load
```python
REFRESH_INTERVAL = 15  # Slower scanning
TOP_N = 5              # Show fewer pairs
```

### Focus on Specific Pairs
Modify `fetch_binance_pairs()` to filter by specific coins:
```python
filtered = [s for s in pairs if s in ['BTCUSDT', 'ETHUSDT', 'XRPUSDT']]
```

## Limitations

- **Paper Trading Only**: Scanner does not execute trades
- **1-Minute Data**: Uses 1m candles (may miss longer-term setups)
- **Public API**: Subject to Binance rate limits
- **No Historical Testing**: Real-time only (not a backtester)
- **Market Hours**: Best during high-volume periods

## Troubleshooting

### Slow Scanning
- Increase `REFRESH_INTERVAL`
- Reduce number of pairs scanned
- Check internet connection

### No Signals
- Market may be ranging (low volatility)
- Adjust thresholds in `calc_breakout_score()`
- Check if Binance.US is accessible

### API Errors
- Ensure stable internet
- Verify Binance.US endpoint is operational
- Check for rate limiting

## Advanced Features

### Custom Scoring
Modify `calc_breakout_score()` to weight factors differently:
```python
score = (price_change * 100) * (vol_ratio ** 1.5)  # Emphasize volume more
```

### Multi-Timeframe
Scan multiple timeframes by changing:
```python
fetch_binance_klines(symbol, interval="5m", limit=100)
```

### Sound Alerts
Add audio notification on BLAST signals:
```python
if status == "blast":
    os.system('echo -e "\a"')  # Terminal beep
```

## Safety Notes

- This is a **scanning tool**, not a trading bot
- Always verify signals on exchange before trading
- Past performance doesn't guarantee future results
- Cryptocurrency trading is risky
- Never risk more than you can afford to lose

## License

Provided as-is for personal use and learning.

---

> **API keys are optional.** Paper/read-only mode uses the public REST API — no account or key required. Keys are only needed for live order execution.

**Detect the missiles before they launch** 🚀
