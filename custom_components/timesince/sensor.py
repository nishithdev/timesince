from datetime import datetime, date
from homeassistant.helpers.entity import Entity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .const import DOMAIN, CONF_NAME, CONF_DATE, CONF_REASON

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback):
    async_add_entities([TimeSinceSensor(entry)])

class TimeSinceSensor(Entity):
    def __init__(self, entry: ConfigEntry):
        self._reason = entry.data[CONF_REASON]
        self._name = f"since.{self._reason.lower().replace(' ', '_')}"
        self._start_date = datetime.strptime(entry.data[CONF_DATE], "%Y-%m-%d").date()
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
        days = (today - self._start_date).days
        years = days // 365
        months = (days % 365) // 30
        rem_days = (days % 365) % 30
        parts = []
        if years: parts.append(f"{years} year{'s' if years != 1 else ''}")
        if months: parts.append(f"{months} month{'s' if months != 1 else ''}")
        if rem_days: parts.append(f"{rem_days} day{'s' if rem_days != 1 else ''}")
        return ", ".join(parts)
