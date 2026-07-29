# Final release scope: must-have features before release

This document defines the release scope for the first production-grade release. If a feature below is not implemented, it should be treated as a release blocker or deferred to the next release.

## 1. Core component completeness

The library must ship a complete enough base set of application widgets for real desktop apps.

- Virtualized data table / data grid with sorting, filtering, selection, and resize
- Searchable combobox / autocomplete for large option sets
- Toast / snackbar system for non-blocking feedback
- Drawer / popover / context menu support for modern UI flows
- Stepper / wizard flow for multi-step tasks

## 2. Unified component API

The public API must feel consistent across widgets.

- Every core widget should expose a standard `variant` API
- Every core widget should expose a standard `size` API
- Common icon, state, and disabled semantics should be consistent
- Widgets should be usable without hand-crafted QSS per instance

## 3. Design-token system

The theming story must be production-ready.

- Semantic tokens for surface, border, text, accent, success, warning, danger
- Theme switching by name without per-widget manual overrides
- Token-driven styling for buttons, cards, inputs, tables, and dialogs
- Clear documentation and examples for custom themes

## 4. Forms and validation layer

The package should support application building, not just widgets.

- Form field binding helpers
- Validation rules and error states
- Dirty / touched / submitted state tracking
- Submit handling and form-level feedback

## 5. Accessibility baseline

A release-quality desktop UI library needs accessibility support.

- Keyboard navigation and focus order
- Visible focus indicators
- Screen-reader roles and labels
- Reduced-motion support
- High-contrast theme compatibility

## 6. Responsive and adaptive layout support

The package should support modern desktop layouts.

- Breakpoint-aware containers
- Adaptive sidebar / content reflow
- Multi-monitor and high-DPI handling
- Layout behavior that degrades gracefully at narrow widths

## 7. Developer experience and templates

To sell the library as a product, it must be easy to adopt.

- Starter templates for dashboard, settings, admin CRUD, and chat-style UIs
- Component gallery / playground for quick evaluation
- Copy-paste examples that work without custom setup
- Clear install and first-run instructions

## 8. Release quality and packaging

The release must be dependable and easy to distribute.

- Verified wheel and sdist builds
- Clear dependency guidance for PySide6 / PyQt6
- Optional dependency documentation for extras
- Release notes and migration notes
- Verified install path from a clean environment

## 9. Testing and regression protection

The release should not ship with avoidable regressions.

- Automated UI and interaction tests for key components
- Visual regression checks for major examples
- CI validation for docs, build, and packaging

## 10. Product polish

These items are part of the final product experience.

- Polished example applications
- Clear value proposition in README and docs
- Stronger marketing story around AI-ready, agent-native, and modern desktop UI workflows

## Release decision rule

If an item above is missing, it should either be implemented before release or explicitly deferred with a visible, documented reason. The final release should not be treated as “feature-complete” unless the core experience above is covered.
