"""Tests for the design-token system and variant/size widget styling.

Covers primitive/{ref} resolution, per-theme semantic roles, generated QSS,
idempotent application, the button's variant/sizeVariant properties, and the
regression guard that `sizeVariant` (not `size`) is used so QWidget.size()
still works.
"""
from qtpy.QtWidgets import QApplication


class TestTokenResolution:
    def test_ref_chain_resolves_to_primitive(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens
        t = DesignTokens(theme="light")
        assert t.role("primary") == "#2563eb"        # {color.blue.600}
        assert t.role("on-primary") == "#ffffff"

    def test_theme_changes_roles(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens
        light = DesignTokens(theme="light")
        dark = DesignTokens(theme="dark")
        assert light.role("surface") != dark.role("surface")
        assert dark.role("surface") == "#0f172a"     # {color.slate.900}

    def test_primitive_path_and_px(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens
        t = DesignTokens()
        assert t.role("space.2") == 8
        assert t.px("radius.md") == "8px"

    def test_overrides_deep_merge(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens
        t = DesignTokens(theme="light",
                         semantic={"light": {"primary": "{color.red.600}"}})
        assert t.role("primary") == "#dc2626"
        assert t.role("on-primary") == "#ffffff"      # untouched role intact


class TestQssGeneration:
    def test_qss_has_variant_and_size_selectors(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens, button_qss
        qss = button_qss(DesignTokens(theme="light"))
        assert 'QCustomQPushButton[variant="primary"]' in qss
        assert 'QCustomQPushButton[variant="destructive"]' in qss
        assert 'QCustomQPushButton[sizeVariant="sm"]' in qss
        assert "#2563eb" in qss                        # resolved primary colour
        assert ":focus" in qss                         # a11y focus ring

    def test_apply_is_idempotent(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        w = QApplication.instance()
        applyDesignTokens(w, theme="light")
        once = w.styleSheet()
        applyDesignTokens(w, theme="light")
        twice = w.styleSheet()
        assert once == twice                           # no accumulation
        assert once.count("custom-widgets design tokens >>>") == 1
        w.setStyleSheet("")                            # clean up shared app state


class TestScssEngine:
    def test_token_function_compiles(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import compile_scss
        out = compile_scss("W { background-color: token('primary');"
                           " padding: token('space.2'); border-radius: token('radius.md');"
                           " font-weight: token('font.weight.semibold'); }", theme="light")
        assert "#2563eb" in out            # colour, unquoted
        assert "8px" in out                # space.2 / radius.md
        assert "600" in out                # weight, unitless

    def test_theme_switches_token_values(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import compile_scss
        assert "#2563eb" in compile_scss("W{c: token('primary');}", theme="light")
        assert "#3b82f6" in compile_scss("W{c: token('primary');}", theme="dark")

    def test_theme_colour_override_bridges(self, qapp):
        # QCustomTheme bridges the active theme colours onto token roles.
        from Custom_Widgets.JSonStyles.tokens import compile_scss, DesignTokens
        tokens = DesignTokens(theme="light",
                              semantic={"light": {"surface": "#123456"}})
        out = compile_scss("W{background-color: token('surface');}", tokens=tokens)
        assert "#123456" in out

    def test_qtsass_defaults_preserved(self, qapp):
        # Registering token() must not clobber qtsass's own functions.
        from Custom_Widgets.JSonStyles.tokens import compile_scss
        out = compile_scss(
            "W { background-color: token('primary');"
            " qproperty-x: qlineargradient(0, 0, 0, 1, (0 red, 1 blue)); }",
            theme="light")
        assert "#2563eb" in out
        assert "qlineargradient" in out    # qtsass default still worked

    def test_compile_from_file(self, qapp, tmp_path):
        from Custom_Widgets.JSonStyles.tokens import compile_scss
        f = tmp_path / "style.scss"
        f.write_text("W { color: token('on-surface'); }")
        out = compile_scss(str(f), theme="light", is_filename=True)
        assert "#0f172a" in out             # on-surface light


class TestDataTableTokens:
    def test_datatable_qss_selectors(self, qapp):
        from Custom_Widgets.JSonStyles.tokens import DesignTokens, datatable_qss
        qss = datatable_qss(DesignTokens(theme="light"))
        assert "QCustomDataTable QTableView" in qss
        assert "QCustomDataTable QHeaderView::section" in qss
        assert "selection-background-color: #2563eb" in qss   # accent
        assert '#dataTablePrev' in qss

    def test_header_paints_surface_muted(self, qapp):
        from qtpy.QtGui import QColor
        from Custom_Widgets.QCustomDataTable import QCustomDataTable, DataTableColumn
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        t = QCustomDataTable()
        t.setColumns([DataTableColumn("a"), DataTableColumn("b")])
        t.setData([{"a": "x", "b": 1}])
        t.pageSize = 0
        t.resize(300, 200)
        t.show()
        t.ensurePolished()
        hdr = t.view().horizontalHeader()
        c = QColor(hdr.grab().toImage().pixel(hdr.width() // 2, hdr.height() // 2))
        assert c.name().lower() == "#f1f5f9"          # light surface-muted
        applyDesignTokens(qapp, theme="dark")
        t.ensurePolished()
        c2 = QColor(hdr.grab().toImage().pixel(hdr.width() // 2, hdr.height() // 2))
        assert c2.name().lower() == "#1e293b"         # dark surface-muted
        qapp.setStyleSheet("")


class TestButtonVariant:
    def test_defaults_set_dynamic_properties(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        b = QCustomQPushButton()
        assert b.variant == "primary"
        assert b.sizeVariant == "md"
        assert b.property("variant") == "primary"
        assert b.property("sizeVariant") == "md"

    def test_setting_updates_dynamic_property(self, qapp):
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        b = QCustomQPushButton()
        b.variant = "ghost"
        b.sizeVariant = "lg"
        assert b.property("variant") == "ghost"        # QSS selector will match
        assert b.property("sizeVariant") == "lg"

    def test_variant_actually_paints(self, qapp):
        # End-to-end: a declared Qt property must be matched by the QSS
        # attribute selector and actually paint the token colour.
        from qtpy.QtGui import QColor
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        from Custom_Widgets.JSonStyles.tokens import applyDesignTokens
        applyDesignTokens(qapp, theme="light")
        b = QCustomQPushButton("")          # empty text -> solid fill to sample
        b.variant = "primary"
        b.resize(120, 40)
        b.ensurePolished()
        center = QColor(b.grab().toImage().pixel(60, 20)).name().lower()
        assert center == "#2563eb"          # primary token painted
        b.variant = "destructive"           # setter repolishes -> repaint
        b.ensurePolished()
        center = QColor(b.grab().toImage().pixel(60, 20)).name().lower()
        assert center == "#dc2626"
        qapp.setStyleSheet("")

    def test_size_method_not_shadowed(self, qapp):
        # Regression: naming the property `size` would shadow QWidget.size().
        from Custom_Widgets.QCustomQPushButton import QCustomQPushButton
        from Custom_Widgets.QCustomDataTable import QCustomDataTable
        b = QCustomQPushButton()
        assert b.size().isValid() or b.size() is not None  # callable, returns QSize
        t = QCustomDataTable()
        assert t.size() is not None                    # was broken with `size` prop
        assert t.sizeVariant == "md"


class TestScssImportDiagnostics:
    """The scss engine turns a dangling @import (which makes qtsass fail
    opaquely) into an actionable message. Pure/Qt-free helpers."""

    def _scss(self, tmp_path, name, body):
        p = tmp_path / name
        p.write_text(body)
        return str(p)

    def test_resolves_partial_and_plain(self, tmp_path):
        from Custom_Widgets.JSonStyles.tokens import find_unresolved_imports
        self._scss(tmp_path, "_vars.scss", "$x: 1;")
        self._scss(tmp_path, "extra.scss", "QLabel{}")
        root = self._scss(tmp_path, "main.scss",
                          "@import 'vars';\n@import 'extra';\nQWidget{}")
        assert find_unresolved_imports(root, [str(tmp_path)]) == []

    def test_flags_missing_import_recursively(self, tmp_path):
        from Custom_Widgets.JSonStyles.tokens import find_unresolved_imports
        # main -> default -> (missing) custom
        self._scss(tmp_path, "defaultStyle.scss", "@import 'custom';")
        root = self._scss(tmp_path, "main.scss", "@import 'defaultStyle';")
        problems = find_unresolved_imports(root, [str(tmp_path)])
        assert len(problems) == 1
        importer, name = problems[0]
        assert name == "custom"
        assert importer.endswith("defaultStyle.scss")

    def test_css_and_url_imports_are_ignored(self, tmp_path):
        from Custom_Widgets.JSonStyles.tokens import find_unresolved_imports
        root = self._scss(tmp_path, "main.scss",
                          "@import 'reset.css';\n@import 'https://x/y';")
        assert find_unresolved_imports(root, [str(tmp_path)]) == []

    def test_describe_names_file_and_partial(self, tmp_path):
        from Custom_Widgets.JSonStyles.tokens import describe_scss_compile_error
        self._scss(tmp_path, "defaultStyle.scss", "@import 'custom';")
        root = self._scss(tmp_path, "main.scss", "@import 'defaultStyle';")
        msg = describe_scss_compile_error(root, [str(tmp_path)])
        assert msg and "custom" in msg and "defaultStyle.scss" in msg

    def test_describe_returns_none_when_no_import_problem(self, tmp_path):
        from Custom_Widgets.JSonStyles.tokens import describe_scss_compile_error
        root = self._scss(tmp_path, "main.scss", "QWidget{ color: red; }")
        assert describe_scss_compile_error(root, [str(tmp_path)]) is None


class TestTokensUsedIsTrue:
    """`tokens_used` is consumed by the MCP server and the generated docs, so a
    wrong entry actively misinforms. It drifted badly once: 43 widgets declared
    roles while resolving none, and 10 named roles that do not exist at all
    (`up`, `down`, `background`, `text`).

    Checking it is subtler than it looks. Grepping the generator source for
    `r("role")` misses dynamic lookups -- alert_qss resolves 7 roles it never
    names literally and badge_qss 13, because both loop over variants as `r(v)`.
    Matching a generator to a widget by name is worse: `textarea_qss` merely
    MENTIONS QCustomInput in its docstring, which once pulled that generator's
    whole role set onto a widget with no generator of its own.

    So attribute per RULE: hand back a unique sentinel colour for every semantic
    role, emit the QSS, and read the sentinels back out of each rule's
    declarations. The selector says which class the rule targets.
    """

    @staticmethod
    def _attribution():
        import ast
        import re
        from Custom_Widgets.theming import tokens as T
        from Custom_Widgets.theming.tokens import _SEMANTIC
        from Custom_Widgets.mcp.catalog import discover_widgets

        roles = sorted(_SEMANTIC["light"])
        sentinel = {r: "#%06x" % (0xE70000 + i) for i, r in enumerate(roles)}
        back = {v: k for k, v in sentinel.items()}
        catalog = set(discover_widgets())

        src = open(T.__file__, encoding="utf-8").read()
        generators = {}
        for node in ast.parse(src).body:
            if isinstance(node, ast.FunctionDef) and node.name.endswith("_qss"):
                body = ast.get_source_segment(src, node) or ""
                generators[node.name] = {m for m in re.findall(r"\b(\w+_qss)\s*\(", body)
                                         if m != node.name}
        # build_component_qss and friends re-emit their children's rules
        aggregates = {g for g, calls in generators.items() if calls}

        rule = re.compile(r"([^{}]+)\{([^{}]*)\}", re.S)
        hexes = re.compile(r"#[0-9a-fA-F]{6}")
        klass = re.compile(r"\b(QCustom[A-Za-z0-9_]+|QTagEdit)\b")
        objname = re.compile(r"#([A-Za-z][A-Za-z0-9_]*)")

        # Many rules select by objectName alone (#colorHex, #comboPopup) and
        # name no class. Resolve those through the class that actually calls
        # setObjectName with that string -- #customCalendar belongs to
        # QCustomDateEdit, which is the only class that creates it.
        import pathlib
        owner_of = {}
        for path in pathlib.Path("Custom_Widgets/widgets").rglob("*.py"):
            try:
                tree = ast.parse(path.read_text(encoding="utf-8", errors="ignore"))
            except SyntaxError:
                continue
            for cls in [c for c in ast.walk(tree) if isinstance(c, ast.ClassDef)]:
                if cls.name not in catalog:
                    continue
                for call in ast.walk(cls):
                    if (isinstance(call, ast.Call)
                            and isinstance(call.func, ast.Attribute)
                            and call.func.attr == "setObjectName"
                            and call.args
                            and isinstance(call.args[0], ast.Constant)
                            and isinstance(call.args[0].value, str)):
                        owner_of.setdefault(call.args[0].value, set()).add(cls.name)

        original = T.DesignTokens.role
        T.DesignTokens.role = lambda self, name: sentinel.get(name) or original(self, name)
        try:
            found = {}
            for name in generators:
                if name in aggregates:
                    continue
                rules = []
                for theme in ("light", "dark"):
                    css = getattr(T, name)(T.DesignTokens(theme))
                    if isinstance(css, list):
                        css = "".join(css)
                    rules += rule.findall(css)
                owners = {c for selector, _ in rules
                          for c in klass.findall(selector) if c in catalog}
                for selector, decls in rules:
                    used = {back[h.lower()] for h in hexes.findall(decls)
                            if h.lower() in back}
                    if not used:
                        continue
                    classes = {c for c in klass.findall(selector) if c in catalog}
                    if not classes:
                        for obj in objname.findall(selector):
                            classes |= owner_of.get(obj, set())
                    if not classes and len(owners) == 1:
                        classes = set(owners)
                    for cls in classes:
                        found.setdefault(cls, set()).update(used)
        finally:
            T.DesignTokens.role = original
        return found

    def test_every_declared_role_exists(self, qapp):
        """Catches the `up` / `down` / `background` / `text` class of bug."""
        from Custom_Widgets.theming.tokens import _SEMANTIC
        from Custom_Widgets.mcp.catalog import discover_widgets, find_widget
        roles = set(_SEMANTIC["light"])
        bogus = [(name, role) for name in discover_widgets()
                 for role in (find_widget(name) or {}).get("tokens_used") or []
                 if role not in roles]
        assert not bogus, "tokens_used names roles that do not exist: %r" % (bogus,)

    def test_declarations_match_the_rules_that_target_them(self, qapp):
        """For widgets styled ONLY by QSS, the declaration must be exact.

        Restricted to widgets whose source never touches the token API: anything
        that resolves a role in paintEvent (the loaders, QCustomMessageStatus,
        the charts via their theme manager) would need a rendered widget to
        observe, which is out of scope for a unit test.
        """
        import pathlib
        import re
        from Custom_Widgets.mcp.catalog import find_widget
        touches = re.compile(r"activeDesignTokens|_tokenColor|_defaultColor|\.role\(")
        attributed = self._attribution()
        wrong = []
        for cls, used in attributed.items():
            entry = find_widget(cls)
            if not entry:
                continue
            path = pathlib.Path(entry["module"].replace(".", "/") + ".py")
            candidates = list(pathlib.Path("Custom_Widgets/widgets").rglob(path.name))
            if candidates and touches.search(
                    candidates[0].read_text(encoding="utf-8", errors="ignore")):
                continue                      # resolves roles in its paint path
            declared = set(entry.get("tokens_used") or [])
            if declared != used:
                wrong.append((cls, sorted(declared - used), sorted(used - declared)))
        assert not wrong, ("tokens_used disagrees with the rules targeting the "
                           "widget (class, over-claimed, under-claimed): %r" % (wrong,))


class TestOutlineIsNeverText:
    """Regression guard for the recurring bug: `outline` is a BORDER value
    (slate.300 = 1.48:1 on a light surface). Used as a text `color:` it makes
    the text invisible. 2.5.0 fixed six such sites; the inverse-contrast sweep
    found six more (statLabel, statCaption, cardSubtitle, kbdPlus, alertClose,
    HeaderNav's painted textColor). This proves none come back.

    Disabled controls and a stepper's not-yet-reached "pending" step are the
    only legitimate places outline may dim text -- both are WCAG-exempt
    inactive states.
    """

    def _outline_foregrounds(self, theme):
        import re
        from Custom_Widgets.theming import tokens as T
        tok = T.DesignTokens(theme=theme)
        outline = tok.role("outline")
        qss = T.build_component_qss(tok)
        # `(?<!-)color:` excludes background-color / border-color / selection-color.
        colour_re = re.compile(r"(?<!-)\bcolor:\s*(#[0-9a-fA-F]{6})")
        exempt = (":disabled", 'state="pending"')
        selector, hits = "", []
        for line in qss.splitlines():
            if "{" in line:
                selector = line.split("{", 1)[0]
            for hexval in colour_re.findall(line):
                if hexval.lower() == outline.lower() \
                        and not any(e in selector for e in exempt):
                    hits.append(selector.strip())
        return hits

    def test_outline_not_used_as_text_light(self, qapp):
        assert not self._outline_foregrounds("light"), \
            "outline (a border value) used as text colour: %r" \
            % self._outline_foregrounds("light")

    def test_outline_not_used_as_text_dark(self, qapp):
        assert not self._outline_foregrounds("dark"), \
            "outline (a border value) used as text colour: %r" \
            % self._outline_foregrounds("dark")
