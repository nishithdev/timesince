import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from datetime import datetime, date
from .const import DOMAIN, CONF_NAME, CONF_DATE, CONF_REASON, CONF_MODE

class TimeSinceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            try:
                # Parse and validate date
                target_date = datetime.strptime(user_input[CONF_DATE], "%Y-%m-%d").date()
                today = date.today()
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
            vol.Required(CONF_DATE): str,  # Format: YYYY-MM-DD
            vol.Required(CONF_MODE, default="since"): vol.In(["since", "countdown"])
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)