# Attempt 03/04 Evidence Materialization Record

`FINAL_VERIFIED_EVIDENCE_MATERIALIZATION_RECORD`

## Identity and authority

- Authorized cycle: `ATTEMPT_03_04_EVIDENCE_MATERIALIZATION_AND_DISPOSITION_PREPARATION`
- Repository: `/Users/rianray/Documents/Codex/2026-07-22/files-mentioned-by-the-user-equinesync/work/EquineSync-V4-canonical`
- Remote contacted: `https://github.com/rianray2012-coder/EquineSync-V4.git`
- Branch: `codex/founder-review-phase1-pilot-a-mode-b-attempt-04-founder-disposition-v1`
- HEAD before and after retrieval: `05eaa53be3e5e6aa00814eaeee49f145b3bc6c49`
- Attempt 03: `34c427c0196d3f8273ac3ea88ad05a2bbe5a2c29`
- Attempt 04: `ebd6a1ed18a2231b450e7bbfb58035198bfcb93c`

## Prior disclosed fetch

The earlier automatic promisor fetch at approximately `2026-07-22T11:26:39Z` remains separately classified as `DISCLOSED_NONDESTRUCTIVE_PROMISOR_FETCH_NO_REPOSITORY_STATE_CHANGE`. Its objects were not deleted, pruned, repacked, or remediated.

## Newly authorized retrieval

- Start: `2026-07-22T12:12:49.930Z`
- End verification timestamp: `2026-07-22T12:13:00Z`
- Retrieval scope: 87 unique missing object IDs reachable only within the preserved Attempt 03 and Attempt 04 package paths.
- Automatic lazy fetches during the authorized retrieval/verification: `0`; retrieval used one explicit batched fetch and subsequent verification set `GIT_NO_LAZY_FETCH=1`.

Object-discovery command:

```sh
GIT_NO_LAZY_FETCH=1 git rev-list --objects --missing=print refs/remotes/origin/codex/founder-review-phase1-pilot-a-mode-b-attempt-03-v1 refs/remotes/origin/codex/founder-review-phase1-pilot-a-mode-b-attempt-04-v1 -- governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-03 governance/founder_orchestrated_review/phase1/V1.0.0/pilot_a/mode_b_configuration_identified_execution/attempt-04
```

Exact retrieval command:

