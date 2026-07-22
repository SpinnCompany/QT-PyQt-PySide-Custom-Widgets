# Contributing to Custom Widgets

> **⚠️ DRAFT.** The **CLA requirement** in §1 activates only once the CLA is
> finalized and the CLA bot is wired up (see `lgpl-relicense-plan.md`). The dev
> setup and conventions below are accurate now. When the CLA is live, this file is
> promoted to `/CONTRIBUTING.md`.

Thank you for helping improve Custom Widgets! This guide covers how to contribute
and the conventions we follow.

## 1. Contributor License Agreement (required)

Custom Widgets uses a sustainable **open-core** model: a free, open-source library
(**LGPLv3**) funded by a separately-licensed commercial add-on. To keep this
possible, all contributors must accept our **Contributor License Agreement (CLA)**
before their contribution can be merged.

- You **keep the copyright** to your work.
- You grant the maintainer the right to use your contribution in **both** the free
  LGPL library and the commercial product.
- The CLA bot will prompt you to accept on your first pull request; acceptance is
  recorded automatically.

See the CLA text: `CLA.md`. Contributions cannot be merged until the CLA is
accepted.

> Contributions are made to the **free core** (`QT-PyQt-PySide-Custom-Widgets`).
> The commercial `custom-widgets-pro` package is developed separately and does not
> accept outside contributions.

## 2. Development setup

Custom Widgets targets **PySide6** and **PyQt6** via [`qtpy`](https://github.com/spyder-ide/qtpy).
Use a **single virtual environment** (do not create per-binding venvs).

```bash
# clone your fork, then:
python -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
pip install -e .                     # editable install of the library
pip install -e ".[mcp]"              # optional: MCP server / Designer bridge extras
pip install pytest                   # test runner
```

PySide6 is the default/primary binding. To exercise the PyQt6 path, set `QT_API`.

## 3. Running tests

```bash
python -m pytest tests/ -v                    # default (PySide6)
QT_API=pyqt6 python -m pytest tests/ -v       # verify the PyQt6 binding
```

Some tests require Qt Designer or a display and will **skip** automatically when
those aren't available — that's expected in headless environments. Please make
sure the suite passes on at least PySide6 before opening a PR.

## 4. Project conventions

Follow the existing patterns — new code should read like the surrounding code.

- **Bindings:** use `qtpy` imports (`from qtpy.QtWidgets import ...`), never import
  `PySide6`/`PyQt6` directly. Code must work on **both** PySide6 and PyQt6.
- **Designer-facing properties:** expose widget properties as **typed properties**,
  and use **`QEnum`** for enumerated choices so they appear correctly in Qt
  Designer's property editor.
- **Styling:** put styles in the theme's **`defaultStyle.scss`** (compiled to QSS).
  **Never** hardcode styles in `.ui` XML.
- **Clean breaks over shims:** this project favors clean API changes with migration
  notes (in the docs repo) rather than backward-compat shims. Discuss breaking
  changes in an issue first.
- **Docs:** user-facing documentation lives in the separate Docusaurus repo; update
  it when you change public behavior.

## 5. Pull request process

1. **Open an issue first** for anything non-trivial (features, breaking changes) so
   we can agree on the approach.
2. Branch from `main`; keep PRs focused and reasonably small.
3. Ensure `python -m pytest tests/ -v` passes (PySide6 at minimum).
4. Write a clear description of **what** changed and **why**. Reference the issue.
5. Accept the **CLA** when the bot prompts (§1).
6. Optional but appreciated: sign your commits with DCO (`git commit -s`).

## 6. Reporting bugs & requesting features

- **Bugs:** open an issue with your OS, Python version, Qt binding (PySide6/PyQt6),
  a minimal reproduction, and the traceback.
- **Features:** describe the use case and, if relevant, how it fits the modernization
  roadmap (`docs/design/modernization-roadmap.md`).

## 7. Code of conduct

Be respectful and constructive. Harassment or abuse of any kind is not tolerated.
(A full `CODE_OF_CONDUCT.md` may be added; until then, this applies.)

---

*Questions? Open a discussion or issue. Thanks for contributing! 🎉*
