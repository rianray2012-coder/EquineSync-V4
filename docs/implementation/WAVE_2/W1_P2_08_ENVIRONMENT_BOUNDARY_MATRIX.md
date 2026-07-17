# W1-P2-08 Environment Boundary Matrix

| Environment | Credentials | Network | Result |
| --- | --- | --- | --- |
| ordinary local/test/CI | empty by default | loopback only | allowed |
| inherited nonempty credential | rejected | no provider call | blocked |
| production-like credential in nonproduction | always rejected | no provider call | blocked |
| authorized sandbox test | explicit opt-in plus verified test mode | named allowlist only | separately authorized |
| production | outside this package | outside this package | no authority |
