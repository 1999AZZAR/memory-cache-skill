---
name: memory-cache
description: High-performance temporary storage using Redis. Use to save context, cache expensive API results, or share state between agent sessions. Follows strict key naming conventions.
---

# Memory Cache

## Setup
1.  Copy `.env.example` to `.env`.
2.  Ensure Redis is running locally or provide remote credentials.
3.  Install `redis-tools` (apt) if not available.

## Usage
- **Role**: Memory Manager.
- **Trigger**: "Save this for later", "Cache these results", "What was the last search?".
- **Output**: Confirmation of storage or retrieved values.

## Commands (CLI)
- `scripts/cache_manager.py set <key> <value> [--ttl X]`
- `scripts/cache_manager.py get <key>`
- `scripts/cache_manager.py keys <pattern>`

## Key Naming Convention
**ALWAYS** follow `mema:<category>:<name>` structure.
- `mema:context:*` -> Session context (TTL: 24h).
- `mema:cache:*` -> API/Data cache (TTL: 7d).
- `mema:state:*` -> Persistent app state.

See [Key Standards](references/key-standards.md) for full details.

## Examples
```bash
# Cache a search result for 1 hour
./scripts/cache_manager.py set mema:cache:search:123 "search result json" --ttl 3600

# Retrieve context
./scripts/cache_manager.py get mema:context:summary
```
