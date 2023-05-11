# home_assistant_viaris

Home Assistant integration for monitoring Viaris EV chargers.

![GitHub stars](https://img.shields.io/github/stars/HGC72/homeassistant_assistant_viaris)
![GitHub forks](https://img.shields.io/github/forks/HGC72/homeassistant_assistant_viaris)
![GitHub watchers](https://img.shields.io/github/watchers/HGC72/homeassistant_assistant_viaris)

## Sample view

![imagen](https://github.com/HGC72/home_assistant_viaris/assets/66405397/0529bd2b-17ca-4747-b1a0-c648247c8641)

## Installation

Use HACS to install this custom component.

## Configuration

In order to add the viaris EV charger integration, first of all, MQTT integration must be configurated with your broker credentials. The system can discover automatically all of the devices that are connected, after switch them on and restart Home Assistant.  There is another way to add the integration using the web UI, entering your charger serial number.


## Entities

### Sensors

| Friendly name | Category | Enabled per default | Supported | Unsupported reason |
| ------------- | -------- | ------------------- | --------- | ------------------ |
| Contax D0613  | `config` |  | :heavy_check_mark: |  | 
| Ethernet | `config` |  | :heavy_check_mark: | |  
| Firmware application version | `config` |  | :heavy_check_mark: | |
| Firmware cortex version | `config` |  | :heavy_check_mark: | |
| Firmware application version | `config` |  | :heavy_check_mark: |  |
| Hardware power version | `config` |  | :heavy_check_mark: | |
| Hardware version | `config` |  | :heavy_check_mark: |  |
| Keep alive | `config` |  | :heavy_check_mark: |  |
| Limit power | `config` |  | :heavy_check_mark: | |
| Mac | `config` |  | :heavy_check_mark: | |
| Max power | `config` |  | :heavy_check_mark: | |
| Modbus | `config` |  | :heavy_check_mark: | |
| Model | `config` |  | :heavy_check_mark: | |
| Mqtt clien Id | `config` |  | :heavy_check_mark: | |
| Mqtt pin Interval | `config` |  | :heavy_check_mark: | |
| Mqtt port | `config` |  | :heavy_check_mark: | |
| Mqtt OoS | `config` |  | :heavy_check_mark: | |
| Mqtt clien Id | `config` |  | :heavy_check_mark: | |
| Mqtt URL | `config` |  | :heavy_check_mark: | |
| Mqtt user | `config` |  | :heavy_check_mark: | |
| Ocpp | `config` |  | :heavy_check_mark: | |
| Rfid | `config` |  | :heavy_check_mark: | |
| Schuko present | `config` |  | :heavy_check_mark: | |
| Selector power| `config` |  | :heavy_check_mark: | |
| Serial | `config` |  | :heavy_check_mark: | |
| Solar | `config` |  | :heavy_check_mark: | |
| Spl | `config` |  | :heavy_check_mark: | |
| TMC100 | `config` |  | :heavy_check_mark: | |
| Active energy connector 1 | `Diagnostic` |  | :heavy_check_mark: | |
| Active energy connector 2 | `Diagnostic` |  | :heavy_check_mark: | |
| Reactive energy connector 1 | `Diagnostic` |  | :heavy_check_mark: | |
| Reactive energy connector 2 | `Diagnostic` |  | :heavy_check_mark: | |
| Evse power | `Diagnostic` |  | :heavy_check_mark: | |
| Home power | `Diagnostic` |  | :heavy_check_mark: | |
| Overload rel | `Diagnostic` |  | :heavy_check_mark: | |
| Active power connector 1 | `Diagnostic` |  | :heavy_check_mark: | |
| Active power connector 2 | `Diagnostic` |  | :heavy_check_mark: | |
| Reactive power connector 1 | `Diagnostic` |  | :heavy_check_mark: | |
| Reactive power connector 2 | `Diagnostic` |  | :heavy_check_mark: | |
| Solar and battery power | `Diagnostic` |  | :heavy_check_mark: | |
| Status connector 1 | `Diagnostic` |  | :heavy_check_mark: | |
| Status connector 2 | `Diagnostic` |  | :heavy_check_mark: | |
| Total Current | `Diagnostic` |  | :heavy_check_mark: | |
| Total Power | `Diagnostic` |  | :heavy_check_mark: | |
| User connector 1 | `Diagnostic` |  | :heavy_check_mark: | |
| User connector 2 | `Diagnostic` |  | :heavy_check_mark: | |





















