from datetime import date
from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
import homeassistant.util.dt as dt_util
from .const import DOMAIN, CONF_DATE, CONF_REASON, CONF_MODE, MILESTONES_SINCE, MILESTONES_COUNTDOWN


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    async_add_entities([TimeSinceSensor(entry)])


class TimeSinceSensor(SensorEntity):
    _attr_icon = "mdi:calendar-clock"
    _attr_state_class = SensorStateClass.MEASUREMENT
    _attr_native_unit_of_measurement = UnitOfTime.DAYS

    def __init__(self, entry: ConfigEntry) -> None:
        self._reason = entry.options.get(CONF_REASON, entry.data[CONF_REASON])
        self._mode = entry.options.get(CONF_MODE, entry.data.get(CONF_MODE, "since"))
        slug = self._reason.lower().replace(" ", "_")
        self._attr_name = f"{self._mode}.{slug}"
        self._attr_unique_id = f"{DOMAIN}_{entry.entry_id}"
        self._target_date = date.fromisoformat(
            entry.options.get(CONF_DATE, entry.data[CONF_DATE])
        )

    def _delta_days(self) -> int | None:
        today = dt_util.now().date()
        delta = (today - self._target_date).days if self._mode == "since" else (self._target_date - today).days
        return delta if delta >= 0 else None

    def _next_milestone(self, delta: int) -> tuple[int, int] | None:
        milestones = MILESTONES_SINCE if self._mode == "since" else MILESTONES_COUNTDOWN
        for milestone in milestones:
            if (self._mode == "since" and delta < milestone) or (self._mode == "countdown" and delta > milestone):
                return milestone, abs(milestone - delta)
        return None

    def _anniversary_info(self) -> tuple[int, bool]:
        today = dt_util.now().date()
        year = today.year
        try:
            ann = self._target_date.replace(year=year)
        except ValueError:
            ann = date(year, 2, 28)
        if ann < today:
            try:
                ann = self._target_date.replace(year=year + 1)
            except ValueError:
                ann = date(year + 1, 2, 28)
        return (ann - today).days, ann == today

    @property
    def native_value(self) -> int | None:
        return self._delta_days()

    @property
    def extra_state_attributes(self) -> dict:
        delta = self._delta_days()
        if delta is None:
            msg = "Date is in the future" if self._mode == "since" else "Date has passed"
            return {"status": msg}

        attrs: dict = {"total_days": delta, "total_weeks": delta // 7}

        if delta == 0:
            attrs.update({"display": "Today", "years": 0, "months": 0, "days": 0})
        else:
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
            attrs.update({"display": ", ".join(parts), "years": years, "months": months, "days": rem_days})

        milestone = self._next_milestone(delta)
        if milestone is not None:
            attrs["next_milestone"] = milestone[0]
            attrs["days_to_milestone"] = milestone[1]

        if self._mode == "since":
            days_to_ann, is_ann = self._anniversary_info()
            attrs["days_to_anniversary"] = days_to_ann
            attrs["is_anniversary"] = is_ann

        return attrs
