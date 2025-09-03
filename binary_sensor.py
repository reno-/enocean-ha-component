"""Support for EnOcean binary sensors."""
import logging
import time

import voluptuous as vol

from homeassistant.components.binary_sensor import (
    DEVICE_CLASSES_SCHEMA,
    PLATFORM_SCHEMA,
    BinarySensorEntity,
)
from homeassistant.const import CONF_DEVICE_CLASS, CONF_ID, CONF_NAME
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.restore_state import RestoreEntity

from .entity import EnOceanEntity

_LOGGER = logging.getLogger(__name__)

DEFAULT_NAME = "EnOcean binary sensor"
DEPENDENCIES = ["enocean"]
EVENT_BUTTON_PRESSED = "button_pressed"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_ID): vol.All(cv.ensure_list, [vol.Coerce(int)]),
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_DEVICE_CLASS): DEVICE_CLASSES_SCHEMA,
    }
)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Binary Sensor platform for EnOcean."""
    dev_id = config.get(CONF_ID)
    dev_name = config.get(CONF_NAME)
    device_class = config.get(CONF_DEVICE_CLASS)

    add_entities([EnOceanBinarySensor(dev_id, dev_name, device_class)])


class EnOceanBinarySensor(EnOceanEntity, BinarySensorEntity):

    def __init__(self, dev_id, dev_name, device_class):
        """Initialize the EnOcean binary sensor."""
        super().__init__(dev_id, dev_name)
        self._device_class = device_class
        self._state = 0

    @property
    def name(self):
        """Return the default name for the binary sensor."""
        return self.dev_name

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return self._device_class

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    def value_changed(self, packet):
        """EEP: F6-02-02 - Nodon Soft Remote"""
        if packet.rorg == 0xF6:
            press = packet.data[1]
            if press == 0x70:
                self._state = 4
                self.schedule_update_ha_state()
                time.sleep(1)
                self._state = 0
                self.schedule_update_ha_state()
            elif press == 0x50:
                self._state = 3
                self.schedule_update_ha_state()
                time.sleep(1)
                self._state = 0
                self.schedule_update_ha_state()
            elif press == 0x30:
                self._state = 2
                self.schedule_update_ha_state()
                time.sleep(1)
                self._state = 0
                self.schedule_update_ha_state()
            elif press == 0x10:
                self._state = 1
                self.schedule_update_ha_state()
                time.sleep(1)
                self._state = 0
                self.schedule_update_ha_state()
            else:
                self._state = 0
                self.schedule_update_ha_state()
        
        """EEP: D2-03-0A - Nodon Soft Button"""
        if packet.rorg == 0xD2:
            press = packet.data[2]
            if press == 0x01:
                self._state = 1
                self.schedule_update_ha_state()
                time.sleep(1)
                self._state = 0
                self.schedule_update_ha_state()
            elif press == 0x02:
                self._state = 2
                self.schedule_update_ha_state()
                time.sleep(1)
                self._state = 0
                self.schedule_update_ha_state()
            elif press == 0x03:
                self._state = 3
                self.schedule_update_ha_state()
                time.sleep(1)
                self._state = 0
                self.schedule_update_ha_state()
            else:
                self._state = 0
                self.schedule_update_ha_state()

        """EEP: A5-07-03 - Nodon Detecteur de Mouvement"""

        if packet.rorg == 0xA5:
            press = packet.data[4]
            if press == 0x88:
                self._state = "on"
            elif press == 0x08:
                self._state = "off"
            else:
                self._state = "off"
            self.schedule_update_ha_state()