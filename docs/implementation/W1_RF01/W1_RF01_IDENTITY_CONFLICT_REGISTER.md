# W1-RF01 Identity Conflict Register

| Conflict | Current behavior | Target resolution |
| --- | --- | --- |
| Role vs role status | Capabilities inspect role; review state may be ignored | Granted authority separate from requested/enrollment role |
| JWT role vs user role | User document wins | Keep claim non-authoritative or revision-bind it |
| User barn vs selected membership | Most routes use user barn | Explicit active context with server enforcement |
| Existing-user invite vs legacy role/barn | Adds membership without changing legacy pair | Context-aware access; no silent overwrite |
| Platform role vs barn role | Separate fields | Preserve strict separation |
| User vs owner/rider/guardian person records | Domain duplicates | Stable actor links and manual duplicate resolution |
| Provider role vs provider grant | Mixed checks | Grant required for horse/client scope |
| Suspended account vs retained relationships | Login blocked; history remains | Suspend access, retain lineage and notices |
| Deleted/inactive account vs actor history | Incomplete lifecycle | Tombstone account, retain minimized actor evidence |

No automatic merge or legal-identity conclusion is authorized.

