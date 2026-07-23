########################################################################
## CUSTOM WIDGETS — TYPE STUB GENERATOR
##
## qtpy's dynamic imports + unwrapped enums make the widget classes opaque to
## type-checkers and to any agent that reasons about signatures. This generates
## PEP 484 `.pyi` stubs by INTROSPECTING the real classes (inspect), re-rooting
## each widget's base to the concrete, typed PySide6 class — so QCustomBadge is
## seen as `QLabel` (typed) instead of qtpy's opaque re-export.
##
## Regenerate the on-disk stubs after changing a widget's public API:
##     python -m Custom_Widgets.mcp.stubgen --write
##
## The same functions back the `widget_signature` MCP tool (generated live per
## call, so an agent never sees a stale signature).
########################################################################
import argparse
import glob
import importlib
import inspect
import os

_BUILTIN_TYPES = {
    "str": "str", "int": "int", "bool": "bool", "float": "float",
    "bytes": "bytes", "list": "list", "dict": "dict", "tuple": "tuple",
    "NoneType": "None",
}
# __catalog__ prop type -> stub type
_PROP_TYPE = {
    "string": "str", "str": "str", "enum": "str", "bool": "bool",
    "boolean": "bool", "int": "int", "integer": "int", "float": "float",
    "number": "float", "color": "str", "icon": "str",
}

_HEADER = ("# Auto-generated type stub — DO NOT EDIT.\n"
           "# Regenerate with:  python -m Custom_Widgets.mcp.stubgen --write\n")


def _widgets_package_dir():
    import Custom_Widgets
    return os.path.dirname(Custom_Widgets.__file__)


def _catalog_props():
    """{class_name: {prop: type}} from the AST catalog, for typing properties."""
    from Custom_Widgets.mcp.server import _discover_widgets
    out = {}
    for entry in _discover_widgets().values():
        types = {}
        for prop, meta in (entry.get("props") or {}).items():
            t = (meta or {}).get("type", "")
            types[prop] = _PROP_TYPE.get(str(t).lower(), "Any")
        out[entry["class"]] = types
    return out


def _catalog_modules():
    """Widget modules to stub: those that declare at least one __catalog__."""
    from Custom_Widgets.mcp.server import _discover_widgets
    return sorted({e["module"] for e in _discover_widgets().values()})


def _ann(annotation):
    """Render a parameter annotation conservatively — builtins keep their name,
    everything else collapses to Any so a stub never names an undefined type."""
    if annotation is inspect.Parameter.empty:
        return None
    name = getattr(annotation, "__name__", None)
    return _BUILTIN_TYPES.get(name, "Any")


def _render_params(func):
    try:
        sig = inspect.signature(func)
    except (ValueError, TypeError):
        return "self, *args: Any, **kwargs: Any"
    parts, seen_kwonly_marker = [], False
    for p in sig.parameters.values():
        if p.kind is p.KEYWORD_ONLY and not seen_kwonly_marker:
            parts.append("*")
            seen_kwonly_marker = True
        if p.kind is p.VAR_POSITIONAL:
            seen_kwonly_marker = True
            token = "*" + p.name
        elif p.kind is p.VAR_KEYWORD:
            token = "**" + p.name
        else:
            token = p.name
            ann = _ann(p.annotation)
            if ann:
                token += ": " + ann
            if p.default is not inspect.Parameter.empty:
                token += " = ..."
        parts.append(token)
    return ", ".join(parts)


def _is_public_method(name, value):
    return (not name.startswith("_") and
            (inspect.isfunction(value) or isinstance(value, (staticmethod,
                                                             classmethod))))


def stub_for_class(cls, prop_types=None):
    """Return the `.pyi` class block for one widget class via live
    introspection: bases, signals, declared properties, own public methods."""
    from qtpy.QtCore import Signal, Property
    prop_types = prop_types or {}
    bases = [b for b in cls.__bases__ if b is not object]
    base_str = ", ".join(b.__name__ for b in bases) or "object"
    lines = ["class %s(%s):" % (cls.__name__, base_str)]
    body = []

    for name, value in vars(cls).items():
        if isinstance(value, Signal):
            body.append("    %s: ClassVar[Signal]" % name)
    for name, value in vars(cls).items():
        if isinstance(value, Property):
            body.append("    %s: %s" % (name, prop_types.get(name, "Any")))

    if "__init__" in vars(cls):
        body.append("    def __init__(%s) -> None: ..."
                    % _render_params(vars(cls)["__init__"]))
    for name, value in vars(cls).items():
        if name == "__init__" or not _is_public_method(name, value):
            continue
        deco, func = "", value
        if isinstance(value, staticmethod):
            deco, func = "    @staticmethod\n", value.__func__
        elif isinstance(value, classmethod):
            deco, func = "    @classmethod\n", value.__func__
        params = _render_params(func)
        ret = " -> None" if name.startswith("set") else ""
        body.append("%s    def %s(%s)%s: ..." % (deco, name, params, ret))

    lines.extend(body or ["    ..."])
    return "\n".join(lines)


