from datetime import datetime, date
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, CONF_NAME, CONF_DATE, CONF_REASON, CONF_MODE

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    async_add_entities([TimeSinceSensor(entry)])

class TimeSinceSensor(Entity):
    def __init__(self, entry: ConfigEntry):
        self._reason = entry.data[CONF_REASON]
        self._mode = entry.data.get(CONF_MODE, "since")  # default to "since"
        self._name = f"{self._mode}.{self._reason.lower().replace(' ', '_')}"
        self._target_date = datetime.strptime(entry.data[CONF_DATE], "%Y-%m-%d").date()
        self._attr_unique_id = f"{DOMAIN}_{self._name}"

    @property
    def name(self):
        return self._name

    @property
    def unique_id(self):
        return self._attr_unique_id

    @property
    def icon(self):
        return "mdi:calendar-clock"

    @property
    def state(self):
        today = date.today()

        if self._mode == "since":
            delta_days = (today - self._target_date).days
            if delta_days < 0:
                return "Date is in the future"
        else:  # countdown
            delta_days = (self._target_date - today).days
            if delta_days < 0:
                return "Date has passed"

        years = delta_days // 365
        months = (delta_days % 365) // 30
        rem_days = (delta_days % 365) % 30

        parts = []
        if years:
            parts.append(f"{years} year{'s' if years != 1 else ''}")
        if months:
            parts.append(f"{months} month{'s' if months != 1 else ''}")
        if rem_days or not parts:
            parts.append(f"{rem_days} day{'s' if rem_days != 1 else ''}")

        return ", ".join(parts)