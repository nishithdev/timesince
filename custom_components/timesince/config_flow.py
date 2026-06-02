from datetime import date
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from homeassistant.helpers import selector
import homeassistant.util.dt as dt_util
from .const import DOMAIN, CONF_NAME, CONF_DATE, CONF_REASON, CONF_MODE

_MODE_OPTIONS = [
    {"label": "Since — tracks time elapsed since a past date", "value": "since"},
    {"label": "Countdown — tracks time remaining until a future date", "value": "countdown"},
]


def _schema(defaults: dict | None = None) -> vol.Schema:
    d = defaults or {}
    return vol.Schema({
        vol.Required(CONF_REASON, default=d.get(CONF_REASON, "")): selector.TextSelector(
            selector.TextSelectorConfig(type=selector.TextSelectorType.TEXT)
        ),
        vol.Required(CONF_DATE, default=d.get(CONF_DATE, "")): selector.DateSelector(),
        vol.Required(CONF_MODE, default=d.get(CONF_MODE, "since")): selector.SelectSelector(
            selector.SelectSelectorConfig(
                options=_MODE_OPTIONS,
                mode=selector.SelectSelectorMode.LIST,
            )
        ),
    })


def _validate(user_input: dict) -> dict:
    errors: dict = {}
    try:
        target_date = date.fromisoformat(user_input[CONF_DATE])
        today = dt_util.now().date()
        mode = user_input.get(CONF_MODE, "since")
        if mode == "since" and target_date > today:
            errors["base"] = "date_in_future_for_since"
        elif mode == "countdown" and target_date < today:
            errors["base"] = "date_in_past_for_countdown"
    except (ValueError, KeyError, TypeError):
        errors["base"] = "invalid_date"
    return errors


class TimeSinceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            errors = _validate(user_input)
            if not errors:
                reason = user_input[CONF_REASON]
                mode = user_input[CONF_MODE]
                name = f"{mode}.{reason.lower().replace(' ', '_')}"
                user_input[CONF_NAME] = name
                return self.async_create_entry(title=name, data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=_schema(user_input), errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> "TimeSinceOptionsFlow":
        return TimeSinceOptionsFlow(config_entry)


class TimeSinceOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}
        if user_input is not None:
            errors = _validate(user_input)
            if not errors:
                return self.async_create_entry(title="", data=user_input)

        entry = self._config_entry
        current = {
            CONF_REASON: entry.options.get(CONF_REASON, entry.data.get(CONF_REASON, "")),
            CONF_DATE: entry.options.get(CONF_DATE, entry.data.get(CONF_DATE, "")),
            CONF_MODE: entry.options.get(CONF_MODE, entry.data.get(CONF_MODE, "since")),
        }
        return self.async_show_form(
            step_id="init", data_schema=_schema(current), errors=errors
        )
