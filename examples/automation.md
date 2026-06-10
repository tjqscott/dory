# Project Changelog
<!-- Append-only. One line per entry. No headings or blank lines. -->

Architecture settled — single `run.py` with five sequential phases; `state.json` as sole persistence layer
Scan filters added — head-to-head regex, slug blacklist, volume floor, no settled markets
Crash recovery implemented — marks pending entries as placed if already held on sync
Settlement detection via price thresholds; wins trigger FOK sell, losses marked without sell attempt
Fix: in-progress entries bypassed entry window check due to clamped timestamp; explicit guard added
Fix: double-entry guard missed matches when name parsing hit abbreviations; switched to slug-based key
Stake reduced from 5% to 3% after ruin analysis on shuffled historical outcomes
Fix: phantom cashouts — FOK sell success now validated before booking P&L
