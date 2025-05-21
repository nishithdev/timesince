import voluptuous as vol
from homeassistant import config_entries
from .const import DOMAIN, CONF_NAME, CONF_DATE, CONF_REASON, CONF_MODE

class TimeSinceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 2

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            reason = user_input[CONF_REASON]
            mode = user_input.get(CONF_MODE, "since")
            name = f"{mode}.{reason.lower().replace(' ', '_')}"
            user_input[CONF_NAME] = name
            return self.async_create_entry(title=name, data=user_input)

        schema = vol.Schema({
            vol.Required(CONF_REASON): str,
            vol.Required(CONF_DATE): str,  # Format: YYYY-MM-DD
            vol.Required(CONF_MODE, default="since"): vol.In(["since", "countdown"])
        })

        return self.async_show_form(step_id="user", data_schema=schema)