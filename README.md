# ⚽ eTipster – Football Betting Odds Filter

eTipster is a Python script that uses the [API-FOOTBALL](https://www.api-football.com/) service to fetch daily football fixtures, filter teams based on recent goal-scoring history, and create a betting ticket with matches likely to hit **Over 1.5 goals**.  

---

## 📂 Project Structure
```
.
├── config.py      # Configuration file (API key, settings, league filters)
├── etipster.py    # Core logic: API requests, match filtering, ticket creation
├── run.py         # Entry point to execute the program
```

---

## ⚙️ Configuration (`config.py`)

Before running the script, update the following parameters in **config.py**:

| Variable        | Description |
|-----------------|-------------|
| `API_KEY`       | Your **API-FOOTBALL** API key (required). |
| `TZ`            | Timezone for fetching today's matches (default: `"Europe/Vatican"`). |
| `HEADERS`       | HTTP headers for API requests (includes API key). |
| `LEAGUES_ENABLED` | Set `True` to filter only specific leagues listed in `LEAGUES`. |
| `LEAGUES`       | List of league names to include (e.g. `["Serie C", "Serie D"]`). |
| `MIN_TOT_GOALS` | Minimum total goals in each of a team’s last matches to pass the filter. |
| `LAST_MATCHES_NUM` | Number of recent matches to evaluate per team. |
| `BOOKMAKER`     | Bookmaker ID (default `8` = Bet365). |
| `BET_TYPE`      | Bet type ID (default `5` = Over/Under). |
| `MULTIPLIER`    | Minimum cumulative odds multiplier to stop selecting matches. |

---

## 🚀 Usage

1. **Install dependencies**  
   ```bash
   pip install requests pytz tqdm
   ```

2. **Set API Key**  
   Edit `config.py` and place your API key:
   ```python
   API_KEY = "YOUR_API_KEY"
   ```

3. **Run the script**  
   ```bash
   python run.py
   ```

---

## 🏆 How It Works
1. **Fetch Matches** – Gets today’s upcoming fixtures (`getTodayMatches`).  
2. **Filter Teams** – Checks each team’s recent matches. A team qualifies if it scored at least `MIN_TOT_GOALS` in all of its last `LAST_MATCHES_NUM` games (`filterMatches`).  
3. **Fetch Odds & Build Ticket** – Retrieves **Over 1.5** odds from the bookmaker and creates a ticket whose cumulative odds reach the configured `MULTIPLIER` (`createTicket`).  

---

## 📋 Example Output
```
PRENDENDO PARTITE...
12 PARTITE OGGI
5 PARTITE FILTRATE E POTENZIALI
+++++++++++++++++++++++++++++++++++++++++
AC Milan VS Juventus || 1.35
Napoli VS Roma      || 1.40
+++++++++++++++++++++++++++++++++++++++++
```

---

## ⚠️ Disclaimer
This project is for **educational purposes only**.  
Betting involves financial risk. Use at your own discretion.
