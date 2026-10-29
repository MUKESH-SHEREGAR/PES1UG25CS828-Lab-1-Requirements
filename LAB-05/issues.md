# Static-analysis issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Hard-coded ERP API key | Security / Bandit B105 | 12 | A live-looking credential was stored in source control. | Read ERP_API_KEY from the environment and fail clearly when it is missing. |
| TLS certificate verification disabled | Security / Bandit B501 | 60 | verify=False allowed an untrusted HTTPS connection. | Use Requests' default certificate verification. |
| Missing request timeout | Reliability / Bandit B113 | 60 | The ERP call could hang indefinitely. | Add a 10-second timeout and raise HTTP errors. |
| Shell command execution | Security / Bandit B602/B604/B609 | 64, 73 | Backup and reminder jobs used shell execution and wildcard expansion. | Use tarfile for backups and represent reminder arguments without invoking a shell. |
| Legacy TLS protocol | Security / Bandit B503 | 66 | ssl.PROTOCOL_TLSv1 selected an obsolete protocol. | Remove the unused legacy helper. |
| Mutable default argument | Bug / Pylint | 18 | register={} shared state across calls. | Default to None and create a new dictionary per call. |
| Incorrect eligibility boundary | Logic bug | 26 | Exactly 75% was rejected despite the stated 75% rule. | Change the comparison from > to >=. |
| CSV formula injection | Security | 86 | Names beginning with =, +, -, or @ could be interpreted as spreadsheet formulas. | Prefix potentially executable cell values with an apostrophe. |
| Unused imports and formatting violations | Style / Flake8 | 1-7 and throughout | Unused imports, missing blank lines, and long lines reduced maintainability. | Remove unused imports and format the module consistently. |


