# ⏳ Time Since — Home Assistant Integration

A Home Assistant integration that creates a sensor tracking how long it has been **since** a past date, or how many days are **remaining until** a future event.

The sensor state is the number of days, and a human-readable breakdown like `"1 year, 3 months, 5 days"` is available as the `display` attribute — ready to use in dashboards, automations, and templates.

---

## What You Get

After setup, each configured entry creates one sensor entity:

| Sensor | State | `display` attribute |
|--------|-------|---------------------|
| `sensor.since.started_gym` | `428` | `1 year, 2 months, 3 days` |
| `sensor.countdown.vacation` | `14` | `14 days` |

Additional attributes exposed per sensor:

| Attribute | Description |
|-----------|-------------|
| `display` | Human-readable breakdown (e.g. `"2 years, 1 month, 4 days"`) |
| `years` | Years component |
| `months` | Months component |
| `days` | Days component |
| `total_days` | Total elapsed or remaining days (same as sensor state) |

When the date is `today`, the `display` attribute shows `"Today"`.  
When the date is invalid for the mode (e.g. a future date in `since` mode), the sensor state is `unavailable` and a `status` attribute explains why.

---

## Installation

### Option 1 — HACS (Recommended)

1. Open **HACS** in your Home Assistant sidebar.
2. Go to **Integrations**.
3. Click the **⋮ menu** (top-right) → **Custom Repositories**.
4. Paste this URL and set the category to **Integration**:
   ```
   https://github.com/nishithdev/timesince
   ```
5. Click **Add**.
6. Search for **Time Since** in HACS and click **Download**.
7. **Restart Home Assistant**.

### Option 2 — Manual

1. Download or clone this repository.
2. Copy the `custom_components/timesince/` folder into your HA config directory:
   ```
   <config>/custom_components/timesince/
   ```
3. **Restart Home Assistant**.

---

## Setup

After restarting, add the integration through the HA UI:

**Settings → Devices & Services → + Add Integration → search "Time Since"**

Fill in the form:

| Field | Description | Example |
|-------|-------------|---------|
| **Reason** | A short label for what you're tracking | `Started Gym` |
| **Target Date** | The date in `YYYY-MM-DD` format | `2023-01-15` |
| **Mode** | `since` for past dates, `countdown` for future dates | `since` |

Click **Submit**. The sensor appears immediately — no restart needed.

You can add as many sensors as you like by repeating the process.

### Editing a Sensor

To change the target date after setup:

**Settings → Devices & Services → Time Since → Configure**

This opens the edit form without needing to delete and re-add the sensor.

---

## Example Use Cases

**Since (past dates)**
- Days since your last dentist visit
- How long you've been at your current job
- Time since you started a new habit or workout routine

**Countdown (future dates)**
- Days until your next vacation
- Countdown to a birthday or anniversary
- Time remaining until a project deadline

---

## Using in Dashboards & Automations

**Show the readable breakdown in a card:**
```yaml
type: entity
entity: sensor.since.started_gym
attribute: display
```

**Trigger an automation on an anniversary:**
```yaml
trigger:
  - platform: numeric_state
    entity_id: sensor.since.started_gym
    value_template: "{{ state.attributes.days == 0 and state.attributes.months == 0 }}"
    above: 364
```

**Use in a template:**
```yaml
{{ state_attr('sensor.since.started_gym', 'display') }}
# → "1 year, 2 months, 3 days"
```

---

## Compatibility

- **Home Assistant**: 2023.0.0 or newer
- **Installation**: UI only — no YAML configuration required
- **Dependencies**: None (uses only built-in HA libraries)
