"""Sensor platform for myenergi."""
from homeassistant.components.number import NumberEntity

from .const import DOMAIN
from .entity import MyenergiEntity


async def async_setup_entry(hass, entry, async_add_devices):
    """Setup number platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    devices = []
    # Don't cause a refresh when fetching devices
    all_devices = await coordinator.client.get_devices("all", False)
    for device in all_devices:
        # Zappi only numbers
        if device.kind == "zappi":
            devices.append(MinimumGreenLevelNumber(coordinator, device, entry))
    async_add_devices(devices)


class MinimumGreenLevelNumber(MyenergiEntity, NumberEntity):
    """myenergi Sensor class."""

    def __init__(self, coordinator, device, config_entry):
        super().__init__(coordinator, device, config_entry)

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return f"{self.config_entry.entry_id}-{self.device.serial_number}-minimum_green_level"

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"myenergi {self.device.name} Minimum Green Level"

    @property
    def value(self):
        """Return the state of the sensor."""
        return self.device.minimum_green_level

    async def async_set_value(self, value: float) -> None:
        """Change the selected option."""
        await self.device.set_minimum_green_level(int(value))
        self.async_schedule_update_ha_state()

    @property
    def min_value(self):
        return 0

    @property
    def max_value(self):
        return 100

    @property
    def step(self):
        return 1