def _iter_module_classes(module):
    """Public classes actually DEFINED in this module (not imported)."""
    for name, value in vars(module).items():
        if (inspect.isclass(value) and not name.startswith("_")
                and value.__module__ == module.__name__):
            yield value


def _toposort(classes):
    """Order classes so an intra-module base is defined before its subclass."""
    names = {c.__name__ for c in classes}
    ordered, placed = [], set()

    def place(c):
        if c.__name__ in placed:
            return
        for b in c.__bases__:
            if b.__name__ in names and b.__name__ not in placed:
                nxt = next((x for x in classes if x.__name__ == b.__name__), None)
                if nxt is not None:
                    place(nxt)
        placed.add(c.__name__)
        ordered.append(c)

    for c in classes:
        place(c)
    return ordered


def stub_for_module(module_name, prop_types=None):
    """Full `.pyi` text for a widget module: every public class defined in it,
    with a resolved-and-typed base import for each."""
    prop_types = prop_types if prop_types is not None else _catalog_props()
    module = importlib.import_module(module_name)
    classes = _toposort(list(_iter_module_classes(module)))
    if not classes:
        return None

    from qtpy.QtCore import Signal
    imports = {}  # module -> {names}
    imports["typing"] = {"Any", "ClassVar"}
    # Import Signal from its concrete, typed binding module (e.g.
    # PySide6.QtCore), not qtpy — qtpy ships no stubs.
    imports[getattr(Signal, "__module__", "PySide6.QtCore")] = {"Signal"}
    for cls in classes:
        for base in cls.__bases__:
            if base is object or base.__module__ == module_name:
                continue
            imports.setdefault(base.__module__, set()).add(base.__name__)

    import_lines = []
    for mod in sorted(imports):
        names = ", ".join(sorted(imports[mod]))
        import_lines.append("from %s import %s" % (mod, names))

    blocks = [stub_for_class(cls, prop_types.get(cls.__name__, {}))
              for cls in classes]
    return _HEADER + "\n".join(import_lines) + "\n\n\n" + "\n\n\n".join(blocks) + "\n"


def generate_all():
    """{pyi_path: text} for every cataloged widget module."""
    prop_types = _catalog_props()
    out = {}
    for module_name in _catalog_modules():
        try:
            text = stub_for_module(module_name, prop_types)
        except Exception as exc:  # a single bad module must not sink the batch
            print("skip %s: %s" % (module_name, exc))
            continue
        if not text:
            continue
        rel = module_name.split(".", 1)[1].replace(".", os.sep)
        out[os.path.join(_widgets_package_dir(), rel + ".pyi")] = text
    return out


def write_all():
    """Write the stubs and the py.typed marker; return the list of paths."""
    written = []
    for path, text in generate_all().items():
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        written.append(path)
    marker = os.path.join(_widgets_package_dir(), "py.typed")
    if not os.path.exists(marker):
        with open(marker, "w", encoding="utf-8") as fh:
            fh.write("# PEP 561 marker: this package ships inline types + stubs.\n")
        written.append(marker)
    return written


def main():
    parser = argparse.ArgumentParser(description="Generate widget type stubs")
    parser.add_argument("--write", action="store_true",
                        help="write .pyi files next to the widget modules")
    args = parser.parse_args()
    if args.write:
        written = write_all()
        print("wrote %d files" % len(written))
        for p in written:
            print("  " + os.path.relpath(p, _widgets_package_dir()))
    else:
        stubs = generate_all()
        print("would write %d stub files (pass --write):" % len(stubs))
        for p in sorted(stubs):
            print("  " + os.path.relpath(p, _widgets_package_dir()))


if __name__ == "__main__":
    main()
