# 📘 EGM6 Nixie Tube Clock  
## Complete English User Guide (Practical Edition)

---

# 🧭 Table of Contents

- Overview
- WiFi Settings
- Apps
- Daylight Savings Changes
- Remote Control Basics
- Display Modes
- Setting Time
- Setting Date
- Time & Date Formats
- Auto Power Scheduling
- Time/Date Auto Switching
- Digit Transition Effects
- Motion Effects (Minute Animation)
- Cathode Protection (Anti-Poisoning)
- Colon (Middle Dots) Settings
- Nixie Tube Test
- Reset Functions
- Recommended “Balanced” Setup

---

# 🧩 Overview

This is a **WiFi-enabled Nixie tube clock controller** with:

- Remote control configuration  
- WiFi time sync  
- Daily scheduling (on/off)  
- Display effects & animations  
- Tube protection (anti-poisoning)  

---

# WiFi settings

By default, the module will have an SSID of `EGM_TUBE6_XXXXXX` - the password is `12345678` (not documented). The IP address of the module is `192.168.4.1` and there is a basic Web UI and an app (Android and Windows only). I struggled to operate the Android App and did most of the settings using the remote, and used the web UI at http://192.168.4.1 to set the SSID, Password and Timezone (GMT+1 for BST). 

There's no need to turn time sync on or off - this just worked for me once I had set the IP. The Web UI remains accessible, but you have to find the IP address on your selected network.

---

# Apps

The apps (Android APK, Windows .NET) do work (which I didn’t think originally) but **only** when the device is in AP mode and has its default IP. Although you can (on Windows) hand edit the configuration and it appears in the GUI, the communication with the device never seems to work (even though you can see the 3-way handshake in Wireshark). If you want to use the app:
1. Reset the WiFi (see below) to default
2. Connect to the `EGM_TUBE6_XXXXXX` AP
3. Use the app on `192.168.4.1`
4. Set the SSID and timezone through the Web UI in a browser (I couldn’t make this work in the app)

Most functions of the remote are available in the app, but not the flashing “colons”. This has to be done with the remote

Alternatively, the `egm6.py` tool in this repository sends the same commands as the app and works on any network the clock is joined to. See the [README](../README.md).

---

# Daylight Savings Changes

There’s no specific setting for this as on some devices, simply:
1. GMT->BST = change the timezone to UTC+1
2. BST->GMT = change the timezone to UTC

That can be done in the Web UI without a reset to the WiFi. And no need for the app.

---

# 🎮 Remote Control Basics

## Key Buttons

| Button | Function |
|--------|--------|
| 1 | Time display |
| 2 | Date display |
| 6 | Auto on/off schedule |
| 7 | Nixie tube test mode |
| 8 | Anti-poisoning interval |
| 9 | Advanced settings (incl. time/date switching) |
| MODE | Enter setting mode |
| << / >> | Move between fields |
| + / - | Adjust values |
| 0 (short) | Cycle motion effects |
| 0 (long) | Toggle auto-rotation of effects |
| MENU | Cycle digit transition effects |
| Power (long) | Enable/disable scheduled on/off |

---

# 🖥 Display Modes

Switch modes using number keys:

- `1` → Time  
- `2` → Date  
- `6` → Schedule  
- `7` → Nixie Tube Test  
- `8` → Anti-poisoning  
- `9` → Advanced settings

Screens auto revert to default after 10 seconds if no action taken.  

---

# ⏰ Setting Time

## Steps:
1. Press **1** (time display)  
2. Press **MODE**  
3. Use **<< / >>** to select:
   - Hour / Minute / Second  
4. Use **+ / -** to adjust  
5. Exit (wait or press another mode)

---

# 📅 Setting Date

## Steps:
1. Press **2** (date display)  
2. Press **MODE**  
3. Use **<< / >>** to select:
   - Year / Month / Day  
4. Use **+ / -** to adjust  

---

# 🔄 Time & Date Format

## Time Format (12h / 24h)
- In time display → press **Return** (curly arrow)
- Toggles 12h / 24h

