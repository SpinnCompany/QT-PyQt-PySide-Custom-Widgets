# Widget Tiering & Hardening Manifest

**Generated mechanically 2026-07-24** by `tools/scan_widgets.py` (test / example /
`__catalog__` / Designer-registration / `.pyi` coverage per widget). This is the
launch gate artifact: no free/pro SKU split is locked until every user-facing row
below is **tested, stable, secure, and tier-classified**, then the whole product
ships at once. Tiers here are **first-pass proposals for ratification**, not final.

> Regenerate: `python tools/scan_widgets.py`. Presence signals are objective; the
> **Tier** and **Stable/Secure** judgments are human.

## Coverage summary (108 widget modules)

| Signal | Coverage |
|---|---|
| Has a test | 80/108 (74%) |
| Has an example | 84/108 (78%) |
| In `__catalog__` | 54/108 (50%) |
| Designer-registered | 74/108 (69%) |
| `.pyi` type stub | 54/108 (50%) |

Breakdown: **5** free-base-with-Pro-extension, **89** free
standalone, **14** internal/engine (not shipped as standalone).

## Legend
- **Test / Example / Catalog / Designer / .pyi** -- objective presence signals.
- **Tier** -- proposed classification: `free` (ships free, standalone),
  `free -> Pro` (free base kept in core, a compiled Pro widget extends it),
  `internal` (engine/helper, not a standalone shipped widget).
- **Stable / Secure** -- filled during the hardening pass (not mechanical).

---

## Tier: free base -> Pro extension (5)

Stay free in the core; the Pro package extends them (never bundles them).

| Widget | Test | Example | Catalog | Designer | .pyi | LOC | Module |
|---|:--:|:--:|:--:|:--:|:--:|--:|---|
| `QCustomAreaChart` | ✅ | ✅ | — | ✅ | — | 1135 | Custom_Widgets/QCustomCharts/QCustomAreaChart.py |
| `QCustomBarChart` | ✅ | ✅ | — | ✅ | — | 1044 | Custom_Widgets/QCustomCharts/QCustomBarChart.py |
| `QCustomDataTable` | ✅ | ✅ | ✅ | ✅ | ✅ | 1824 | Custom_Widgets/QCustomDataTable.py |
| `QCustomLineChart` | ✅ | ✅ | — | ✅ | — | 735 | Custom_Widgets/QCustomCharts/QCustomLineChart.py |
| `QCustomPieChart` | ✅ | ✅ | — | ✅ | — | 1612 | Custom_Widgets/QCustomCharts/QCustomPieChart.py |

Pro mapping:
- `QCustomDataTable` -> DataTable Pro (SKU-1, built)
- `QCustomAreaChart` -> Charts Pro (SKU-2, candidate)
- `QCustomLineChart` -> Charts Pro (SKU-2, candidate)
- `QCustomBarChart` -> Charts Pro (SKU-2, candidate)
- `QCustomPieChart` -> Charts Pro (SKU-2, candidate)

## Tier: free -- standalone (89)

