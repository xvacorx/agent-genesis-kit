---
name: game-feel-and-juiciness
description: "Formulas, curves, physics, and tactile interaction design for game feel and juiciness. Covers procedural squash & stretch, trauma-based camera shake, hitstop/freeze-frame curves, reactive audio arpeggios, and Android haptic feedback."
allowed-tools: Read, Glob, Grep
risk: unknown
source: chroma-cat-studios
---

# Game Feel & Juiciness — Kinetic Design & Micro-Interactions

> **Philosophy:** Games should feel responsive, organic, and physically satisfying to touch.
> **Core Law:** Every player action must produce multi-sensory feedback: visual deformation, audio resonance, and camera response.

---

## 1. Procedural Squash & Stretch

Deform visual sprites without modifying physics colliders or game logic.

### 1.1 The Elastic Volume Conservation Formula
When squashing along an axis, the perpendicular axis must stretch inversely to maintain perceived physical volume:
$$\text{Volume} \approx S_x \times S_y \implies S_y = \frac{1}{S_x}$$

### 1.2 Implementation Pattern in Unity C#
```csharp
public IEnumerator SquashRoutine(Transform visualSkin, Vector2 direction, float intensity = 0.35f, float duration = 0.18f)
{
    float elapsed = 0f;
    Vector3 baseScale = Vector3.one;

    while (elapsed < duration)
    {
        elapsed += Time.unscaledDeltaTime;
        float t = elapsed / duration;
        
        // Damped sine wave oscillation
        float curve = Mathf.Sin(t * Mathf.PI * 3f) * (1f - t) * intensity;
        
        float squashX = 1f + (direction.x != 0 ? -curve : curve * 0.5f);
        float squashY = 1f + (direction.y != 0 ? -curve : curve * 0.5f);

        visualSkin.localScale = new Vector3(baseScale.x * squashX, baseScale.y * squashY, 1f);
        yield return null;
    }
    visualSkin.localScale = baseScale;
}
```

---

## 2. Hybrid Hit-Stop & Freeze-Frame Curves

Hit-stop gives impacts weight. Instead of an abrupt binary pause (`timeScale = 0`), use a 3-phase hybrid curve:

### 2.1 The 3-Phase Curve
1. **Phase 1: Snappy Deceleration (0.02s - 0.04s):**
   Drop `Time.timeScale` rapidly from `1.0f` to `0.02f`.
2. **Phase 2: Tactile Read Hold (0.04s - 0.08s):**
   Hold at near-zero (`0.02f`) to let the player's brain read spatial positioning, hazard proximity, or trajectory.
3. **Phase 3: Smooth Quadratic Recovery (0.08s - 0.12s):**
   Restore `Time.timeScale` smoothly using an ease-out quadratic formula:
   $$t_{\text{norm}} = \frac{t - t_{\text{hold}}}{t_{\text{recover}}}$$
   $$\text{timeScale} = \text{Lerp}(0.02f, 1.0f, t_{\text{norm}}^2)$$

> **CRITICAL:** Timers, UI animations, and input command queues must use `Time.unscaledDeltaTime` during hit-stop so menus and buffers never freeze.

---

## 3. Trauma-Based Camera Shake

Linear camera shake feels artificial. Trauma-based shake feels visceral and naturally decays.

### 3.1 The Trauma Equation
$$\text{Trauma} \in [0.0, 1.0]$$
$$\text{Shake Amount} = \text{Trauma}^2 \quad \text{(or } \text{Trauma}^3 \text{ for extreme impacts)}$$
$$\text{Offset}_x = \text{MaxOffset}_x \times \text{Shake Amount} \times \text{Perlin}(t \times \text{Frequency}, 0)$$
$$\text{Offset}_y = \text{MaxOffset}_y \times \text{Shake Amount} \times \text{Perlin}(0, t \times \text{Frequency})$$

### 3.2 Rules of Camera Shake
* **Always clamp trauma:** `trauma = Mathf.Clamp01(trauma + addedTrauma)`.
* **Trauma decay:** Linear decay per second: `trauma = Mathf.Max(0f, trauma - decayRate * Time.unscaledDeltaTime)`.
* **Cooldowned Shake:** For consecutive rapid impacts (e.g. wall slides or chain breaking), add a `0.15s` cooldown threshold to avoid visual chaos and motion sickness.

---

## 4. Pentatonic Audio Arpeggios & Dynamic Modulation

### 4.1 Ascending Note Tuning
For sequential pickups (e.g. 3 flies, 3 coins, consecutive combos):
* **Pickup 1:** Root note (Do / 1.0x pitch)
* **Pickup 2:** Major third (Mi / 1.25x pitch)
* **Pickup 3:** Perfect fifth (Sol / 1.50x pitch)
* **Combo Climax:** Octave (Do high / 2.0x pitch) + celebratory sparkling layer.

### 4.2 Dynamic Audio Filters
* When entering a shadow/alternate dimension or sub-world:
  - Transition AudioMixer low-pass filter to `1600 Hz` in `0.2s`.
  - Cut high frequencies to create a submerged, mysterious atmosphere.

---

## 5. Android Haptic Feedback Integration

Provide micro-vibrations for tactile tactile feedback on Android devices:
```csharp
#if UNITY_ANDROID && !UNITY_EDITOR
public static void TriggerLightHaptic()
{
    try
    {
        using (var unityPlayer = new AndroidJavaClass("com.unity3d.player.UnityPlayer"))
        using (var currentActivity = unityPlayer.GetStatic<AndroidJavaObject>("currentActivity"))
        using (var vibrator = currentActivity.Call<AndroidJavaObject>("getSystemService", "vibrator"))
        {
            if (vibrator != null && vibrator.Call<bool>("hasVibrator"))
            {
                // 15ms micro-pulse
                vibrator.Call("vibrate", 15L);
            }
        }
    }
    catch (System.Exception) {}
}
#endif
```
