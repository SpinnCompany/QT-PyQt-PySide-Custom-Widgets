# Compatibility shim: the design-token machinery lives under theming/ now.
# Everything below is re-exported from Custom_Widgets.theming.tokens so both
# import paths resolve to the SAME module object (no duplicate registration).
from Custom_Widgets.theming.tokens import *  # noqa: F401,F403
from Custom_Widgets.theming.tokens import (  # noqa: F401
    DesignTokens,
    sass_functions,
    applyDesignTokens,
    activeDesignTokens,
    button_qss,
    compile_scss,
)