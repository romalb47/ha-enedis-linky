"""Platform for sensor integration."""
from __future__ import annotations

import voluptuous as vol

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
    PLATFORM_SCHEMA,
)
import homeassistant.helpers.config_validation as cv
from homeassistant.const import UnitOfEnergy
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_ACCESS_TOKEN, CONF_CLIENT_ID
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

import requests
import datetime


# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_ACCESS_TOKEN): cv.string,
    vol.Required(CONF_CLIENT_ID): cv.string,
})

def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the sensor platform."""
    add_entities([EnedisSensor(config)])

def get_actual_day():
    today = datetime.date.today()
    return f"{today.year}-{today.month:02d}-{today.day:02d}"

def get_previous_day():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    return f"{yesterday.year}-{yesterday.month:02d}-{yesterday.day:02d}"

class EnedisSensor(SensorEntity):
    """Representation of a Sensor."""

    _attr_name = "Linky Energy Measurement"
    _attr_native_unit_of_measurement = UnitOfEnergy.WATT_HOUR
    _attr_device_class = SensorDeviceClass.ENERGY
    _attr_state_class = SensorStateClass.MEASUREMENT

    def __init__(self, config) -> None:
        self._prm = config[CONF_CLIENT_ID]
        self._bearer_token = config[CONF_ACCESS_TOKEN]

    def update(self) -> None:
        """Fetch new state data for the sensor.

        This is the only method that should fetch new data for Home Assistant.
        """
        headers = {
            "Authorization": f"Bearer {self._bearer_token}",
            "Content-Type": "application/json"
        }

        url = f"https://conso.boris.sh/api/daily_consumption?prm={self._prm}&start={get_previous_day()}&end={get_actual_day()}"


        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            self._attr_native_value = response.json()["interval_reading"][0]["value"]
        else:
            print(f"Failed to retrieve data from API: {response.status_code}")

