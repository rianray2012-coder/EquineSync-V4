# Master EquineSync Wave 2 RF Dependency Graph

`W2-RF01 -> W2-RF02 -> W2-RF03 -> W2-RF04 -> W2-RF05 -> W2-RF06`

RF02 and RF03 may share RF01 primitives but do not own each other's writes.
RF04 references horse/location identity. RF05 references facility/location and
actor identity. RF06 is evidence and integration, not a new business domain.
