# Reflection

## 1. How did static analysis help?

It found both obvious style problems and security-sensitive behavior that a normal demo run would not reveal. Bandit highlighted the hard-coded API key, disabled TLS verification, missing timeout, and shell execution. Pylint and Flake8 exposed maintainability issues such as the mutable default argument, unused imports, naming/style problems, and missing documentation.

## 2. Which issue was most serious?

The hard-coded ERP API key was the most serious because anyone with repository access could copy and misuse it. Disabled TLS verification was also high risk because it could expose the credential and attendance data to a man-in-the-middle attack.

## 3. What did the tools reveal that execution did not?

The demo appeared to work, but it did not call the ERP integration and therefore did not exercise its insecure request. Static analysis examined dormant code paths as well as the executed path, which is why it identified risks that the demo output did not show.

## 4. How would these improvements be maintained?

The tools should run in CI on every pull request, with Bandit and Flake8 treated as blocking checks and a minimum Pylint score enforced. Secrets should be supplied through a managed secret store or environment configuration, and dependencies should be pinned and updated regularly.