## Date Format
- In date display → press **Return** (curly arrow)
- Cycles:
  - YY-MM-DD  
  - MM-DD-YY  
  - DD-MM-YY  

---

# 🔌 Auto Power Scheduling

## What it does
Turns display:
- OFF at a set time  
- ON at a set time  

---

## How to set it

### 1. Enter mode
- Press **6**

### 2. Enter settings
- Press **MODE**

### 3. Set time
- Use **<< / >>** (hour - mid digits/minute - right digits)
- Use **+ / -** to adjust

### 4. Select ON or OFF
Press the **toggle button** (Play/Pause button)

- `0` = OFF time  
- `1` = ON time  

👉 You must set BOTH separately

---

### 5. Enable feature
- Long press **Power**

---

# 🔁 Time/Date Auto Switching

## What it does
Automatically alternates:

Time (duration) → Date (duration) → Time → Date

So a good setting is 25s for time and 5s for date, which gives a total cycle time of 30 seconds so it's clean within the minute.

---

## How to configure

### 1. Enter mode
- Press **9** until you see a 4-digit config display

### 2. Press MODE

### 3. Configure fields

- Use **<< / >>** to move digits
- Use **+ / -** to adjust
- Use **Play/Pause** to toggle on/off

| Position | Meaning |
|----------|--------|
| 1–2 | Time display duration (seconds) |
| 3 | Date duration |
| 6 | Enable (0=off, 1=on) |

---

### Example

30 5 1

- Time = 30s  
- Date = 5s  
- Enabled  

---

# 🎨 Digit Transition Effects

## Change effect
- Press **MENU**

## Options:
- Fade (recommended)  
- Alternate  
- Rolling  
- Instant  

---

# 🎬 Motion Effects (Minute Animation)

## What it does
Plays an animation **once per minute at second = 00**

---

## Controls

### Select effect
- Short press **0**

Cycles:

Effect 1 → Effect 2 → Effect 3 → Effect 4 → OFF

---

### Auto rotation
- Long press **0**

- ON → rotates effects each minute  
- OFF → fixed effect  

---

## Important Rule

👉 If set to **OFF**, no animation will play (even if auto-rotation is ON)

---

## Effects Explained

1. Right → left wipe, then rebuild  
2. Slide out → slide in  
3. Sequential vanish/rebuild  
4. Dual-side scan  

---

# 🛡 Cathode Protection (Anti-Poisoning)

## What it does
Prevents tube damage by cycling all digits periodically

---

## How to set

### 1. Press **8**
### 2. Press **MODE**
### 3. Set interval:
- Hours / Minutes using **<< / >>**
- Adjust with **+ / -**

---

## Behaviour
- Runs at **:30–:31 seconds**
- Lasts ~2 seconds  
- Default is every 20 minutes (at :00, :20 and :40)

---

# ⏰ Nixie Tube Test

## Steps:
1. Press **7** (test mode)  
2. All digits turn to `0`
3. Use **+ / -** to adjust digits to `0` through `9` - all show the same number at the same time 
4. Exit (wait or press another mode)

---

# 🔵 Colon (Middle Dots)

## Change mode
- Long press **MENU**

## Options:
- Off  
- Blinking  
- Breathing  
- Always on  

---

# 🔄 Reset Functions

## Reset basic settings
- Long press **Mute (green button)**

## Reset WiFi
- Long press **9**

---

# 🌟 Recommended “Balanced” Setup

## Visual Behaviour

- Digit transition → **Fade**
- Motion effect → **Effect 1 or 4**
- Auto-rotation → **OFF**

---

## Timing

- Time/date switching → 30 / 5 / ON
- Anti-poisoning → every 60–120 mins

---

## Colon

- Breathing (modern)  
or  
- Blinking (classic)  

---

## Power schedule (optional)

- OFF → 23:30  
- ON → 07:00  

---

# 🧠 Final Mental Model

Your clock behaves like:

- Smooth every second  
- Subtle animation every minute  
- Occasional maintenance  
- Brief date display  
- Sleeps at night  

---

# 👍 Troubleshooting Tip

If something “does nothing”:

👉 It’s usually because:
- A master toggle is OFF  
- Or you’re in the wrong mode  
