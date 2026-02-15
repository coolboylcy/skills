---
name: water-coach
description: "Hydration tracking and coaching skill. Use when user wants to track water intake, get reminders to drink water, log body metrics (weight, body fat, muscle %, water %), or get analytics on hydration habits. Triggers on: water, hydration, drink more water, body metrics, weight tracking, water goal"
---

# Water Coach v1.0

## Quick Start

This skill helps track daily water intake and provides adaptive reminders based on progress.

## First Run (One-Time Setup)

When user first enables water tracking, create these files:

### 1. Config File
Create at `memory/water_config.json`:
```json
{
  "version": "1.0",
  "user": {
    "weight_kg": null,
    "height_m": null,
    "body_fat_pct": null,
    "muscle_pct": null,
    "water_pct": null
  },
  "settings": {
    "goal_multiplier": 35,
    "cutoff_hour": 22,
    "reminder_slots": [
      {"name": "morning", "hour": 9, "default_ml": 500},
      {"name": "lunch", "hour": 12, "default_ml": 500},
      {"name": "afternoon", "hour": 15, "default_ml": 500},
      {"name": "predinner", "hour": 18, "default_ml": 500},
      {"name": "evening", "hour": 21, "default_ml": 500}
    ]
  },
  "reports": {
    "weekly_enabled": false,
    "monthly_enabled": false
  }
}
```

### 2. Scripts (Create in memory/ or skills/water-coach/scripts/)

**calc_daily_goal.py** - Calculate goal from weight:
```python
#!/usr/bin/env python3
import json, os
CONFIG = 'memory/water_config.json'
def get_goal():
    with open(CONFIG) as f:
        w = json.load(f)['user']['weight_kg']
    return w * 35 if w else None
```

**log_water.py** - Log water intake to CSV:
```python
#!/usr/bin/env python3
import csv, json, sys, os
from datetime import datetime, date
CONFIG, LOG = 'memory/water_config.json', 'memory/water_log.csv'
# Reads config, calculates cumulative, appends to CSV
```

**log_body_metrics.py** - Log body metrics:
```python
#!/usr/bin/env python3
import csv, json, sys, os
from datetime import datetime, date
CONFIG, BODY = 'memory/water_config.json', 'memory/body_metrics.csv'
# Updates config + logs to body_metrics.csv
```

**weekly_report.py** / **monthly_report.py** - Analytics:
```python
#!/usr/bin/env python3
import csv, json, os
from datetime import datetime, date, timedelta
# Reads water_log.csv, calculates stats, returns report
```

## Configuration (First Run)

On first use, ask user for:
- **Weight** (required): Current weight in kg
- **Height** (optional): Height in meters
- **Body fat %** (optional): Body fat percentage
- **Muscle %** (optional): Muscle percentage  
- **Water %** (optional): Body water percentage

Store in `water_config.json`.

**Daily Goal Formula:**
```
daily_goal_ml = 35 × weight_kg
```

## Daily Tracking

### Reminder Slots (Base Schedule)
| Slot | Time | Default |
|------|------|---------|
| Morning | 09:00 | 500ml |
| Lunch | 12:00 | 500ml |
| Afternoon | 15:00 | 500ml |
| Pre-dinner | 18:00 | 500ml |
| Evening | 21:00 | 500ml |

### User Response Format
- `yes 500` → drank 500ml
- `yes 250` → drank 250ml
- `no` → didn't drink
- `later` → remind again in 15-20 min

### Adaptive Logic
- Behind schedule (<50%): Add extra slots
- Ahead of schedule: Reduce triggers
- Cutoff: No reminders after 22:00

### Edge Cases
- At 22:00 cutoff → auto-log 0ml for missed slots
- Retroactive: "I drank 2L today" → log 2000ml for today
- Past day: "yesterday I drank 2L" → log for yesterday

## CSV Format

**water_log.csv:**
```
timestamp,date,slot,answer,ml_drank,cumulative_ml,daily_goal,goal_pct
```

**body_metrics.csv:**
```
date,weight_kg,height_m,bmi,body_fat_pct,muscle_pct,water_pct
```

## Commands

- "start water tracking" → First run: create config + scripts, then begin reminders
- "log water [ml]" / "I drank [ml]" → Log intake
- "yesterday I drank [ml]" → Log for past day
- "body metrics [weight] [height] [fat%] [muscle%] [water%]" → Log body data
- "water report" → Weekly analytics
- "water month" → Monthly analytics
- "enable weekly report" → Schedule Sunday 10:00
- "enable monthly report" → Schedule 1st of month 10:00
