# Roadmap Porting SC/CSPB to Xash (arm64)

## Current factual status
- Boot on arm64 is working on Xash build test.
- CSPB currently uses temporary fallback DLL in launcher to avoid missing CSPB server module.
- Fallback path loads Half-Life server rules, not full Counter-Strike server rules.
- Impact: gameplay can enter map, but CS-specific systems (buy logic and related assets/scripts) are not fully active.

## Root cause of "cannot buy weapon"
- CS buy behavior is a server-gamerules feature, not only UI.
- Current fallback uses HL server path when CSPB arm64 gamedll is missing.
- Because CSPB/CS server module is not loaded, buy command flow is incomplete even if menu appears.

## Target architecture for stable CSPB on arm64
- Engine: xash3d-fwgs arm64-v8a.
- Client module: CSPB-compatible client module on arm64.
- Server module: CSPB/CS server gamedll on arm64 (mandatory for buy/game rules).
- Data layer: CSPB assets/scripts with correct search path and fallback chain.

## Phase plan

### Phase 1: Stabilize launch and data lookup (1-2 days)
- Confirm game directory chain and fallback data search order.
- Verify required CSPB folders are readable at runtime.
- Add startup diagnostics for missing resources (weapon script/sprite/sound/model).
- Deliverable: repeatable boot with resource-missing report file.

### Phase 2: Arm64 server module bring-up (2-4 days)
- Port/build CSPB server gamedll from source for arm64.
- Export expected symbols and naming used by Xash Android loader.
- Package generated .so in expected runtime lookup path.
- Deliverable: server module loads without fallback to HL.

### Phase 3: CS gameplay parity checkpoint (1-2 days)
- Validate buyzone + buytime + team restrictions + economy updates.
- Validate round flow and C4 logic.
- Validate bot interaction with CS rules.
- Deliverable: buying works normally in test maps.

### Phase 4: CSPB feature migration by changelog waves (3-7 days)
- Wave A (v12.6-v13.6): weapon/announcement/radio/scoreboard behavior.
- Wave B (v14.8-v16): mask/items/hud/scope/hitmark/healthbar.
- Wave C (v20-v20.1): melee classes, event 6001 behavior, mapconfig, protections.
- Deliverable: feature matrix with pass/fail per subsystem.

### Phase 5: Asset and script compliance pass (2-3 days)
- Audit weapon_list, scripts_character, sprites, sound, model bindings.
- Normalize path case and extension mismatches.
- Ensure map-specific config execution works.
- Deliverable: zero critical missing-assets in runtime logs.

### Phase 6: Packaging and release hardening (1-2 days)
- Build non-ASAN signed arm64 test APK for install.
- Keep ASAN flavor only for diagnostics.
- Smoke test on emulator + real arm64 device.
- Deliverable: installable signed APK and regression checklist.

## Acceptance gates
- Gate 1: no fallback to HL server DLL for CSPB mode.
- Gate 2: buy works in official and custom maps with expected restrictions.
- Gate 3: no blocking missing-asset errors during full round start.
- Gate 4: CSPB v20.1 key features verified on arm64.

## Immediate next actions
1. Remove dependency on temporary HL fallback for CSPB once arm64 server .so is available.
2. Build and load CSPB arm64 server gamedll first (highest priority).
3. Re-test buy flow before moving to cosmetic/feature migrations.
