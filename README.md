# Tormentum — Dark Sorrow: TSPS / SpruceOS PortMaster port

Development port using a native ARM64 Ruffle frontend and GLES2. Tested on TrimUI Smart Pro S (SpruceOS). **You must own the GOG PC game, version 1.4.1. No commercial game files, APK/OBB, saves or generated texture cache are distributed.**

## Repository layout

- `port/`: installable launcher, ARM64 runtime, controller/ALSA configuration and empty game-data template.
- `source/runtime/`: modified ruffle4consoles frontend and GLES renderer, including disk-backed lossless texture cache.
- `source/core/`: Ruffle core source snapshot corresponding to Cargo.lock, with the opt-in nested-stream clock correction. Its sibling workspace dependencies are obtained from the pinned upstream Git revision by the build script; this directory is not a standalone Cargo workspace.
- `tools/`: ARM64 build and owner-side game compatibility patcher.
- `tests/cache/`: executable cold/warm/corruption/fallback cache regression test.
- `docs/`: measured results, limitations and checksums.

## Install

1. Copy **the contents of `port/`** to `/mnt/SDCARD/Roms/PORTS/`. Do not replace or delete an existing save/cache folder when upgrading.
2. Extract your GOG installer with `innoextract`. Copy the contents of its extracted `app/` directory to `/mnt/SDCARD/Roms/PORTS/tormentum/gamedata/`.
3. Keep an untouched copy of the original `Tormentum.swf`. On a Linux PC with Java, Python 3 and [FFDec 26.3.0](https://github.com/jindrapetrik/jpexs-decompiler/releases/tag/version26.3.0), run:

```sh
python3 tools/patch_game.py /path/to/original/Tormentum.swf /path/to/patched/Tormentum.swf \
  --ffdec /path/to/ffdec.jar --work /path/to/owner-only-patch-work
```

The patcher checks exact decompiled source hashes before editing. It replaces AIR filesystem saves with flushed SharedObject storage, removes NativeApplication dependencies and centers the full 4:3 frame. Copy its **patched** output over the installed `gamedata/Tormentum.swf`. Keep `gamedata/config.ron` from this repository: it selects that filename, not `movie.swf`.

4. Mark `Tormentum.sh` and `tormentum/ruffle-native-multifile.aarch64.lazy` executable and launch **Tormentum from the Spruce menu**. Do not start the game alongside MainUI over SSH. Allow the first texture-cache generation to finish.

## Controls / settings

- Left stick or D-pad: cursor; A: left click; B: right click; L: precision movement.
- Start + Select: exit. The SDL frontend supplies mouse input; gptokeyb2 is used for the exit helper.
- Save: `tormentum/gamedata/storage/localhost/tormentum_portmaster.sol`. The file is written; full save/reload and full-game progression still need regression coverage.
- `TOR_BITMAP_CACHE_DIR` in the launcher enables disk backing. Cache may be deleted **only while the game is stopped**; it is regenerated, contains game-derived pixels and must not be redistributed. Remove that environment setting to use the RAM-only fallback.
- Audio defaults to **1024 samples at 44100 Hz**, tested and confirmed clean by the device owner. Change `TOR_AUDIO_SAMPLES=2048` for a conservative fallback. Buffer duration is not a measured end-to-end speaker latency.
- `TOR_STREAM_SYNC_ROOT_ONLY=1` fixes the tested slowdown by preventing nested streamed sounds from retiming the entire stage. Sound playback itself remains enabled. This is game-specific, not a general upstream policy.
- No texture downscaling, CPU/GPU overclock or forced 60 FPS is applied.

## Build from the checked-in sources

Docker on x86-64 Linux:

```sh
docker run --rm --security-opt label=disable -v "$PWD":/work rust:1.90-bullseye \
  bash /work/tools/build-aarch64.sh
```

The script installs the ARM64 cross-toolchain/SDL2 headers, fetches Cargo.lock-pinned dependencies, overlays the checked-in core audio source into the pinned Cargo checkout, cleans that release package when needed, runs host cache tests and builds/strips the ARM64 runtime into `port/tormentum/`. System SDL2 and Mali on the device are used; the cross-build SDL2 library is not bundled. Bullseye archive sources are explicit because regular Bullseye mirrors are no longer reliable for this build.

Frontend upstream: Hexadecinull/ruffle4consoles, commit `d88628ff545cdacdc7c3e0f5bf1d13fce370693f`. Original packaging reference: SilverPsychoo/Ruffle-Handheld. Core dependency revision is pinned in `source/runtime/Cargo.lock`. Upstream licenses/notices are preserved in the source directories; game compatibility edit recipes do not grant rights to the commercial game.

## Evidence and remaining limits

See `docs/VALIDATION.md` and `docs/optimization-metrics.json`. Native graphics, centering, mouse interaction and sound are demonstrated on TSPS. Root-only audio clock correction raised the tested steady scene from ~12–13 to ~30 FPS. Asset/scene transitions still dip; **locked 30 FPS throughout the game is not claimed**. The disk cache primarily reduces resident memory, not a proven large startup speedup. Android resources were assessed separately but are not the input to this port.
