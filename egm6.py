#!/usr/bin/env python3
"""Control an EGM6 nixie tube clock (Jingdian / Totem Lab) over TCP port 10000.

Frame format, decoded from the Windows app's traffic:

    53 <group> <len> <payload...> 0D 0A

where <len> = len(payload) + 2 (it counts the trailing 0D 0A). The clock
never replies, so the only confirmation is the display itself.

Examples:
    egm6.py timezone +0          # UTC+00 (GMT)
    egm6.py time-format 24
    egm6.py automatic on         # time/date auto-switching on
    egm6.py cycle 25 5           # 25 s time, 5 s date
    egm6.py test-digit 8
    egm6.py --host 192.168.1.50 date-format dmy
    egm6.py --dry-run schedule 23:30 07:00
"""
import argparse
import os
import socket
import sys

DEFAULT_HOST = os.environ.get("EGM6_HOST", "192.168.4.1")
PORT = 10000

SCREENS = {"time": 0, "date": 1, "schedule": 5, "test": 6, "antitoxin": 7, "automatic": 8}
EFFECTS = {"breathe": 0, "alternate": 1, "scan": 2, "general": 3}
DATE_FORMATS = {"ymd": 0, "mdy": 1, "dmy": 2}
ON_OFF = {"off": 0, "close": 0, "on": 1, "open": 1}


def frame(group, *payload):
    """Build one command frame."""
    for b in payload:
        if not 0 <= b <= 255:
            raise ValueError(f"byte out of range: {b}")
    return bytes([0x53, group, len(payload) + 2, *payload, 0x0D, 0x0A])


def hhmm(text):
    """Parse 'HH:MM' into (hour, minute)."""
    h, m = (int(x) for x in text.split(":"))
    if not (0 <= h <= 23 and 0 <= m <= 59):
        raise argparse.ArgumentTypeError(f"bad time: {text}")
    return h, m


def timezone(text):
    """Parse a UTC offset like +0, -5 or +13 into the clock's zone index."""
    offset = int(text)
    if not -11 <= offset <= 13:
        raise argparse.ArgumentTypeError("UTC offset must be between -11 and +13")
    return offset + 11


def build(args):
    """Turn parsed arguments into the frame to send."""
    c = args.command
    if c == "screen":
        return frame(0x02, SCREENS[args.name])
    if c == "time-format":
        return frame(0x03, 0 if args.hours == "12" else 1)
    if c == "date-format":
        return frame(0x04, DATE_FORMATS[args.format])
    if c == "effect":
        return frame(0x06, EFFECTS[args.name])
    if c == "special":
        return frame(0x07, ON_OFF[args.state])
    if c == "auto":
        return frame(0x08, ON_OFF[args.state])
    if c == "effect-mode":
        return frame(0x0A, args.mode - 1)
    if c == "automatic":
        return frame(0x0B, ON_OFF[args.state])
    if c == "timezone":
        return frame(0x0C, args.offset)
    if c == "cycle":
        # Trailing three bytes were always 00 in the app's traffic; meaning unknown.
        return frame(0x0D, args.time_seconds, args.date_seconds, 0, 0, 0)
    if c == "antitoxin":
        return frame(0x0F, args.hours, args.minutes)
    if c == "test-digit":
        return frame(0x14, args.digit)
    if c == "switching":
        return frame(0x18, ON_OFF[args.state])
    if c == "schedule":
        (off_h, off_m), (on_h, on_m) = args.off, args.on
        return frame(0x19, off_h, off_m, on_h, on_m)
    if c == "raw":
        return frame(int(args.group, 16), *(int(b, 16) for b in args.payload))
    raise SystemExit(f"unknown command {c}")


def main():
    p = argparse.ArgumentParser(description="Control an EGM6 nixie clock.")
    p.add_argument("--host", default=DEFAULT_HOST, help=f"clock IP (default {DEFAULT_HOST}, or $EGM6_HOST)")
    p.add_argument("--dry-run", action="store_true", help="print the bytes without sending")
    sub = p.add_subparsers(dest="command", required=True)

    sub.add_parser("screen", help="switch the displayed screen").add_argument("name", choices=SCREENS)
    sub.add_parser("time-format", help="12 or 24 hour").add_argument("hours", choices=["12", "24"])
    sub.add_parser("date-format", help="date order").add_argument("format", choices=DATE_FORMATS)
    sub.add_parser("effect", help="digit transition effect").add_argument("name", choices=EFFECTS)
    sub.add_parser("special", help="'special' (motion effects) on/off").add_argument("state", choices=ON_OFF)
    sub.add_parser("auto", help="'auto' on/off").add_argument("state", choices=ON_OFF)
    sub.add_parser("effect-mode", help="motion effect 1-4").add_argument("mode", type=int, choices=range(1, 5))
    sub.add_parser("automatic", help="time/date auto-switching on/off").add_argument("state", choices=ON_OFF)
    sub.add_parser("timezone", help="UTC offset, e.g. +0 or -5").add_argument("offset", type=timezone)
    s = sub.add_parser("cycle", help="time/date auto-switching durations in seconds")
    s.add_argument("time_seconds", type=int)
    s.add_argument("date_seconds", type=int)
    s = sub.add_parser("antitoxin", help="anti-poisoning interval")
    s.add_argument("hours", type=int)
    s.add_argument("minutes", type=int)
    sub.add_parser("test-digit", help="show one digit on every tube").add_argument("digit", type=int, choices=range(10))
    sub.add_parser("switching", help="'switching' on/off").add_argument("state", choices=ON_OFF)
    s = sub.add_parser("schedule", help="display off/on times, e.g. 23:30 07:00")
    s.add_argument("off", type=hhmm)
    s.add_argument("on", type=hhmm)
    s = sub.add_parser("raw", help="send an arbitrary frame (hex), e.g. raw 03 01")
    s.add_argument("group")
    s.add_argument("payload", nargs="+")

    args = p.parse_args()
    data = build(args)
    if args.dry_run:
        print(data.hex(" "))
        return
    try:
        with socket.create_connection((args.host, PORT), timeout=5) as s:
            s.sendall(data)
    except OSError as e:
        sys.exit(f"could not reach clock at {args.host}:{PORT}: {e}")
    print(f"sent to {args.host}: {data.hex(' ')}")


if __name__ == "__main__":
    main()
