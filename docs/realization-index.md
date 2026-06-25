# Realization index (derived — Tier-0 spike)

> **GENERATED FILE — do not edit by hand.** Regenerate with `python3 tools/realization-index.py`; `--check` fails on drift.
>
> A cross-design map of *which accepted reference design realizes each AC, where in its code, and at which archived commit* — the asset-dual of [field notes](field-notes/), derived from each design's bundled `Architecture.md` attestation table + `design.toml` SWHID pin. Spike for [`design-notes/2026-06-harvesting-reusable-code.md`](design-notes/2026-06-harvesting-reusable-code.md). Realization pointers are best-effort over prose; the design's own Architecture.md is authoritative. Fetch the pinned `swhid_dir` (not `main`) to study a realization at the archived commit.

## Designs indexed

| Design | Status | Archival | Pin | swhid_dir | Flavor |
|---|---|---|---|---|---|
| [fellows_local_db](https://github.com/richbodo/fellows_local_db) | active | archived | `15be80d` | `swh:1:dir:f139d27207eb6d814eaf031d374f9cfb795aba17` | distribution:web-bundle-with-magic-link, storage:opfs-sqlite-wasm, ingestion:single-source-static-mirror, workspace:vanilla-js-spa, comms:mailto-only, mcp-exposure:shared+private+comms |
| [prm](https://github.com/richbodo/prm) | active | archived | `2d6889d` | `swh:1:dir:e90b07e1b4c0c1d1023ffc82618ce6341104a79f` | distribution:never-distributed-single-user, storage:native-sqlite-via-filesystem, ingestion:multi-source-merge-with-dedup, workspace:vanilla-js-spa, comms:none, mcp-exposure:shared-only |

## Coverage summary

- **27** distinct ACs indexed across **2** designs; **27** have at least one non-N/A realization.
- **14** ACs are realized by **more than one** design (the prime harvest candidates — two realizations to compare): AC-1, AC-4, AC-6, AC-7, AC-9, AC-10, AC-11, AC-15, AC-17, AC-22, AC-23, AC-MCP-A, AC-PRM-A, AC-PRM-D.
- **Realization-pointer coverage** — the standing goal is **100%** for every accepted design (each non-N/A row's realization should resolve to a `path:symbol` code pointer; see the design note). A number below 100% marks attestation prose that names a symbol without its file:
    - fellows_local_db: **25/25** non-N/A rows carry a code pointer (**100%**).
    - prm: **14/16** non-N/A rows carry a code pointer (**88%**).

## Realization matrix

One row per (commitment-or-realization, design) — `AC-*` architectural commitments and the `RZ-*` realizations a pick brings. `Realization` and `Verification` are the code/test pointers harvested from the attestation; `Pin` is the design's archived commit (study the realization there, via `swhid_dir` above).

| AC / RZ | Title | Design | Status | Realization | Verification | Pin |
|---|---|---|---|---|---|---|
| AC-1 | two-store ownership split | fellows_local_db | conformant | `app/relationships.py:open_db()` | `tests/test_relationships.py::test_attach_fellows_readonly_allows_select`, `tests/test_relationships.py::test_attach_fellows_readonly_denies_write`, `tests/test_database.py` | `15be80d` |
| AC-1 | two-store ownership split | prm | conformant | `core/shared_db.py`, `core/relationships_db.py` | `tests/unit/test_relationships_store.py::test_import_seeds_private_and_keeps_shared_intact`, `tests/db/test_shared_db.py` | `2d6889d` |
| AC-2 | no SaaS surface | fellows_local_db | conformant | `deploy/server.py` | `tests/test_deploy_auth_round_trip.py::test_directory_api_is_403_without_session`, `test_deploy_sqlite_api.py`, `test_deploy_mcpb_routes.py` | `15be80d` |
| AC-3 | single OPFS owner | fellows_local_db | conformant | `app/static/vendor/sqlite-worker.js` | `tests/e2e/test_worker_rpc.py`, `test_worker_cold_start.py`, `test_local_first_boot.py` | `15be80d` |
| AC-4 | versioned cross-boundary handshake | fellows_local_db | conformant | `vendor/sqlite-worker.js` | `tests/e2e/test_version_handshake.py::test_version_skew_refuses_mutations_but_allows_reads`, `tests/e2e/test_worker_rpc.py` | `15be80d` |
| AC-4 | versioned cross-boundary handshake | prm | conformant | `daemon/server.py:route` | `tests/db/test_shared_db.py::test_incompatible_schema_version_is_rejected`, `tests/db/test_relationships_db_version.py::test_private_mismatch_refuses_seed`, `tests/db/test_relationships_db_version.py::test_private_mismatch_refuses_apply`, `tests/unit/test_daemon_diag.py::test_schema_mismatch_refuses_write_reads_continue` | `2d6889d` |
| AC-5 | stale session never locks users out of cache | fellows_local_db | conformant | `app/static/app.js:bootDirectoryAsApp` | `tests/e2e/test_offline_only_mode.py::test_401_with_cached_data_shows_directory_from_cache`, `tests/e2e/test_offline_only_mode.py::test_onboarded_multitab_stale_session_shows_cached_directory_not_gate`, `tests/e2e/test_offline_only_mode.py::test_ownership_conflict_empty_cache_shows_panel_not_gate`, `test_search_offline_fallback.py` (+1) | `15be80d` |
| AC-6 | always-reachable diagnostic escape | fellows_local_db | conformant | `app/static/app.js:startBrowserUx`, `app/static/app.js:clearEverything` | `tests/e2e/test_email_gate.py`, `tests/e2e/test_reset_everything.py`, `tests/e2e/test_clear_app_cache.py` | `15be80d` |
| AC-6 | always-reachable diagnostic escape | prm | conformant | `core/diag.py:lock_state`, `cli/prm_import.py:cmd_doctor` | `tests/unit/test_doctor.py::test_unlock_clears_stale_lock`, `tests/unit/test_doctor.py::test_unlock_refuses_when_held_live` | `2d6889d` |
| AC-7 | self-service field-debug substrate | fellows_local_db | conformant | `deploy/client_error_sanitizer.py` | `tests/e2e/test_diagnostics_panel.py`, `test_boot_watchdog.py`, `test_boot_error_panel.py`, `test_bug_report.py` (+1) | `15be80d` |
| AC-7 | self-service field-debug substrate | prm | conformant | `core/diag.py:capture_error` | `tests/unit/test_diag.py::test_state_dump_is_sanitized_metadata`, `tests/unit/test_diag.py::test_error_log_redacts_and_tails`, `tests/unit/test_daemon_diag.py::test_diag_route_sanitized`, `tests/unit/test_doctor.py::test_doctor_dump_runs` | `2d6889d` |
| AC-8 | anti-enumeration + abuse-bounded analytics | fellows_local_db | conformant | `deploy/server.py`, `deploy/magic_link_auth.py:check_rate_limit`, `deploy/client_error_sanitizer.py` | `tests/test_magic_link_auth.py`, `test_deploy_auth_round_trip.py`, `test_deploy_client_errors.py`, `test_client_error_sanitizer.py` | `15be80d` |
| AC-9 | auto-backup of private data | fellows_local_db | conformant | `vendor/sqlite-worker.js:maybeBackupRelationshipsDb()` | `tests/e2e/test_user_folder_storage.py::test_snapshot_lands_in_folder_when_folder_mode_active`, `tests/e2e/test_user_folder_storage.py::test_opfs_to_folder_backup_migration_on_folder_boot`, `tests/e2e/test_settings.py`, `code inspection` (+1) | `15be80d` |
| AC-9 | auto-backup of private data | prm | conformant | `core/snapshots.py` | `tests/unit/test_apply.py::test_snapshot_and_restore`, `tests/unit/test_apply.py::test_apply_merge_then_undo` | `2d6889d` |
| AC-10 | opt-in non-destructive re-imports | fellows_local_db | conformant | `app/static/vendor/sqlite-worker.js:previewFellowsDbSwap()` | `tests/e2e/test_directory_data_update_flow.py::test_apply_with_group_impact_shows_dialog_and_can_cancel`, `tests/e2e/test_directory_data_update_flow.py::test_apply_with_group_impact_confirm_completes_swap`, `test_orphan_soft_scan.py`, `test_versioned_fellows_db.py` | `15be80d` |
| AC-10 | opt-in non-destructive re-imports | prm | conformant | `cli/ingest.py:reimport` | `tests/unit/test_reimport.py::test_reimport_added_updated_stale`, `tests/unit/test_reimport.py::test_reimport_apply_keeps_stale_and_snapshots`, `tests/unit/test_reimport.py::test_reimport_flags_merges_with_stale` | `2d6889d` |
| AC-11 | concurrent-access detection | fellows_local_db | conformant | `app/static/vendor/sqlite-worker.js:isOwnershipConflictError()` | `tests/e2e/test_user_folder_storage.py::TestPhase2WriteLock::test_lock_held_during_write_surfaces_failure_then_recovers`, `test_worker_spawn_failure.py` | `15be80d` |
| AC-11 | concurrent-access detection | prm | conformant | `core/lock.py:file_lock` | `tests/unit/test_lock.py::test_second_holder_refused_with_message` | `2d6889d` |
| AC-12 | capability detection inside worker | fellows_local_db | conformant | `app/static/vendor/sqlite-worker.js:handlers.init` | `tests/e2e/test_unsupported_browser.py::test_no_sah_falls_back_to_api_idb_provider`, `test_worker_cold_start.py` | `15be80d` |
| AC-13 | COOP/COEP required | fellows_local_db | conformant | `app/server.py:Handler.end_headers`, `deploy/server.py` | `tests/test_api.py::TestSecurityHeaders::test_coop_coep_present`, `tests/test_api.py::TestSecurityHeaders::test_strict_csp_present`, `tests/test_api.py::TestSecurityHeaders::test_other_hardening_headers_present` | `15be80d` |
| AC-14 | SW never owns SQLite | fellows_local_db | conformant | `app/static/sw.js` | `tests/e2e/test_sw_post_caching.py`, `test_image_cache_no_bust.py` | `15be80d` |
| AC-15 | build label tied to source revision | fellows_local_db | conformant | `build/build_pwa.py:compute_build_label()`, `vendor/sqlite-worker.js`, `app/server.py` | `tests/test_build_pwa.py`, `tests/e2e/test_update_check.py`, `test_bug_report.py`, `test_boot_beacon.py` | `15be80d` |
| AC-15 | build label tied to source revision | prm | conformant | `core/build_label.py` | `tests/unit/test_build_label.py::test_running_label_is_git_date_sha`, `tests/unit/test_build_label.py::test_archived_source_uses_stamp_file`, `tests/unit/test_build_label.py::test_no_git_no_stamp_is_non_empty_fallback` | `2d6889d` |
| AC-16 | user-driven transport selection | fellows_local_db | partial | `app/static/app.js:renderGroupDetailPage`, `app/static/app.js:renderDetail` | `tests/e2e/test_groups_export.py`, `tests/test_comms.py` | `15be80d` |
| AC-16 | user-driven transport selection | prm | not-applicable | — | — | `2d6889d` |
| AC-17 | mirrored data is sourced | fellows_local_db | conformant | `build/restore_from_knack_scrapefile.py` | `tests/test_database.py`, `build/diff_fellows_db.py`, `./data_provenance.md`, `human review` | `15be80d` |
| AC-17 | mirrored data is sourced | prm | conformant | `core/schema/shared.sql`, `cli/ingest.py` | `tests/db/test_shared_db.py::test_load_writes_records_provenance_and_fts` | `2d6889d` |
| AC-18 | transports cannot read message contents | fellows_local_db | conformant | `mcp_servers/comms.py:stage_email()` | `tests/test_comms.py`, `tests/test_private_data_ops.py`, `human-review`, `architectural` | `15be80d` |
| AC-18 | transports cannot read message contents | prm | not-applicable | — | — | `2d6889d` |
| AC-19 | user-visible payload before send | fellows_local_db | conformant | `app/static/app.js:renderGroupDetailPage` | `tests/e2e/test_groups_export.py`, `tests/e2e/test_groups_compose.py` | `15be80d` |
| AC-19 | user-visible payload before send | prm | not-applicable | — | — | `2d6889d` |
| AC-22 | honest capability assessment | fellows_local_db | conformant | `app/static/vendor/sqlite-worker.js:handlers.init`, `app/static/app.js:renderLocalDataUnavailablePanel` | `tests/e2e/test_unsupported_browser.py::test_no_sah_falls_back_to_api_idb_provider`, `tests/e2e/test_worker_cold_start.py` | `15be80d` |
| AC-22 | honest capability assessment | prm | conformant | — | `tests/unit/test_doctor.py::test_doctor_dump_runs`, `tests/unit/test_diag.py::test_state_dump_is_sanitized_metadata`, `code inspection` | `2d6889d` |
| AC-23 | source available for verification | fellows_local_db | conformant | `build/build_pwa.py:compute_build_label()` | `tests/test_build_pwa.py`, `tests/e2e/test_update_check.py`, `by construction` | `15be80d` |
| AC-23 | source available for verification | prm | conformant | — | `by construction` | `2d6889d` |
| AC-MCP-A | cloud AI clients require consent for Private DB | fellows_local_db | partial | `mcp_servers/private_data_ops.py` | `tests/e2e/test_pna_exception_mode.py`, `tests/test_private_data_ops.py` | `15be80d` |
| AC-MCP-A | cloud AI clients require consent for Private DB | prm | conformant | `core/relationships_db.py:shareable_field_values`, `core/disclosure.py`, `core/apply.py:set_disclosure_mode`, `mcp_servers/tools.py` | `tests/unit/test_mcp_data_floor.py::test_sealed_never_crosses_and_shareable_needs_consent`, `tests/unit/test_mcp_data_floor.py::test_sealed_absent_from_mcp_projection_in_every_mode`, `tests/unit/test_daemon_disclosure.py::test_default_state_then_consent_cycle`, `tests/e2e/test_disclosure_flow.py::test_consent_gate_governs_the_mcp_floor_end_to_end` (+1) | `2d6889d` |
| AC-MCP-B | MCP Communications stages; workspace launches | fellows_local_db | conformant | `mcp_servers/comms.py:stage_email()` | `tests/test_comms.py::test_stage_email_basic_to`, `tests/test_comms.py::test_stage_email_bcc_group_send` | `15be80d` |
| AC-MCP-B | MCP Communications stages; workspace launches | prm | not-applicable | — | — | `2d6889d` |
| AC-PRM-A | LLM calls over user data are transports | fellows_local_db | partial | `app/static/app.js:recordMcpbConsent()` | `tests/e2e/test_pna_exception_mode.py`, `test_mcpb_settings.py` | `15be80d` |
| AC-PRM-A | LLM calls over user data are transports | prm | partial | `mcp_servers/consent.py:CLOUD_LLM_NOTICE`, `core/disclosure.py` | `tests/unit/test_mcp_consent.py`, `code inspection` | `2d6889d` |
| AC-PRM-B | multi-source dedup contract | fellows_local_db | not-applicable | _n/a: Applies to ingestion:multi-source-merge-with-dedup; fellows is single-source…_ | — | `15be80d` |
| AC-PRM-B | multi-source dedup contract | prm | conformant | `cli/identity.py`, `core/relationships_db.py:identity_map`, `core/candidates.py`, `core/projection.py:preview_merge` | `tests/unit/test_candidates.py::test_detect_clusters_and_tiers`, `tests/unit/test_candidates.py::test_transitive_overmerge_guard`, `tests/unit/test_relationships_store.py::test_preview_merge_marks_conflicts`, `tests/unit/test_reimport.py::test_reimport_preserves_merges` (+1) | `2d6889d` |
| AC-PRM-C | single-instance file-lock | fellows_local_db | not-applicable | _n/a: Applies to storage:native-sqlite-via-filesystem; fellows uses opfs-sqlite-wasm._ | — | `15be80d` |
| AC-PRM-C | single-instance file-lock | prm | conformant | `core/lock.py:file_lock` | `tests/unit/test_lock.py::test_second_holder_refused_with_message`, `tests/unit/test_lock.py::test_release_allows_reacquire` | `2d6889d` |
| AC-PRM-D | re-ingestion is user-initiated | fellows_local_db | conformant | `app/static/app.js:handleUpdateDirectoryDataClick` | `tests/e2e/test_directory_data_update_flow.py`, `test_versioned_fellows_db.py::test_install_only_does_not_refetch_on_sha_mismatch` | `15be80d` |
| AC-PRM-D | re-ingestion is user-initiated | prm | conformant | `cli/prm_import.py:cmd_import`, `cli/prm_import.py:cmd_reimport` | `tests/unit/test_reimport.py`, `by construction` | `2d6889d` |

