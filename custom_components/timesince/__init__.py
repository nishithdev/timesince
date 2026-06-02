import voluptuous as vol
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers import entity_registry as er
import homeassistant.util.dt as dt_util
from .const import DOMAIN, CONF_DATE


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    async def handle_reset_to_today(call: ServiceCall) -> None:
        entity_id = call.data["entity_id"]
        registry = er.async_get(hass)
        entity_entry = registry.async_get(entity_id)
        if entity_entry is None or entity_entry.config_entry_id is None:
            raise HomeAssistantError(f"Entity {entity_id} not found")
        config_entry = hass.config_entries.async_get_entry(entity_entry.config_entry_id)
        if config_entry is None:
            raise HomeAssistantError(f"Config entry not found for {entity_id}")
        today = dt_util.now().date().isoformat()
        hass.config_entries.async_update_entry(
            config_entry, options={**config_entry.options, CONF_DATE: today}
        )

    hass.services.async_register(
        DOMAIN,
        "reset_to_today",
        handle_reset_to_today,
        schema=vol.Schema({vol.Required("entity_id"): cv.entity_id}),
    )
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
