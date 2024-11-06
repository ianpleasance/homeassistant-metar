import logging
_LOGGER = logging.getLogger(__name__)
_LOGGER.info("METAR custom component loaded")  # Add this line

from homeassistant.helpers import discovery

async def async_setup(hass, config):
    """Set up the METAR integration."""
    # Set the integration's friendly name for the UI
    hass.data["metar_integration"] = {
        "name": "METAR and TAFs"
    }
    return True
