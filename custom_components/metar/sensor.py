import logging
import aiohttp
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import async_get_platforms

_LOGGER = logging.getLogger(__name__)

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the METAR sensors from configuration.yaml."""
    
    airfields = config.get("airfields", [])
    scan_interval = config.get("scan_interval", 600)  # Default to 10 minutes if not specified

    # Log the airfields for debugging
    _LOGGER.info("Configured airfields: %s", airfields)

    # Track active airfields in Home Assistant's state
    if "metar_airfields" not in hass.data:
        hass.data["metar_airfields"] = set()

    # Identify airfields to remove and add
    current_airfields = set(airfields)
    previous_airfields = hass.data["metar_airfields"]
    airfields_to_remove = previous_airfields - current_airfields
    airfields_to_add = current_airfields - previous_airfields

    # Remove entities for any airfields no longer in the config
    platform = async_get_platforms(hass, "metar")
    for airfield in airfields_to_remove:
        _LOGGER.info("Removing entities for airfield %s", airfield)
        for entity in platform[0].entities:
            if entity.unique_id.startswith(f"metar_{airfield.lower()}"):
                await entity.async_remove()

    # Create and add sensors for new or updated airfields
    entities = []
    for airfield in airfields_to_add:
        entities.extend(await create_metar_sensors(airfield))

    async_add_entities(entities, True)

    # Update the tracked list of active airfields
    hass.data["metar_airfields"] = current_airfields

async def create_metar_sensors(airfield):
    """Create METAR sensors for each field in the METAR data."""
    sensors = []

    url = f"https://aviationweather.gov/api/data/metar?ids={airfield}&format=json&taf=true&hours=0"
    _LOGGER.info("Fetching METAR data from %s", url)

    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    json_data = await response.json()
                    _LOGGER.info("Received data: %s", json_data)

                    # Create sensors for each field
                    if json_data:
                        metar_data = json_data[0]  # Assuming the first item contains the relevant data
                        sensors.append(METARSensor(airfield, "metar_id", metar_data['metar_id']))
                        sensors.append(METARSensor(airfield, "report_time", metar_data['reportTime']))
                        sensors.append(METARSensor(airfield, "temperature", metar_data['temp']))
                        sensors.append(METARSensor(airfield, "dew_point", metar_data['dewp']))
                        sensors.append(METARSensor(airfield, "wind_direction", metar_data['wdir']))
                        sensors.append(METARSensor(airfield, "wind_speed", metar_data['wspd']))
                        sensors.append(METARSensor(airfield, "wind_gust", metar_data['wgst']))
                        sensors.append(METARSensor(airfield, "visibility", metar_data['visib']))
                        sensors.append(METARSensor(airfield, "altimeter", metar_data['altim']))
                        sensors.append(METARSensor(airfield, "latitude", metar_data['lat']))
                        sensors.append(METARSensor(airfield, "longitude", metar_data['lon']))
                        sensors.append(METARSensor(airfield, "elevation", metar_data['elev']))
                        sensors.append(METARSensor(airfield, "raw_ob", metar_data['rawOb']))
                        sensors.append(METARSensor(airfield, "raw_taf", metar_data['rawTaf']))
                        sensors.append(METARSensor(airfield, "name", metar_data['name']))
                else:
                    _LOGGER.error("Failed to fetch data, status code: %s", response.status)
        except Exception as e:
            _LOGGER.error("Error fetching METAR data: %s", str(e))

    return sensors

class METARSensor(Entity):
    """Representation of a METAR sensor."""

    def __init__(self, airfield, field_name, value):
        """Initialize the sensor."""
        self._airfield = airfield
        self._field_name = field_name
        self._value = value

    @property
    def name(self):
        # Format the field name: e.g., 'dew_point' becomes 'Dew Point'
        formatted_field_name = self._field_name.replace('_', ' ').title()
        return f"METAR {self._airfield} {formatted_field_name}"

    @property
    def state(self):
        return self._value

    @property
    def extra_state_attributes(self):
        return {
            "airfield": self._airfield,
            "field_name": self._field_name
        }

