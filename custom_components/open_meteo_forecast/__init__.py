"""Open-Meteo Weather Forecast integration."""
from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_UPDATE_INTERVAL, CONF_WEATHER_ENTITY, DEFAULT_UPDATE_INTERVAL, DOMAIN
from .coordinator import OpenMeteoCoordinator

_LOGGER = logging.getLogger(__name__)

_BASE_PLATFORMS = ["sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    opts: dict[str, Any] = {**entry.data, **entry.options}
    interval = timedelta(minutes=int(opts.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)))

    coordinator = OpenMeteoCoordinator(hass, entry, interval)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    platforms = list(_BASE_PLATFORMS)
    if opts.get(CONF_WEATHER_ENTITY, False):
        platforms.append("weather")

    await hass.config_entries.async_forward_entry_setups(entry, platforms)
    entry.async_on_unload(entry.add_update_listener(_async_reload_entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    opts: dict[str, Any] = {**entry.data, **entry.options}
    platforms = list(_BASE_PLATFORMS)
    if opts.get(CONF_WEATHER_ENTITY, False):
        platforms.append("weather")

    unload_ok = await hass.config_entries.async_unload_platforms(entry, platforms)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok


async def _async_reload_entry(hass: HomeAssistant, entry: ConfigEntry) -> None:
    await hass.config_entries.async_reload(entry.entry_id)
