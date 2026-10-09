# Device validation and optimization evidence

## Working baseline

The Tormentum-specific root-only audio clock correction replaced the previous 12–13 rendered FPS behavior with ~30 FPS in the tested steady scene. GPU 888 MHz and changing swap-interval call order did not improve the clock-driven slowdown. Bounded polling reduced CPU work, not independently FPS.

## Additional opt-in optimizations

Each step was built and exercised on TSPS through Spruce principal flow, with real DRM captures, preserved saves and the previous runtime retained on the SD card.

- RAM-backed baseline: preload **15.924 s**, RSS **752844 KiB**, swap **20688 KiB** at ~51 seconds.
- Empty disk cache: preload **24.262 s**, RSS **534860 KiB**, swap **0**. First-generation cost is a regression in startup time.
- Warm disk cache: preload **15.356 s**, RSS **605340 KiB**, swap **0**. Preload registered 3750 cache hits and no misses at the last pre-end reporting interval. The benefit is primarily memory, not a demonstrated large startup acceleration.
- Warm cache + audio 1024: preload **16.048 s**, RSS **569612 KiB**, swap **0**. SDL confirmed 44100 Hz, stereo, 1024 samples; the owner confirmed clean sound with no crackles/dropouts.
- Final binary rebuilt from this repository plus the game regenerated with the checked-in patch tool: preload **17.113 s**, RSS **629772 KiB**, swap **0** at ~61 seconds. Real game frame confirmed, native runtime alive. Recent render intervals: 29.97, 25.53, 25.87, 25.16, 26.95, 25.05 FPS.

**Comparability limit:** the owner interacted with the game during these tests, so final snapshots and FPS do not represent identical scenes. Do not claim a matched FPS gain, a memory-leak fix or locked 30 FPS. Short memory samples are not peak/long-run bounds. Raw numerical results for earlier steps are in `optimization-metrics.json`.

The cache retains exact pixels, validates SHA-256 payload checksums, repairs corrupted entries on the next registration and falls back to RAM if writing fails. Do not delete cache files while the process is running. Its tests cover cold/warm byte equality, corruption repair, key dimensions and write-failure fallback; all passed in the executed host harness.

## Reproducible artifacts

- ARM64 binary built from checked-in repository sources, SHA-256:
  `67238e33ba664df2804cf30b48b2164d93e9b335484491de24711f6366b64468`
- Installable launcher, SHA-256:
  `02aadbd0950807f1e10c31d9b11abd603929161daea670f400472832f0ed15a3`
- Owner-only regenerated game SWF, tested on desktop and TSPS, SHA-256:
  `66ef15faa42a6b27c7728e035f9c313069ef2b94506f75f865784c5dbdf3c478`
  The SWF itself is NOT included. Different FFDec compilation sequences can produce a different SHA despite equivalent edits; this hash corresponds to the checked-in two-stage patcher and FFDec 26.3.0.

The repository ARM64 build completed successfully and the cache unit test passed. Baseline shader/SDL ABI remains unchanged; no game textures are resized. Native dependencies use the device's SDL2/Mali.

## Outstanding verification

- Full save/reload and progression round-trip on TSPS (write observed, full restoration not yet acceptance-tested).
- Long-run resource release across repeated scene transitions.
- Audio/timeline regression coverage beyond the owner-confirmed current scenes.
- Full fresh-image build without the seeded dependency cache used for the executed repository build. The documented Docker script was exercised, but its successful test image had previously installed build dependencies.

No Android-derived port, full game completion or submission-ready PortMaster approval is claimed.
