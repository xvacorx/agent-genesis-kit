---
name: unity-6-mobile-master
description: "Elite Unity 6 LTS (6000.x) mobile game development skill. Covers URP 2D, zero-GC architecture, frame pacing/Swappy, Android 16 (API 36) compliance, memory-safe pooling, audio streaming, additive level loading, and IL2CPP build optimization."
allowed-tools: Read, Glob, Grep, Bash
risk: unknown
source: chroma-cat-studios
---

# Unity 6 Mobile Master — High Performance & Production Standards

> **Philosophy:** Zero GC in hot loops. 60 FPS rock-solid frame pacing. Native battery efficiency.
> **Engine Baseline:** Unity 6 LTS (6000.x) with Universal Render Pipeline (URP 2D).
> **Target Platforms:** Android (Target API 34-36 / Android 14-16) & iOS.

---

## 1. Zero-Allocation & Garbage Collection Elimination

### 1.1 Strictly Prohibited APIs in Hot Loops
* **Never use `FindObjectOfType`:** Deprecated in Unity 6. Always use `FindFirstObjectByType<T>()` or `FindAnyObjectByType<T>()` with `FindObjectsInactive.Include` when necessary.
* **No LINQ in `Update`, `FixedUpdate`, or Coroutine Loops:** `.Where()`, `.Select()`, `.ToList()`, `.ToArray()` generate hidden heap allocations (`IEnumerable<T>` boxing and iterators). Use standard `for (int i = 0; i < count; i++)`.
* **No `Instantiate` / `Destroy` during Gameplay:** All dynamic objects (projectiles, particles, hazards, floating text, coins, flies) **MUST** use an Object Pool (`Pool<T>` / `ScriptableObjectPool`).
* **Avoid String Concatenation in UI:** Use `StringBuilder`, custom formatters, or cached static string buffers. For numbers, use pre-allocated buffers or formatted `TMP_Text.SetText("{0:00}:{1:00}", min, sec)`.

### 1.2 Static & Cached Allocations Pattern
```csharp
// BAD: Allocates 24-32 bytes per frame on heap
void Update() {
    var hits = Physics2D.RaycastAll(transform.position, Vector2.down, 5f);
}

// GOOD: Zero allocation with NonAlloc buffer
private readonly RaycastHit2D[] _hitBuffer = new RaycastHit2D[8];
void Update() {
    int hitCount = Physics2D.RaycastNonAlloc(transform.position, Vector2.down, _hitBuffer, 5f);
    for (int i = 0; i < hitCount; i++) {
        // Process _hitBuffer[i]
    }
}
```

---

## 2. Mobile Frame Pacing & Battery Optimization

### 2.1 Display Pacing & Swappy Integration
* Android Display Pacing (Swappy) is mandatory for smooth frame delivery on high-refresh screens (90Hz, 120Hz).
* Ensure `androidUseSwappy: 1` in `ProjectSettings.asset`.
* Target Framerate:
  ```csharp
  Application.targetFrameRate = 60; // Standardize 60 FPS
  QualitySettings.vSyncCount = 0;   // Let Swappy handle sync
  Screen.sleepTimeout = SleepTimeout.NeverSleep; // Prevent dimming during gameplay
  ```

### 2.2 Cold-Start Hitch Elimination
1. **Never use synchronous `Shader.WarmupAllShaders()` at startup:** Compiling thousands of variants on mobile freezes the thread for 1.5s-4.0s.
2. **Use Additive Master Scene Architecture (`LevelCore.unity`):**
   - Core scene stays loaded via `DontDestroyOnLoad`.
   - Subscenes (`Level X.unity`) load and unload additively with `LoadSceneMode.Additive`.
   - Thread priority during loading: `Application.backgroundLoadingPriority = ThreadPriority.High`.
   - Force hidden garbage collection: Execute `System.GC.Collect()` while screen is faded to solid black (`SceneTransitionManager`), wait 2 frames, then fade in.

---

## 3. Audio & Texture Memory Architecture

### 3.1 Audio Import Settings
* **Long Music Tracks (> 15s):**
  - Load Type: `Streaming` (`preloadAudioData = 0`).
  - Compression: `Vorbis` (Quality 60%-70%).
  - Keeps RAM footprint under 2MB for music.
* **Lightweight SFX (< 5s):**
  - Load Type: `Decompress On Load` (`preloadAudioData = 1`).
  - Compression: `ADPCM` or `PCM`.
  - Zero latency on playback for jumps, impacts, and death sounds.

### 3.2 Texture Compression
* Android 100% standard: **ASTC** (Adaptive Scalable Texture Compression).
  - Normal sprites & UI: `ASTC 4x4` or `ASTC 6x6`.
  - Large backgrounds & tilemaps: `ASTC 6x6` or `ASTC 8x8`.
  - Always check "Generate Mip Maps" = False for 2D sprites and UI to save 33% VRAM.

---

## 4. Android 15 & 16 (API 35-36) Compliance Checklist

1. **16KB Page Alignment:**
   - Android 15+ devices support 16KB memory page sizes. Ensure NDK / IL2CPP builds use Unity 6000.0.18f1+ or verify libil2cpp is compiled with `-z max-page-size=16384`.
2. **Predictive Back Navigation:**
   - Handle Android back gestures gracefully in UI modals with `KeyCode.Escape` or `UnityEngine.InputSystem.Keyboard.current.escapeKey`.
3. **Target SDK:**
   - Maintain `AndroidTargetSdkVersion: 36` in `PlayerSettings`.
   - Use App Bundle format (`.aab`) with Play Asset Delivery when exceeding standard APK limits.
