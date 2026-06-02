from datetime import date
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import homeassistant.util.dt as dt_util
from .const import DOMAIN, CONF_DATE, CONF_REASON, CONF_MODE


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([TimeSinceSensor(entry)])


class TimeSinceSensor(SensorEntity):
    _attr_icon = "mdi:calendar-clock"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTime.DAYS

    def __init__(self, entry: ConfigEntry) -> None:
        self._reason = entry.data[CONF_REASON]
        self._mode = entry.data.get(CONF_MODE, "since")
        slug = self._reason.lower().replace(" ", "_")
        self._attr_name = f"{self._mode}.{slug}"
        self._attr_unique_id = f"{DOMAIN}_{self._mode}.{slug}"
        self._target_date = date.fromisoformat(
            entry.options.get(CONF_DATE, entry.data[CONF_DATE])
        )

    def _delta_days(self) -> int | None:
        today = dt_util.now().date()
        if self._mode == "since":
            delta = (today - self._target_date).days
        else:
            delta = (self._target_date - today).days
        return delta if delta >= 0 else None

    @property
    def native_value(self) -> int | None:
        return self._delta_days()

    @property
    def extra_state_attributes(self) -> dict:
        delta = self._delta_days()
        if delta is None:
            msg = "Date is in the future" if self._mode == "since" else "Date has passed"
            return {"status": msg}
        if delta == 0:
            return {"display": "Today", "years": 0, "months": 0, "days": 0, "total_days": 0}
        years = delta // 365
        months = (delta % 365) // 30
        rem_days = (delta % 365) % 30
        parts = []
        if years:
            parts.append(f"{years} year{'s' if years != 1 else ''}")
        if months:
            parts.append(f"{months} month{'s' if months != 1 else ''}")
        if rem_days or not parts:
            parts.append(f"{rem_days} day{'s' if rem_days != 1 else ''}")
        return {
            "display": ", ".join(parts),
            "years": years,
            "months": months,
            "days": rem_days,
            "total_days": delta,
        }
