# homeassistant-metar

[METAR and TAF integration](https://github.com/ianpleasance/homeassistant-metar) for homeassistant

# What This Is:

A custom integration for Home Assistant which retrieves METAR and TAF observations.

# What It Does:

This integration is designed for use by pilots who want a convenient way to retrieve METAR and TAF observations for display through Home Assistant.

It retrieves the latest METAR/TAF information for one or more airfields and creates sensor entities for them. These can then be used for display on Lovelace cards, or in automations or reports.

Data is pulled from the Aviation Weather site API at https://aviationweather.gov/api/

# Installation and Configuration

This is a custom component, and needs to be manually installed into your Home Assistant folder. Assuming you are on some sort of Linux server installation should look like this

```
$ git clone https://github.com/ianpleasance/homeassistant-metar.git
$ cd homeassistant-metar
$ cd custom_components
$ cp -rp metar /usr/share/hassio/homeassistant/custom_components
```

then add to your configuration.yaml the list of desired ICAO airport codes, and optionally the scan interval to refresh them.

```
sensor:
  - platform: metar
    airfields:
      - EGLL
      - EGMC
      - EGSH
      - EGSS
      - EGUW
      - EGSC
      - EGLC
    scan_interval: "00:10:00"  # Optional: set scan interval to 10 minutes
```

and restart Home Assistant

Under Settings|Integrations|Entities you should now find a group of sensors per airfield/data item, for example

```
METAR EGLC Altimeter - sensor.metar_eglc_altimiter - 1031
```

The sensors created are 

_altimeter - Current altimeter QNH
_dew_point - Current dew point in C
_elevation - Airfield elevation in Feet
_latitude - Airfield Latitude
_longitude - Airfield Longitude
_metar_id - Unique METAR ID
_name - Airfield name in English
_raw_ob - Raw METAR
_raw_taf - Raw TAF
_report_time - Time of report
_temperature - Current temperature in C
_visibility - Current visibility in km
_wind_direction - Current wind direction in Degrees
_wind_gust - Current wind gust speed
_wind_speed - Current wind speed

# Known issues

Gust Speed is often empty, a future enhancement will pull this from the METAR

# Planned enhancements

1. Creation of missing sensor information from METAR
2. Optional creation of sensors for METAR/TAF with decoded information
3. Ability to configure via the HASS Web Interface rather than configuration.yaml


# License

[Apache-2.0](LICENSE). By providing a contribution, you agree the contribution is licensed under Apache-2.0. This is required for Home Assistant contributions.

