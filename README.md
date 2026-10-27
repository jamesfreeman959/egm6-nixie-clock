# egm6-nixie-clock

A small command-line tool for controlling an **EGM6** six-tube nixie clock
(sold under the Jingdian Electronics / Totem Lab name, 景电电子-图腾实验室) over
WiFi, without the vendor's Windows app.

The clock is ESP32-based. It listens for commands on **TCP port 10000** and
never replies, so the only confirmation that a command worked is the display
itself.

The protocol below was worked out by capturing the traffic of the official
Windows configuration app. It is unofficial and incomplete. This project is
not affiliated with or endorsed by the manufacturer.

For using the clock itself (remote control keys, setting modes, resets), see
the [user guide](docs/user-guide.md).

## Requirements

Python 3.8 or later. Standard library only, no dependencies.

## Usage

```sh
./egm6.py --host 192.168.1.50 time-format 24
```

The host defaults to `$EGM6_HOST`, or to `192.168.4.1` (the clock's own
hotspot address) if that isn't set:

```sh
export EGM6_HOST=192.168.1.50
./egm6.py timezone +0          # UTC+00
./egm6.py automatic on         # cycle between time and date
./egm6.py cycle 25 5           # 25 s on time, 5 s on date
./egm6.py --dry-run schedule 23:30 07:00   # print bytes, don't send
```

| Command | Arguments | Group |
|---|---|---|
| `screen` | `time` `date` `schedule` `test` `antitoxin` `automatic` | `02` |
| `time-format` | `12` `24` | `03` |
| `date-format` | `ymd` `mdy` `dmy` | `04` |
| `effect` | `breathe` `alternate` `scan` `general` | `06` |
| `special` | `on` `off` | `07` |
| `auto` | `on` `off` | `08` |
| `effect-mode` | `1`–`4` | `0A` |
| `automatic` | `on` `off` (time/date cycling) | `0B` |
| `timezone` | UTC offset `-11`…`+13` | `0C` |
| `cycle` | time seconds, date seconds | `0D` |
| `antitoxin` | hours, minutes (anti-poisoning interval) | `0F` |
| `test-digit` | `0`–`9` | `14` |
| `switching` | `on` `off` | `18` |
| `schedule` | display off `HH:MM`, on `HH:MM` | `19` |
| `raw` | hex group, hex payload bytes | any |

`on`/`off` also accept `open`/`close`, which is what the vendor app calls them.

## Protocol

Each command is one frame:

```
53 <group> <len> <payload...> 0D 0A
```

- `53` is a fixed start byte (ASCII `S`).
- `<len>` is the payload length plus 2 (it counts the trailing `0D 0A`).
- Values are 0-based. For example, time format is `00` = 12-hour, `01` = 24-hour.
- The clock sends no acknowledgement.

Examples:

| Bytes | Meaning |
|---|---|
| `53 03 03 01 0D 0A` | 24-hour time |
| `53 0C 03 0B 0D 0A` | Time zone index 11 = UTC+00 |
| `53 0D 07 19 05 00 00 00 0D 0A` | Cycle 25 s time, 5 s date |
| `53 19 06 17 1E 07 00 0D 0A` | Display off 23:30, on 07:00 |

### Notes on specific groups

- **`0C` time zone**: index 0 = UTC−11 through 24 = UTC+13. There is no
  daylight saving support, so the offset has to be changed by hand twice a year.
  The clock ignores the length byte for this group.
- **`0D` cycle**: the three trailing payload bytes were always `00` in the
  vendor app's traffic. Their meaning is unknown.
- **`02` screen**: the value is the remote-control key number minus one.

### Unmapped groups

Groups `05`, `09`, `0E`, `10`–`13` and `15`–`17` exist in the sequence but
haven't been identified. Sending value `00` to each produced no visible change.
They probably cover settings the vendor app exposes but that weren't captured,
such as brightness, light sensor, LED mode, alarm and buzzer. Use `raw` to
experiment, but be aware that unknown values can leave the clock in an odd
state. A long press of **Mute** on the remote resets the basic settings.

### WiFi setup

On first boot (or after a WiFi reset) the clock runs a hotspot named
`EGM_TUBE6_XXXXXX` at `192.168.4.1`. It accepts network credentials as a
plain-text line on the same port:

```
AT+AP=<ssid>,<password>\r\n
```

The clock also serves a small settings page on port 80 with a WebSocket at
`ws://<clock>/ws`, which accepts the same binary frames.

## Troubleshooting

- **Nothing happens.** Check the clock is reachable (`nc -z <clock> 10000`).
  The clock's WiFi can become unresponsive; a power cycle usually fixes it.
- **The vendor app connects but does nothing.** In testing, the Windows app
  only sent commands when the clock was at `192.168.4.1`. On a home network
  it opened connections but never sent any data.

## License

MIT. See [LICENSE](LICENSE).
