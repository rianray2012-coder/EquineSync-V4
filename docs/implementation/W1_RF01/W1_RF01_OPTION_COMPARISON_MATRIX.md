# W1-RF01 Option Comparison Matrix

| Dimension | A: Harden | B: Converge | C: External IdP | D: Staged hybrid |
| --- | --- | --- | --- | --- |
| Immediate security value | High | Medium | Medium | High |
| Constitutional alignment | High | High if additive | Conditional | Highest |
| Schema impact | None/minimal | Additive | Linking fields | Staged |
| Migration impact | None | Material | Material | Deferred by stage |
| Lockout risk | Low | Medium/high | High | Controlled |
| Provider dependence | None | None | High | Deferred |
| Test burden | Focused | High | High | Sequenced |
| Rollback | Strong | Requires compatibility | Requires fallback | Strongest overall |
| Timeline | Short | Medium/long | Long | Incremental |
| Current authorization | Not yet authorized | Not authorized | Not authorized | Planning recommendation only |

Option A must still receive explicit runtime authority. Option D describes sequencing, not blanket authorization.

