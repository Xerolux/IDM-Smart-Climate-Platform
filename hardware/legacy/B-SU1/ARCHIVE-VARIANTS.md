# B-SU1 recovered archive variants

Two ZIP containers with the same B-SU1 two-variant package were recovered on 2026-08-19.

| Archive | SHA-256 |
|---|---|
| first recovered ZIP | `8d6c917d9ddd81335a80780abcd14b1b2cdd08ecb499c1ed35e2542df5ba9733` |
| second recovered ZIP | `b9fd77e854cb724152d58e706a500aea77ac7e82ad6aef2a7a6a2096b6bb5555` |

The ZIP files are not byte-identical, but the extracted payload was compared file-by-file:

- 84 files in each archive
- identical relative paths
- identical SHA-256 for every extracted file

Therefore the difference is only in the ZIP container/metadata or packing, not in the B-SU1 design payload. The repository keeps one extracted canonical copy and records both source archive hashes for provenance instead of duplicating the same hardware files.
