# home_assistant_viaris

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)   ![GitHub all releases](https://img.shields.io/github/downloads/orbis-developers/home_assistant_viaris/total)

Home Assistant integration for monitoring Viaris UNI and COMBIPLUS model chargers with mqtt protocol.

## Features

The EV Charger Integration for Home Assistant offers comprehensive information about your charger configuration, along with the necessary states and measures to effectively monitor the charging process. This integration provides valuable insights into various aspects, including active/reactive power/energy measurements, connector states, power configuration, and available analyzers, among others. Besides, users have the possibility of starting and stopping the charge and changing the current in each connector

## List of entities view

This screenshot shows different entities that you can choose to make your dashboard.

![image](https://github.com/orbis-developers/home_assistant_viaris/assets/66405397/c8373582-edf8-451e-a36d-271f228d2720)

## Dashboard example view

![imagen](https://github.com/HGC72/home_assistant_viaris/assets/66405397/1dae3325-d01c-411d-baef-d84fcc1614ed)

## Installation

Use HACS to install this custom component. Under HACS, choose Integrations and add the viaris custom repository.

## Configuration

To add the viaris EV charger integration, firstly the MQTT integration needs to be configured with your broker credentials. The system can automatically discover all of the devices that are connected, after switching them on and restarting Home Assistant. The discovery process is only done at the beginning when none of the devices are configured. There is another way to add the integration using the web UI, entering your charger serial number.

#### Discovering devices:

![imagen](https://github.com/orbis-developers/home_assistant_viaris/assets/66405397/8ac0e34b-e5ee-4af8-a250-07c7dd92294a)

After that, you configure each device.

#### Entering serial number:

![imagen](https://github.com/HGC72/home_assistant_viaris/assets/66405397/465c169d-b4e3-43ec-8754-68f0a5c63567)

Installed devices

![imagen](https://github.com/orbis-developers/home_assistant_viaris/assets/66405397/e47f3b9b-ef70-46d3-b996-40fa22635158)

After activating the integration the user must restart Home Assistant.

## Entities

Once your device has been configured, you will see the integration entities.

![imagen](https://github.com/HGC72/home_assistant_viaris/assets/66405397/a453e0b5-7948-4942-bfbb-6d2ad0601608)

### Sensors

| Friendly name | Category | Units | Supported | Unsupported reason |
| ------------- | -------- | ----- | --------- | ------------------ |
| Contax D0613  |   |       | :heavy_check_mark: |  |
| Ethernet |   |  | :heavy_check_mark: | |
| Firmware application version |   |   | :heavy_check_mark: | |
| Firmware cortex version |   |   | :heavy_check_mark: | |
| Firmware application version |   |   | :heavy_check_mark: |  |
| Hardware power version |   |   | :heavy_check_mark: | |
| Hardware version |   |   | :heavy_check_mark: |  |
| Keep alive |   |  | :heavy_check_mark: |  |
| Limit power |   | kW  | :heavy_check_mark: | |
| Mac |   |   | :heavy_check_mark: | |
| Max power |   | kW  | :heavy_check_mark: | |
| Modbus |   |   | :heavy_check_mark: | |
| Model |   |   | :heavy_check_mark: | |
| Mqtt clien Id |   |   | :heavy_check_mark: | |
| Mqtt pin Interval |   |  | :heavy_check_mark: | |
| Mqtt port |   |   | :heavy_check_mark: | |
| Mqtt QoS |   |   | :heavy_check_mark: | |
| Mqtt clien Id |  |   | :heavy_check_mark: | |
| Mqtt URL |   |   | :heavy_check_mark: | |
| Mqtt user |   |   | :heavy_check_mark: | |
| Ocpp |   |   | :heavy_check_mark: | |
| Rfid |   |   | :heavy_check_mark: | |
| Schuko present |   |   | :heavy_check_mark: | |
| Selector power|   |   | :heavy_check_mark: | |
| Serial |   |   | :heavy_check_mark: | |
| Solar |   |   | :heavy_check_mark: | |
| Spl |   |   | :heavy_check_mark: | |
| TMC100 |   |   | :heavy_check_mark: | |
| Current max power |   | kW  | :heavy_check_mark: | |
| Active energy connector 1 | `Diagnostic` | kWh   | :heavy_check_mark: | |
| Active energy connector 2 | `Diagnostic` | kWh  || Not supported in all devices|
| Reactive energy connector 1 | `Diagnostic` | kVarh   |:heavy_check_mark: | |
| Reactive energy connector 2 | `Diagnostic` | kVarh   | | Not supported in all devices|
| Evse power | `Diagnostic` | kW   | :heavy_check_mark: | |
| Home power | `Diagnostic` | kW   | :heavy_check_mark: | |
| Overload rel | `Diagnostic` |   | :heavy_check_mark: | |
| Active power connector 1 | `Diagnostic` | kW|   :heavy_check_mark: | |
| Active power connector 2 | `Diagnostic` | kW | | Not supported in all devices |
| Reactive power connector 1 | `Diagnostic` | kVar|   :heavy_check_mark: | |
| Reactive power connector 2 | `Diagnostic` | kVar | | Not supported in all devices|
| Solar and battery power | `Diagnostic` | kW |    | Only supported in solar configuration |
| Status connector 1 | `Diagnostic` |   | :heavy_check_mark: | |
| Status connector 2 | `Diagnostic` |   | | Not supported in all devices|
| Total Current | `Diagnostic` | A |  :heavy_check_mark: | |
| Total Power | `Diagnostic` | kW |   :heavy_check_mark: | |
| User connector 1 | `Diagnostic` |  | | Only supported in Rfid configuration|
| User connector 2 | `Diagnostic` |   | | Only supported in viaris COMBIPLUS Rfid|

### Switches

| Friendly name | Category | Supported | Unsupported reason |
| ------------- | -------- | ----- | ------------------ |
| Start connector 1 charging | `config` | :heavy_check_mark: | |
| Start connector 2 charging | `config` | :heavy_check_mark: | |

### Numbers
| Friendly name | Category | Supported | Unsupported reason |
| ------------- | -------- | ----- | ------------------ |
| Current limit connector 1 | `control` | :heavy_check_mark: |Only when device is charging  |
| Current limit connector 2 | `control` | :heavy_check_mark: |Only when device is charging. Supported in viaris COMBIPLUS|













