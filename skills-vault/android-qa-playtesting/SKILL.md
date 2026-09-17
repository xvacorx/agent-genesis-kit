---
name: android-qa-playtesting
description: "Systematic QA, playtesting, and debugging workflow for Android games. Covers ADB commands, logcat crash dumps, memory leak profiling, aspect ratio validation (4:3 to 21:9), safe area testing, and AAB verification."
allowed-tools: Read, Glob, Grep, Bash
risk: unknown
source: chroma-cat-studios
---

# Android QA & Playtesting — Testing Matrix & ADB Command Suite

> **Philosophy:** Never ship a build without verifying crash logs, memory footprints, and extreme aspect ratio rendering on physical hardware.
> **Standard:** Google Play Console Pre-Launch Report (PLR) zero-crash requirement.

---

## 1. ADB Diagnostic Command Suite

Ensure your test Android phone is connected via USB with Developer Mode & USB Debugging enabled.

### 1.1 Device Health & Status
```bash
# Verify connected devices and authorization
adb devices -l

# Check device model, Android OS version, and SDK level
adb shell getprop ro.product.model
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
```

### 1.2 Real-time Unity & Crash Filtering
```bash
# Stream Unity logs and Android Activity Manager only (clean output)
adb logcat -s Unity:V ActivityManager:I AndroidRuntime:E CRASH:E

# Filter logs specifically for Toading Home package
adb logcat | grep -i "ToadingHome"

# Clear logcat buffer before starting a test run
adb logcat -c
```

### 1.3 Memory Leak & Performance Profiling
```bash
# Inspect RAM allocation breakdown (Heap, Native, Graphics, Dalvik)
adb shell dumpsys meminfo com.ChromaCatStudios.ToadingHome

# Check battery temperature and drain
adb shell dumpsys battery

# Check CPU usage of the game thread
adb shell top -m 5 -s cpu | grep -i "ToadingHome"
```

---

## 2. Multi-Aspect Ratio Testing Matrix

Modern Android devices span drastically different viewport ratios. The game must adapt seamlessly without stretched sprites or hidden gameplay elements:

| Ratio | Representative Hardware | Vulnerability / Check Area |
| :--- | :--- | :--- |
| **4:3 / 3:2** | iPad / Android Foldables (Unfolded) | Horizontal cutoff; UI buttons touching screen edges. |
| **16:9** | Standard TVs, PC Landscape, Older Phones | Baseline reference (Letterbox / Pillarbox). |
| **19.5:9** | Samsung Galaxy S23/S24, Pixel 8/9 | Camera punch-hole / notch clipping HUD icons or Pause button. |
| **21:9** | Sony Xperia / Ultra-wide phones | Extreme vertical space; camera confiner bounds leaking void. |

### 2.1 Safe Area Conformance
* All interactive buttons (Pause, Settings, Restart, Language Toggle) must remain strictly within `Screen.safeArea`.
* Never hardcode vertical offsets in pixels (`-100px`); always use normalized anchors or `Safe Area` Canvas Fitter components.

---

## 3. App Bundle (AAB) Pre-Release Verification

Before uploading a release build to Google Play Console:

### 3.1 Inspect AAB Metadata
```bash
# Extract AndroidManifest from .aab using bundletool
bundletool dump manifest --bundle=ToadingHome_v0.1.7_b9.aab

# Generate universal test APK from bundle
bundletool build-apks --bundle=ToadingHome_v0.1.7_b9.aab --output=test.apks --mode=universal
bundletool install-apks --apks=test.apks
```

### 3.2 Verification Checklist
- [ ] `AndroidTargetSdkVersion: 36` (Complies with Google Play policy).
- [ ] `AndroidBundleVersionCode` incremented correctly (e.g. Build `9`).
- [ ] Signed with release keystore (`TH.keystore`).
- [ ] Development Build & Autoconnect Profiler turned **OFF**.
- [ ] Debug symbols (`.symbols.zip`) generated for crash de-obfuscation in Play Console.