```sh
git -c fetch.writeCommitGraph=false fetch --no-tags --no-write-fetch-head --filter=blob:none origin 035c2c51d87792e9af5aa358e5e56c53dc76c5ea 0628319e88845fca7ff30ec2bc5a8e6920801ce9 0743b881ce48e9f2c9671846cf213ebd81e3dce0 081b4f8d809932ae8ade0147755d6d95f5fc64ca 08757b7fe166ad8d439548b4ddbd71dc27cb0465 0f8031a1b4fb6aa6be0bc8e0603eb84b1f795e36 113d2a38fb0a67882f90c170d3f2583e17424b3b 15a3ca95e92f26d0669703774711dd88118de256 1b084367d65e4ef7e71940c176b0873b3c618e40 1fa47cd727c5564558a43a435ea227017e068418 21bdf5a38077d038a7590a04a4dd4d1daa2faedb 231a5fa94d84272e74af1e77145c563f12d1e7e0 239b0839aeb9444999c97f4080d0fb5dcefe8344 278f4611830e669198edef8254b944ffd755608f 27bd3b36cb2e5a0ca10dfb0b752ad73b666f4c58 2bd7d91a5f287487453eeeff8f0395e40c7bd411 2e503a1fc5d9fcd7337ea30b6a9cb5ef861e91fe 3764993821d2ea5656805a500a598653fc58fd96 3db19b1d1b7038a709f7146708dcdb93b0f680a4 3fbe5f5f32ce0f246b37393e2a7b02fd4d08270a 40cfe112ab743e2de9c3cb88544648b2c6533958 43564668f6fabad18737267f6dd248069afad47b 46bcdd49bf41a24c1c31dd23bc3f0e92a981103a 4958497558ee358c4338714ab10a9eafec84aaee 4ac34aff6571314d1bc9d8adde692035c8fa1b83 53399bfad539fa3b85cb32b0f86fc0bdbe5a70dc 5d41a32d8ba2ac7bfe905d87b406ea8f234de519 5f7fbc9a5795f8dc8f507cdda6c5d361d438ac73 609491d21c0c69e7d8c4753b4ca6284bef242d25 653e507327950aa1c144f3228aa1179f6f481356 65481631719f6b90c607240d031a02eb764ef42d 66b4729bcf0d7e1194b1d20da8c2b98e2dde0d2f 6d24f058ba61ae566f747dadd39e981957e6e2b5 6e29c36e3db291ae6d3974d317648533518a71a6 70fdedf8c224247b18480f1a7c2bbc69aeaf2b27 7345f72863daf02e08da8b38b3844fcb5e698534 73f444757d43f08b020f002f2e595c43bce68bba 776d40f2c784d0c4777a8ca237d721e6c1b98255 77fa40d81a33e59b9139f97daa045893eba65c9c 7ad1215086aa9aebd1e209968868b9f910884c1e 840db089023ba1e58232320d381ba9726fa12586 850c5448f0025e33136ce1574482c25fe4c6ad98 8913b7b23b5c04ccf6e5dc6df23036088809ab65 8993f0dfac4483be7eeadb83248a6b13522c70f9 8b0d539e698c7ee5eb0cc0d3dd46afad362eb84c 8c41ad9f5869c392510b9c290351a0f758a842da 8e402219e4008a13ae50fd5a73b56e178fb16655 8f17e2caf3ee3c3034fccfbb3210b37043549173 94cd5759410c19239005c7ff3287e865f2432ac8 9a88adcabebd638731e96ab388484fc26e51837c a274b793b3e2717d385cfea43ab34f11bee7ca27 a3d3368701807c6482ab1d8e40018e1ddcb2c910 a8741d617189e36474387dadf4291ad122b3d885 af51a3160282343322e8aab166ba07bb66a936e0 b1b05688d52b963599c27261e5ae24cdaa817a58 b512ed09a11974587d5717a33363c6406e61d3d5 baf7e80014488bcfda9d3983216c6d30b1529efe bcbf82ee8407686cd2d5858ca5d9cd0c66377b16 be402fab14cc39041bf2b2fed3d7e278bff241a7 c0b8bf50f08553df4f172c69d1028ee799cd851e c32a49fb3f6a3f7a566e27ba0fe47daeb0ce35d7 c8d011f70c07ac8c08c3ab089c83f11974def8c8 c8df1fd1169b9b08636412bfe627f3c54e6d647e c95b8feb14c8c2bbd112c92920623c3e26548b58 cc80cd1d6a5669f9154d3082b1881829893ed64d cc9e23bb193cb73f05b76616d7ca6d2d6d2abf1f ce59664a4815091949973b06ac3adc68746dd1d2 d02532a925ac52bffbb2f98afd1271093009931a db104187113c5d15b1fbffdf52c3a15d3005d755 db5b230a0a67b79686a9b5fc11fbccff1ab08006 db62c998b3981ade4608d3bfa4d5b9727a600b22 dc1367381ec315bb6178fff5e46ba6d42cc7cb35 df0b66188224081f44f96188380d357f375337c7 e2067a358c95a8c9141cd2263f9116ee6e4f37cd e25ac4e03c23fabf492327727c1a800391c87670 e72915036db056acd5d300c907da77d6c0bd89c0 e72c3bd90a3644ac3d3b57a9ade7e715a056d46b ea1cc172ce982cf1a067f8d01d5e3690189dd435 eb0e316983b8cc73c248d12a8f794e95b6abfee9 ebf4b79d44888a6a9632baf5604b90fb1c971a22 f0dbf817733cd2482e993429d776e67ab7c96a1b f484a1a2da0a34ce48190c48ff07a36cb248ee38 f961662d77b0dc324bbc2e6fcc765ac673cb4809 f99ee71bc2955a0669031baa5fda667e31015beb fa6b58443f47d3062932d85492f5271ec774dafe fda00036d523606a637a51cb4ec69d05221546c2 fea72e3b7b58125fe401176feb17c312b8b9b0af
```

## Object-store and disk observations

| Measure | Before | After |
| --- | ---: | ---: |
| Available disk | `10 GiB` | `10 GiB` |
| Repository size | `511 MB` | `511 MB` |
| `.git` size | `197 MB` | `197 MB` |
| Pack count | `23` | `24` |
| Pack bytes | `204,589,822` | `204,789,002` |
| Missing unique Attempt objects | `87` | `0` |

New files created by the authorized fetch:

- `.git/objects/pack/pack-1a84cd97c392ca5577ffb5e055bc186ddd4705c5.pack` — 199,180 bytes
- `.git/objects/pack/pack-1a84cd97c392ca5577ffb5e055bc186ddd4705c5.idx` — 3,508 bytes
- `.git/objects/pack/pack-1a84cd97c392ca5577ffb5e055bc186ddd4705c5.promisor` — 0 bytes
- `.git/objects/pack/pack-1a84cd97c392ca5577ffb5e055bc186ddd4705c5.rev` — 400 bytes

No new loose object was observed. The repository remains a partial clone with `remote.origin.promisor=true` and `remote.origin.partialclonefilter=blob:none`.

## Repository-state result

- Branch changed: `NO`
- Tag changed: `NO`
- HEAD changed: `NO`
- Index changed: `NO`
- Historical worktree checked out: `NO`
- Canonical worktree changed by retrieval: `NO`
- Objects still unavailable within Attempt 03/04 package scope: `0`

The finalized Founder disposition artifacts in this package are separate authorized documentary additions and are not historical evidence changes.