| Widget | Test | Example | Catalog | Designer | .pyi | LOC | Module |
|---|:--:|:--:|:--:|:--:|:--:|--:|---|
| `AnalogGaugeWidget` | ✅ | ✅ | — | ✅ | — | 1014 | Custom_Widgets/AnalogGaugeWidget.py |
| `Canvas` | — | — | — | — | — | 547 | Custom_Widgets/QCustomAnnotationWidget.py |
| `LoadForm` | — | ✅ | — | — | — | 873 | Custom_Widgets/QCustomModals.py |
| `QCustomAccordion` | ✅ | ✅ | ✅ | ✅ | ✅ | 150 | Custom_Widgets/QCustomAccordion.py |
| `QCustomActionButton` | — | ✅ | ✅ | ✅ | ✅ | 153 | Custom_Widgets/QCustomActionButton.py |
| `QCustomAlert` | ✅ | ✅ | ✅ | ✅ | ✅ | 166 | Custom_Widgets/QCustomAlert.py |
| `QCustomAvatar` | — | ✅ | ✅ | ✅ | ✅ | 253 | Custom_Widgets/QCustomAvatar.py |
| `QCustomAvatarGroup` | ✅ | ✅ | ✅ | ✅ | ✅ | 150 | Custom_Widgets/QCustomAvatarGroup.py |
| `QCustomBadge` | ✅ | ✅ | ✅ | ✅ | ✅ | 224 | Custom_Widgets/QCustomBadge.py |
| `QCustomBreadcrumbs` | ✅ | ✅ | ✅ | ✅ | ✅ | 89 | Custom_Widgets/QCustomBreadcrumbs.py |
| `QCustomCard` | ✅ | ✅ | ✅ | ✅ | ✅ | 118 | Custom_Widgets/QCustomCard.py |
| `QCustomCarousel` | ✅ | ✅ | ✅ | ✅ | ✅ | 224 | Custom_Widgets/QCustomCarousel.py |
| `QCustomChatBubble` | ✅ | ✅ | ✅ | ✅ | ✅ | 366 | Custom_Widgets/QCustomChatBubble.py |
| `QCustomChatDivider` | ✅ | — | ✅ | ✅ | ✅ | 183 | Custom_Widgets/QCustomChatDivider.py |
| `QCustomChatInput` | ✅ | ✅ | ✅ | ✅ | ✅ | 174 | Custom_Widgets/QCustomChatInput.py |
| `QCustomChatList` | ✅ | ✅ | ✅ | ✅ | ✅ | 262 | Custom_Widgets/QCustomChatList.py |
| `QCustomChatListItem` | ✅ | ✅ | ✅ | ✅ | ✅ | 406 | Custom_Widgets/QCustomChatListItem.py |
| `QCustomChatThread` | ✅ | ✅ | ✅ | ✅ | ✅ | 281 | Custom_Widgets/QCustomChatThread.py |
| `QCustomCheckBox` | ✅ | ✅ | — | ✅ | — | 269 | Custom_Widgets/QCustomCheckBox.py |
| `QCustomChip` | ✅ | ✅ | ✅ | ✅ | ✅ | 181 | Custom_Widgets/QCustomChip.py |
| `QCustomCodeEditor` | — | ✅ | — | — | — | 330 | Custom_Widgets/QCustomCodeEditor.py |
| `QCustomColorPicker` | ✅ | ✅ | ✅ | ✅ | ✅ | 139 | Custom_Widgets/QCustomColorPicker.py |
| `QCustomComboBox` | ✅ | ✅ | ✅ | ✅ | ✅ | 140 | Custom_Widgets/QCustomComboBox.py |
| `QCustomCommandPalette` | ✅ | ✅ | ✅ | — | ✅ | 247 | Custom_Widgets/QCustomCommandPalette.py |
| `QCustomComponent` | ✅ | ✅ | — | ✅ | — | 114 | Custom_Widgets/QCustomComponent.py |
| `QCustomComponentContainer` | ✅ | ✅ | — | ✅ | — | 171 | Custom_Widgets/QCustomComponentContainer.py |
| `QCustomComponentLoader` | ✅ | — | — | — | — | 678 | Custom_Widgets/QCustomComponentLoader.py |
| `QCustomDateEdit` | ✅ | ✅ | ✅ | ✅ | ✅ | 181 | Custom_Widgets/QCustomDateTimeEdit.py |
| `QCustomDonut` | ✅ | ✅ | ✅ | — | ✅ | 241 | Custom_Widgets/QCustomDonut.py |
| `QCustomDrawer` | ✅ | ✅ | ✅ | — | ✅ | 138 | Custom_Widgets/QCustomDrawer.py |
| `QCustomEmbeddedWindow` | — | ✅ | — | — | — | 266 | Custom_Widgets/QCustomEmbeddedWindow.py |
| `QCustomEmojiPicker` | — | ✅ | — | — | — | 557 | Custom_Widgets/QCustomEmojiPicker.py |
| `QCustomEmptyState` | ✅ | ✅ | ✅ | ✅ | ✅ | 90 | Custom_Widgets/QCustomEmptyState.py |
| `QCustomFileDropZone` | ✅ | ✅ | ✅ | ✅ | ✅ | 160 | Custom_Widgets/QCustomFileDropZone.py |
| `QCustomFlowLayout` | ✅ | ✅ | — | ✅ | — | 750 | Custom_Widgets/QCustomFlowLayout.py |
| `QCustomFlowWidget` | ✅ | ✅ | — | ✅ | — | 399 | Custom_Widgets/QCustomFlowWidget.py |
| `QCustomHamburgerMenu` | ✅ | — | — | ✅ | — | 839 | Custom_Widgets/QCustomHamburgerMenu.py |
| `QCustomHorizontalSeparator` | ✅ | — | — | ✅ | — | 119 | Custom_Widgets/QCustomHorizontalSeparator.py |
| `QCustomKbd` | ✅ | ✅ | ✅ | ✅ | ✅ | 112 | Custom_Widgets/QCustomKbd.py |
| `QCustomListRow` | — | ✅ | ✅ | ✅ | ✅ | 260 | Custom_Widgets/QCustomListRow.py |
| `QCustomLoadingIndicators` | ✅ | ✅ | — | ✅ | — | 7 | Custom_Widgets/QCustomLoadingIndicators.py |
| `QCustomMediaGrid` | — | ✅ | ✅ | ✅ | ✅ | 189 | Custom_Widgets/QCustomMediaGrid.py |
| `QCustomMiniBarChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 288 | Custom_Widgets/QCustomMiniBarChart.py |
| `QCustomNumberInput` | ✅ | ✅ | ✅ | ✅ | ✅ | 196 | Custom_Widgets/QCustomNumberInput.py |
| `QCustomPageDots` | ✅ | ✅ | ✅ | ✅ | ✅ | 236 | Custom_Widgets/QCustomPageDots.py |
| `QCustomPagination` | ✅ | ✅ | ✅ | ✅ | ✅ | 122 | Custom_Widgets/QCustomPagination.py |
| `QCustomPaymentCard` | — | ✅ | ✅ | ✅ | ✅ | 358 | Custom_Widgets/QCustomPaymentCard.py |
| `QCustomPopover` | ✅ | ✅ | ✅ | — | ✅ | 171 | Custom_Widgets/QCustomPopover.py |
| `QCustomProgressBars` | ✅ | ✅ | — | ✅ | — | 1 | Custom_Widgets/QCustomProgressBars.py |
| `QCustomProgressIndicator` | ✅ | ✅ | — | — | — | 375 | Custom_Widgets/QCustomProgressIndicator.py |
| `QCustomProgressRing` | ✅ | ✅ | ✅ | ✅ | ✅ | 190 | Custom_Widgets/QCustomProgressRing.py |
| `QCustomQDialog` | — | ✅ | — | — | — | 489 | Custom_Widgets/QCustomQDialog.py |
| `QCustomQMainWindow` | ✅ | ✅ | — | ✅ | — | 484 | Custom_Widgets/QCustomQMainWindow.py |
| `QCustomQPushButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 538 | Custom_Widgets/QCustomQPushButton.py |
| `QCustomQPushButtonGroup` | — | ✅ | — | — | — | 60 | Custom_Widgets/QCustomQPushButtonGroup.py |
| `QCustomQRGenerator` | ✅ | — | — | ✅ | — | 721 | Custom_Widgets/QCustomQRGenerator.py |
| `QCustomQSlider` | — | ✅ | — | — | — | 47 | Custom_Widgets/QCustomQSlider.py |
| `QCustomQStackedWidget` | ✅ | ✅ | — | ✅ | — | 816 | Custom_Widgets/QCustomQStackedWidget.py |
| `QCustomQToolTip` | — | ✅ | — | — | — | 662 | Custom_Widgets/QCustomQToolTip.py |
| `QCustomRangeSlider` | ✅ | ✅ | ✅ | ✅ | ✅ | 220 | Custom_Widgets/QCustomRangeSlider.py |
| `QCustomRating` | ✅ | ✅ | ✅ | ✅ | ✅ | 135 | Custom_Widgets/QCustomRating.py |
| `QCustomRichTextEditor` | ✅ | ✅ | ✅ | ✅ | ✅ | 186 | Custom_Widgets/QCustomRichTextEditor.py |
| `QCustomSegmentedControl` | ✅ | ✅ | ✅ | ✅ | ✅ | 121 | Custom_Widgets/QCustomSegmentedControl.py |
| `QCustomSidebar` | ✅ | ✅ | — | ✅ | — | 310 | Custom_Widgets/QCustomSidebar.py |
| `QCustomSidebarButton` | ✅ | ✅ | — | ✅ | — | 475 | Custom_Widgets/QCustomSidebarButton.py |
| `QCustomSidebarContainer` | ✅ | — | — | ✅ | — | 246 | Custom_Widgets/QCustomSidebarContainer.py |
| `QCustomSidebarLabel` | ✅ | ✅ | — | ✅ | — | 241 | Custom_Widgets/QCustomSidebarLabel.py |
| `QCustomSkeleton` | ✅ | ✅ | ✅ | ✅ | ✅ | 134 | Custom_Widgets/QCustomSkeleton.py |
| `QCustomSlideMenu` | — | ✅ | — | — | — | 607 | Custom_Widgets/QCustomSlideMenu.py |
| `QCustomSparkline` | ✅ | ✅ | ✅ | — | ✅ | 207 | Custom_Widgets/QCustomSparkline.py |
| `QCustomSplitter` | ✅ | ✅ | ✅ | ✅ | ✅ | 57 | Custom_Widgets/QCustomSplitter.py |
| `QCustomStatCard` | ✅ | ✅ | ✅ | ✅ | ✅ | 160 | Custom_Widgets/QCustomStatCard.py |
| `QCustomStepper` | ✅ | ✅ | ✅ | ✅ | ✅ | 132 | Custom_Widgets/QCustomStepper.py |
| `QCustomSwitch` | ✅ | ✅ | ✅ | ✅ | ✅ | 190 | Custom_Widgets/QCustomSwitch.py |
| `QCustomTableToolbar` | ✅ | ✅ | ✅ | ✅ | ✅ | 541 | Custom_Widgets/QCustomTableToolbar.py |
| `QCustomTabWidget` | ✅ | ✅ | ✅ | ✅ | ✅ | 76 | Custom_Widgets/QCustomTabWidget.py |
| `QCustomTheme` | ✅ | ✅ | — | — | — | 1654 | Custom_Widgets/QCustomTheme.py |
| `QCustomThemeDarkLightToggle` | ✅ | ✅ | — | ✅ | — | 140 | Custom_Widgets/QCustomThemeDarkLightToggle.py |
| `QCustomThemeList` | ✅ | ✅ | — | ✅ | — | 139 | Custom_Widgets/QCustomThemeList.py |
| `QCustomTimeline` | ✅ | ✅ | ✅ | ✅ | ✅ | 143 | Custom_Widgets/QCustomTimeline.py |
| `QCustomTipOverlay` | — | ✅ | — | — | — | 1043 | Custom_Widgets/QCustomTipOverlay.py |
| `QCustomToast` | ✅ | ✅ | ✅ | — | ✅ | 233 | Custom_Widgets/QCustomToast.py |
| `QCustomTreeWidget` | ✅ | ✅ | ✅ | ✅ | ✅ | 102 | Custom_Widgets/QCustomTreeWidget.py |
| `QCustomTrendChip` | ✅ | ✅ | ✅ | ✅ | ✅ | 251 | Custom_Widgets/QCustomTrendChip.py |
| `QCustomTypingIndicator` | ✅ | — | ✅ | ✅ | ✅ | 144 | Custom_Widgets/QCustomTypingIndicator.py |
| `QCustomVerticalSeparator` | ✅ | — | — | ✅ | — | 117 | Custom_Widgets/QCustomVerticalSeparator.py |
| `QCustomVoiceMessage` | ✅ | ✅ | ✅ | ✅ | ✅ | 302 | Custom_Widgets/QCustomVoiceMessage.py |
| `QFlowProgressBar` | ✅ | ✅ | — | — | — | 381 | Custom_Widgets/QFlowProgressBar.py |
| `QTagEdit` | — | — | — | — | — | 266 | Custom_Widgets/QCustomTagEdit.py |

