---
name: verify
description: Validate the timesince integration for HA compatibility and HACS readiness before pushing. Checks deprecated APIs, metadata consistency, and translation files.
disable-model-invocation: false
---

Run through this checklist for the `timesince` Home Assistant integration and report findings:

## 1. Deprecated API Check

Scan `custom_components/timesince/__init__.py` for `async_forward_entry_setup` (singular). If found, note that it should be replaced with `async_forward_entry_setups` (plural, takes a list of platforms). Example fix:
```python
# Old (deprecated):
await hass.config_entries.async_forward_entry_setup(entry, "sensor")
# New:
await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
```
Do the same for `async_unload_platforms` if applicable.

## 2. HACS Metadata Consistency

Read `hacs.json` and `custom_components/timesince/manifest.json`. Check:
- `hacs.json` `"domains"` matches the `"domain"` field in `manifest.json`
- `hacs.json` `"name"` is a clean, human-readable name (not a dev placeholder)
- `manifest.json` `"version"` follows semver (e.g., `1.0.0`)

## 3. Translation File Check

Read `custom_components/timesince/translations/en.json`. Verify:
- All keys referenced in `config_flow.py` (via `errors`, `step` schemas) are present in the translation file
- No orphaned keys in the translation file that are no longer used

## 4. Manifest Sanity

Read `custom_components/timesince/manifest.json`. Verify:
- `"iot_class"` is set (e.g., `"local_push"` or `"calculated"`)
- `"requirements"` is accurate (should be `[]` since all deps are bundled with HA)
- `"homeassistant"` minimum version is set

## 5. Config Flow Version

Check that `config_flow.py` `VERSION` is consistent with any migration logic in `__init__.py`. If the VERSION was bumped, confirm a `async_migrate_entry` function exists.

## Report

Summarize findings as:
- **PASS** — no issues found
- **WARN** — non-blocking issue worth noting
- **FAIL** — must fix before HACS submission or HA reload

List each check with its status and a one-line explanation.
