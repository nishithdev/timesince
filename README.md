# ⏳ Time Since - Home Assistant Integration

Track time passed **since** a custom date — or time **remaining until** a future event — in a friendly format like “1 year, 3 months, 5 days”.

## 📦 Installation (via HACS)

1. Go to **HACS > Integrations**.
2. Click the **+ button** in the bottom-right.
3. Select **“Add Custom Repository”**, paste your GitHub repo URL and set type to **Integration**.
4. Search for **Time Since** and install it.
5. Restart Home Assistant.

## ⚙️ Configuration

After restarting, go to:

**Settings > Devices & Services > Integrations > + Add Integration > Time Since**

### Input Fields

- **Reason**: A label like `Wedding Day`, `Started Gym`, or `Vacation`.
- **Target Date**: The date for tracking (e.g. `2024-02-14`).
- **Mode**:
  - `since` → Tracks time **since** the given date.
  - `countdown` → Tracks time **until** the given date.

Each configured instance creates a sensor entity like:

- `sensor.since.started_gym`
- `sensor.countdown.vacation`

## 🧠 Example Use Cases

- **Since**:
  - How long since your wedding
  - Days since last dentist visit
  - Time since you started a new habit

- **Countdown**:
  - Days left until your next vacation
  - Countdown to a birthday or anniversary
  - Time remaining until a project deadline

## 🛠️ Notes

- The sensor state displays a breakdown like: `1 year, 2 months, 15 days`.
- If the date is invalid for the selected mode (e.g. a future date with `since`, or past date with `countdown`), a friendly message will be shown instead.

## ✅ Compatibility

This integration works entirely through the Home Assistant UI and requires no YAML configuration.