## Internal / engine -- not standalone widgets (14)

Chart-subsystem engine + shared helpers. Ship as free library internals; no
separate tier. (Most surface through the public chart types above.)

| Widget | Test | Example | Catalog | Designer | .pyi | LOC | Module |
|---|:--:|:--:|:--:|:--:|:--:|--:|---|
| `QCustomBarChartBase` | — | — | — | — | — | 1932 | Custom_Widgets/QCustomCharts/QCustomBarChartBase.py |
| `QCustomChartBase` | — | — | — | — | — | 377 | Custom_Widgets/QCustomCharts/QCustomChartBase.py |
| `QCustomChartConstants` | ✅ | — | — | — | — | 372 | Custom_Widgets/QCustomCharts/QCustomChartConstants.py |
| `QCustomChartDataManager` | — | — | — | — | — | 605 | Custom_Widgets/QCustomCharts/QCustomChartDataManager.py |
| `QCustomChartExporter` | — | — | — | — | — | 575 | Custom_Widgets/QCustomCharts/QCustomChartExporter.py |
| `QCustomChartProps` | — | — | — | — | — | 369 | Custom_Widgets/QCustomCharts/QCustomChartProps.py |
| `QCustomChartThemeManager` | — | — | — | — | — | 444 | Custom_Widgets/QCustomCharts/QCustomChartThemeManager.py |
| `QCustomChartToolbar` | — | — | — | — | — | 511 | Custom_Widgets/QCustomCharts/QCustomChartToolbar.py |
| `QCustomChartTooltip` | — | — | — | — | — | 415 | Custom_Widgets/QCustomCharts/QCustomChartTooltip.py |
| `QCustomChartView` | — | — | — | — | — | 483 | Custom_Widgets/QCustomCharts/QCustomChartView.py |
| `QCustomHorizontalBarSeries` | ✅ | — | — | ✅ | — | 271 | Custom_Widgets/QCustomCharts/QCustomHorizontalBarSeries.py |
| `QCustomLegendManager` | — | — | — | — | — | 431 | Custom_Widgets/QCustomCharts/QCustomLegendManager.py |
| `QCustomQLineSeries` | — | — | — | — | — | 127 | Custom_Widgets/QCustomCharts/QCustomQLineSeries.py |
| `QCustomVerticalBarSeries` | ✅ | — | — | ✅ | — | 272 | Custom_Widgets/QCustomCharts/QCustomVerticalBarSeries.py |

