# Lab 5 – Reflection

> The handout refers to reflection questions but does not list them; these are the four standard Lab 5 questions.

**1. Which issues were the easiest to fix, and which were the hardest? Why?**

The easiest were the Flake8 style issues (E225, E231, E261, E302) – each is a mechanical whitespace change with no effect on behaviour. Missing docstrings and the `else`-after-`return` were similarly straightforward. The hardest were the Bandit findings, because each needed a judgement about what the code is actually *for*. For the MD5 warning (B324) I had to decide whether to switch algorithms (which would change every review id) or to declare that MD5 is not used for security here; since the id is only a label, `usedforsecurity=False` was the right fix. The renaming to snake_case was also tedious because every call site had to change consistently.

**2. Did the static analysis tools report any false positives? If so, describe one example.**

Yes, arguably two. B311 flags `random.choice` for picking a "featured movie" – that is not a security decision, so a predictable PRNG is harmless. I still switched to `secrets.choice` since it costs nothing, but suppressing it with `# nosec B311` and a comment would also have been defensible. B324 on MD5 is similar: MD5 is broken for security, but generating a short display id is not a security use. B105 is also heuristic – it flags any variable whose *name* looks like a password, though here it really was a hard-coded secret.

**3. How would you integrate static analysis tools into your actual software development workflow?**

- **Locally:** run Flake8 and Pylint in the editor (VS Code extensions) and as **pre-commit hooks**, so style and quality issues are caught before a commit.
- **In CI (e.g. GitHub Actions):** run Pylint with a minimum score (`--fail-under=9.5`), Flake8, and `bandit -r . -ll` on every push / pull request, and block merging if they fail.
- Keep a shared config (`.pylintrc`, `setup.cfg`) so the whole team uses the same rules, and require a written reason for any `# nosec` / `# pylint: disable`.

**4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?**

- **Security:** no secret in source code, the service no longer listens on every interface by default, and the hash / random calls are explicit about their purpose (Bandit: 4 → 0).
- **Readability:** consistent snake_case names, docstrings on every function, `enumerate` instead of index loops (Pylint: 5.47 → 10.00).
- **Robustness:** removing the `global` variable eliminates hidden shared state; the `__main__` guard means the module can be imported and tested without running the demo.
- **Consistency:** PEP 8-clean formatting (Flake8: 4 → 0), so diffs are cleaner and reviews focus on logic rather than spacing.
