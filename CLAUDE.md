# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`timesince` is a Home Assistant (HA) custom integration (HACS-compatible) that exposes a sensor entity tracking elapsed time since a user-specified date. There is no build system — Python files are loaded directly by Home Assistant at runtime.

## Architecture

- **Entry point**: `custom_components/timesince/__init__.py` — sets up and tears down the config entry
- **Sensor**: `custom_components/timesince/sensor.py` — `TimeSinceSensor` entity; state is computed in the `state` property (no async polling)
- **Config flow**: `custom_components/timesince/config_flow.py` — uses `voluptuous` for schema validation (bundled with HA; not a separate dependency)
- **Constants**: `custom_components/timesince/const.py`
- **Translations**: `custom_components/timesince/translations/en.json` (English only; no `strings.json` source-of-truth file exists)

## Naming Conventions

- Sensor name: `"{mode}.{reason_slug}"` (e.g., `since.started_gym`)
- Unique ID: `"timesince_{mode}.{reason_slug}"`

## Known Gotchas

- **Date math is approximate**: 1 year = 365 days, 1 month = 30 days — not calendar-accurate. This is an intentional design simplification, not a bug to fix without discussion.
- **Deprecated API**: `__init__.py` uses `async_forward_entry_setup` (singular). HA 2024+ prefers `async_forward_entry_setups` (plural, takes a list). The singular form generates deprecation warnings on recent HA versions.
- **`hacs.json` domain mismatch**: `hacs.json` lists `"domains": ["sincethen"]` but the actual HA domain is `"timesince"`. Fix before any HACS submission.
- **`hacs.json` name**: The `"name"` field reads `"since then gh versiion"` (typo) — a placeholder that was never cleaned up.
- **No `strings.json`**: HA integrations typically have `strings.json` as the source of truth alongside `translations/en.json`. Only the translation file exists here.
- **No options flow**: Users cannot edit a sensor after creation — they must delete and re-add it.

## Development Workflow

- **No build step** — drop `custom_components/timesince/` into a live HA instance's `config/custom_components/` directory, or use HACS.
- **Testing** requires a running Home Assistant instance (minimum version `2023.0.0`).
- **No automated tests or CI** exist in this repo. Verify changes manually via the HA UI.
- **No external Python dependencies** — `voluptuous` is bundled with HA.

## HA Integration Patterns

- Use `async def` for all HA lifecycle callbacks.
- Config flow schema version (`VERSION`) and integration release version (`manifest.json` → `"version"`) are separate concerns.
- When updating the config entry setup, prefer `async_forward_entry_setups` (plural) with a list of platforms.
