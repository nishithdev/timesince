import voluptuous as vol
from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import callback
from datetime import datetime
import homeassistant.util.dt as dt_util
from .const import DOMAIN, CONF_NAME, CONF_DATE, CONF_REASON, CONF_MODE


class TimeSinceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                target_date = datetime.strptime(user_input[CONF_DATE], "%Y-%m-%d").date()
                today = dt_util.now().date()
                mode = user_input.get(CONF_MODE, "since")

                if mode == "since" and target_date > today:
                    errors["base"] = "date_in_future_for_since"
                elif mode == "countdown" and target_date < today:
                    errors["base"] = "date_in_past_for_countdown"
                else:
                    reason = user_input[CONF_REASON]
                    name = f"{mode}.{reason.lower().replace(' ', '_')}"
                    user_input[CONF_NAME] = name
                    return self.async_create_entry(title=name, data=user_input)

            except ValueError:
                errors["base"] = "invalid_date"

        schema = vol.Schema({
            vol.Required(CONF_REASON): str,
            vol.Required(CONF_DATE): str,
            vol.Required(CONF_MODE, default="since"): vol.In(["since", "countdown"]),
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

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
            try:
                target_date = datetime.strptime(user_input[CONF_DATE], "%Y-%m-%d").date()
                today = dt_util.now().date()
                mode = self._config_entry.data.get(CONF_MODE, "since")

                if mode == "since" and target_date > today:
                    errors["base"] = "date_in_future_for_since"
                elif mode == "countdown" and target_date < today:
                    errors["base"] = "date_in_past_for_countdown"
                else:
                    return self.async_create_entry(title="", data=user_input)
            except ValueError:
                errors["base"] = "invalid_date"

        current_date = self._config_entry.options.get(
            CONF_DATE, self._config_entry.data.get(CONF_DATE, "")
        )
        schema = vol.Schema({
            vol.Required(CONF_DATE, default=current_date): str,
        })

        return self.async_show_form(step_id="init", data_schema=schema, errors=errors)
