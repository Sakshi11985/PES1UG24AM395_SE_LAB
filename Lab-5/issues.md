# Lab 5 – Static Analysis Issues: `movie_reviews.py`

Line numbers refer to the **original** file. Ordered by severity (High → Low).

| # | Issue | Tool / Code | Severity | Type | Line(s) | Description | Fix Approach |
|---|-------|-------------|----------|------|---------|-------------|--------------|
| 1 | Weak MD5 hash | Bandit B324 | High | Security | 46 | `hashlib.md5()` is cryptographically broken; Bandit assumes it may be used for security. | Here MD5 only makes a short review id, not a security token, so declared `usedforsecurity=False`. Output (`52e343ca87`) unchanged. |
| 2 | Binding to all interfaces | Bandit B104 | Medium | Security | 4 | `STREAM_HOST = "0.0.0.0"` exposes the service on every network interface. | Default to `127.0.0.1` (localhost); allow override via the `STREAM_HOST` environment variable. |
| 3 | Hard-coded password | Bandit B105 | Low | Security | 6 | `MODERATOR_PASSWORD = "reviews-demo"` stores a secret in source code / Git history. | Read it from the `MODERATOR_PASSWORD` environment variable. |
| 4 | Insecure random generator | Bandit B311 | Low | Security | 41 | `random.choice` uses a predictable PRNG. | Replaced with `secrets.choice` (OS CSPRNG). Removed the now-unused `random` import. |
| 5 | Global statement | Pylint W0603 | Medium | Design | 8, 40 | `pick_featured` mutated a module-level `featured` variable via `global`; hidden shared state. | Removed `global featured`; the function now just returns the chosen title. |
| 6 | Non-snake_case names | Pylint C0103 | Low | Convention | 8, 11, 16, 26, 34, 39, 45, 48, 54 | camelCase names (`addMovie`, `reviewText`, …) violate PEP 8. | Renamed to `add_movie`, `rate_movie`, `review_text`, `average_rating`, `top_movies`, `pick_featured`, `review_id`, `print_all_reviews`, `stream_address`; updated all call sites. |
| 7 | Missing docstrings | Pylint C0114 / C0116 | Low | Convention | 1, 11–58 | No module or function docstrings. | Added a module docstring and a one-line docstring to every function. |
| 8 | Unnecessary `else` after `return` | Pylint R1705 | Low | Refactor | 28–31 | `else:` after a `return` adds nesting for no reason. | Removed `else`, de-indented `return 0.0`. |
| 9 | `range(len())` loop | Pylint C0200 | Low | Refactor | 49–51 | Index-based iteration is error-prone and un-Pythonic. | `for i, title in enumerate(movies, start=1)`. |
| 10 | Code runs on import | (best practice) | Low | Design | 75 | `main()` executed whenever the module was imported. | Wrapped in `if __name__ == "__main__":`. |
| 11 | Missing whitespace around operator | Flake8 E225 | Low | Style | 35 | `ranked=sorted(...)` | `ranked = sorted(...)` |
| 12 | Expected 2 blank lines | Flake8 E302 | Low | Style | 48 | Only 1 blank line before a top-level `def`. | Added a second blank line. |
| 13 | Inline comment spacing | Flake8 E261 | Low | Style | 70 | One space before `# demo id`. | Two spaces before the inline comment. |
| 14 | Missing whitespace after comma | Flake8 E231 | Low | Style | 72 | `print("Genres:",sorted(...))` | Added a space after the comma. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 5.47 / 10 | **10.00 / 10** |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | **0 issues** |
| Flake8 | 4 issues | **0 issues** |

Program output is unchanged except the stream address, which now shows `127.0.0.1:8000` instead of `0.0.0.0:8000` (intended – fix #2). The "Featured today" line was random before and is random after.
