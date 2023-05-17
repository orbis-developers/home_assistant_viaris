# home_assistant_viaris

Home Assistant integration for monitoring Viaris EV chargers model UNI and COMBIPLUS with mqtt protocol.

[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub stars](https://img.shields.io/github/stars/HGC72/homeassistant_assistant_viaris)
![GitHub forks](https://img.shields.io/github/forks/HGC72/homeassistant_assistant_viaris)
![GitHub watchers](https://img.shields.io/github/watchers/HGC72/homeassistant_assistant_viaris)

## Features

This custom integration provides you information about your charger configuration and the states and measures necessary in order to monitor the charging process. Measures such as active/reactive power/energy, connectors states, power configuration and available analyzers are among others. 

## List of entities view

This screenshot shows different entities you can choose to make your panel.

![imagen](https://github.com/HGC72/home_assistant_viaris/assets/66405397/5503dc6f-eab6-48a4-bba1-f91a79641f5b)

## Panel example view

![imagen](https://github.com/HGC72/home_assistant_viaris/assets/66405397/1dae3325-d01c-411d-baef-d84fcc1614ed)

## Installation

Use HACS to install this custom component. Under HACS, choose Integrations and add the viaris custom repository.

## Configuration

In order to add the viaris EV charger integration, first of all, MQTT integration must be configurated with your broker credentials. The system can discover automatically all of the devices that are connected, after switch them on and restart Home Assistant.  The discovery process is only done at the beginning when neither of the devices are configured. There is another way to add the integration using the web UI, entering your charger serial number.

#### Discovering devices:

![imagen](https://github.com/HGC72/home_assistant_viaris/assets/66405397/45061de9-a953-477f-8cd4-ebea55c8d2a9)

After that you configure each device.

#### Entering serial number:

![imagen](https://github.com/HGC72/home_assistant_viaris/assets/66405397/465c169d-b4e3-43ec-8754-68f0a5c63567)

Installed devices

![imagen](https://github.com/HGC72/home_assistant_viaris/assets/66405397/21c0c3e8-1ca0-4618-9fc0-051e6ea899e5)


## Entities

Once your device has been configured you will see the integration entities.

![imagen](https://github.com/HGC72/home_assistant_viaris/assets/66405397/a453e0b5-7948-4942-bfbb-6d2ad0601608)

### Sensors

| Friendly name | Category | Units | Supported | Unsupported reason |
| ------------- | -------- | ----- | --------- | ------------------ |
| Contax D0613  | `config` |       | :heavy_check_mark: |  | 
| Ethernet | `config` |  | :heavy_check_mark: | |  
| Firmware application version | `config` |   | :heavy_check_mark: | |
| Firmware cortex version | `config` |   | :heavy_check_mark: | |
| Firmware application version | `config` |   | :heavy_check_mark: |  |
| Hardware power version | `config` |   | :heavy_check_mark: | |
| Hardware version | `config` |   | :heavy_check_mark: |  |
| Keep alive | `config` |  | :heavy_check_mark: |  |
| Limit power | `config` | kW  | :heavy_check_mark: | |
| Mac | `config` |   | :heavy_check_mark: | |
| Max power | `config` | kW  | :heavy_check_mark: | |
| Modbus | `config` |   | :heavy_check_mark: | |
| Model | `config` |   | :heavy_check_mark: | |
| Mqtt clien Id | `config` |   | :heavy_check_mark: | |
| Mqtt pin Interval | `config` |  | :heavy_check_mark: | |
| Mqtt port | `config` |   | :heavy_check_mark: | |
| Mqtt QoS | `config` |   | :heavy_check_mark: | |
| Mqtt clien Id | `config` |   | :heavy_check_mark: | |
| Mqtt URL | `config` |   | :heavy_check_mark: | |
| Mqtt user | `config` |   | :heavy_check_mark: | |
| Ocpp | `config` |   | :heavy_check_mark: | |
| Rfid | `config` |   | :heavy_check_mark: | |
| Schuko present | `config` |   | :heavy_check_mark: | |
| Selector power| `config` |   | :heavy_check_mark: | |
| Serial | `config` |   | :heavy_check_mark: | |
| Solar | `config` |   | :heavy_check_mark: | |
| Spl | `config` |   | :heavy_check_mark: | |
| TMC100 | `config` |   | :heavy_check_mark: | |
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





