---

## Hardening backlog (drives the gate)

### Untested user-facing widgets (17) -- highest priority
- `Canvas` (QCustomAnnotationWidget.py)
- `LoadForm` (QCustomModals.py)
- `QCustomActionButton` (QCustomActionButton.py)
- `QCustomAvatar` (QCustomAvatar.py)
- `QCustomCodeEditor` (QCustomCodeEditor.py)
- `QCustomEmbeddedWindow` (QCustomEmbeddedWindow.py)
- `QCustomEmojiPicker` (QCustomEmojiPicker.py)
- `QCustomListRow` (QCustomListRow.py)
- `QCustomMediaGrid` (QCustomMediaGrid.py)
- `QCustomPaymentCard` (QCustomPaymentCard.py)
- `QCustomQDialog` (QCustomQDialog.py)
- `QCustomQPushButtonGroup` (QCustomQPushButtonGroup.py)
- `QCustomQSlider` (QCustomQSlider.py)
- `QCustomQToolTip` (QCustomQToolTip.py)
- `QCustomSlideMenu` (QCustomSlideMenu.py)
- `QCustomTipOverlay` (QCustomTipOverlay.py)
- `QTagEdit` (QCustomTagEdit.py)

### Missing `__catalog__` entry (40)
- `AnalogGaugeWidget`
- `Canvas`
- `LoadForm`
- `QCustomAreaChart`
- `QCustomBarChart`
- `QCustomCheckBox`
- `QCustomCodeEditor`
- `QCustomComponent`
- `QCustomComponentContainer`
- `QCustomComponentLoader`
- `QCustomEmbeddedWindow`
- `QCustomEmojiPicker`
- `QCustomFlowLayout`
- `QCustomFlowWidget`
- `QCustomHamburgerMenu`
- `QCustomHorizontalSeparator`
- `QCustomLineChart`
- `QCustomLoadingIndicators`
- `QCustomPieChart`
- `QCustomProgressBars`
- `QCustomProgressIndicator`
- `QCustomQDialog`
- `QCustomQMainWindow`
- `QCustomQPushButtonGroup`
- `QCustomQRGenerator`
- `QCustomQSlider`
- `QCustomQStackedWidget`
- `QCustomQToolTip`
- `QCustomSidebar`
- `QCustomSidebarButton`
- `QCustomSidebarContainer`
- `QCustomSidebarLabel`
- `QCustomSlideMenu`
- `QCustomTheme`
- `QCustomThemeDarkLightToggle`
- `QCustomThemeList`
- `QCustomTipOverlay`
- `QCustomVerticalSeparator`
- `QFlowProgressBar`
- `QTagEdit`

### Missing example (10)
- `Canvas`
- `QCustomChatDivider`
- `QCustomComponentLoader`
- `QCustomHamburgerMenu`
- `QCustomHorizontalSeparator`
- `QCustomQRGenerator`
- `QCustomSidebarContainer`
- `QCustomTypingIndicator`
- `QCustomVerticalSeparator`
- `QTagEdit`

## Per-widget hardening checklist (fill during the pass)

Before a tier is locked, each user-facing widget needs:
- [ ] Test present & passing (headless)
- [ ] Example present & runs
- [ ] `__catalog__` entry (name, group, capabilities, edition)
- [ ] `.pyi` stub for IDE/Designer typing
- [ ] Stability: no crash on empty/huge/edge inputs; theme-switch safe
- [ ] Security: no eval/exec/network/file-write on untrusted input; QSS-injection safe
- [ ] Tier ratified (free / free-to-Pro / internal)
