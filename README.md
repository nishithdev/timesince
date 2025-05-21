# ⏳ Time Since - Home Assistant Integration

Track time passed since a custom date with a friendly format like “1 year, 3 months, 5 days”.

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

- **Reason**: A label like `Wedding Day` or `Started Gym`.
- **Start Date**: The date from which time will be tracked (e.g. `2024-02-14`).

Each configured instance creates a sensor entity like: