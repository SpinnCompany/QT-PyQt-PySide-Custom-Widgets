# Widget Tiering & Hardening Manifest

**Generated mechanically 2026-07-31** by `tools/scan_widgets.py` (test / example /
`__catalog__` / Designer-registration / `.pyi` coverage per widget). This is the
launch gate artifact: no free/pro SKU split is locked until every user-facing row
below is **tested, stable, secure, and tier-classified**, then the whole product
ships at once.

> **Tiers RATIFIED 2026-07-31:** everything is **free** except the 5 anchors
> (`free -> Pro`); DataTable Pro is locked, Charts Pro is a candidate. No Pro
> "watchlist" earmarks - mini data-viz, editors, tree and timeline all stay free
> for now. `internal` = engine + infrastructure (still open-source, not a
> sellable widget). Remaining gate work: the per-widget **Stable/Secure** review.

> Regenerate: `python tools/scan_widgets.py`. Presence signals are objective; the
> tier decisions above are ratified; Stable/Secure remain a human review pass.

## Coverage summary (147 widget modules)

| Signal | Coverage |
|---|---|
| Has a test | 128/147 (87%) |
| Has an example | 120/147 (82%) |
| In `__catalog__` | 92/147 (63%) |
| Designer-registered | 110/147 (75%) |
| `.pyi` type stub | 91/147 (62%) |

Breakdown: **5** free-base-with-Pro-extension, **123** free
standalone, **19** internal/engine (not shipped as standalone).

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
| `QCustomPieChart` | ✅ | ✅ | — | ✅ | — | 1706 | Custom_Widgets/QCustomCharts/QCustomPieChart.py |

Pro mapping:
- `QCustomDataTable` -> DataTable Pro (SKU-1, LOCKED - built)
- `QCustomAreaChart` -> Charts Pro (SKU-2, candidate)
- `QCustomLineChart` -> Charts Pro (SKU-2, candidate)
- `QCustomBarChart` -> Charts Pro (SKU-2, candidate)
- `QCustomPieChart` -> Charts Pro (SKU-2, candidate)

## Tier: free -- standalone (123)

| Widget | Test | Example | Catalog | Designer | .pyi | LOC | Module |
|---|:--:|:--:|:--:|:--:|:--:|--:|---|
| `AnalogGaugeWidget` | ✅ | ✅ | — | ✅ | — | 1014 | Custom_Widgets/AnalogGaugeWidget.py |
| `QCustomAccordion` | ✅ | ✅ | ✅ | ✅ | ✅ | 150 | Custom_Widgets/QCustomAccordion.py |
| `QCustomActionButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 152 | Custom_Widgets/QCustomActionButton.py |
| `QCustomAgendaList` | ✅ | ✅ | ✅ | ✅ | ✅ | 365 | Custom_Widgets/QCustomAgendaList.py |
| `QCustomAlert` | ✅ | ✅ | ✅ | ✅ | ✅ | 166 | Custom_Widgets/QCustomAlert.py |
| `QCustomAnnotationWidget` | ✅ | — | — | — | — | 547 | Custom_Widgets/QCustomAnnotationWidget.py |
| `QCustomAvatar` | ✅ | ✅ | ✅ | ✅ | ✅ | 297 | Custom_Widgets/QCustomAvatar.py |
| `QCustomAvatarGroup` | ✅ | ✅ | ✅ | ✅ | ✅ | 150 | Custom_Widgets/QCustomAvatarGroup.py |
| `QCustomBadge` | ✅ | ✅ | ✅ | ✅ | ✅ | 224 | Custom_Widgets/QCustomBadge.py |
| `QCustomBeeswarm` | ✅ | ✅ | ✅ | ✅ | ✅ | 303 | Custom_Widgets/QCustomBeeswarm.py |
| `QCustomBreadcrumbs` | ✅ | ✅ | ✅ | ✅ | ✅ | 89 | Custom_Widgets/QCustomBreadcrumbs.py |
| `QCustomBubbleChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 634 | Custom_Widgets/QCustomBubbleChart.py |
| `QCustomButtonGroup` | ✅ | ✅ | ✅ | — | ✅ | 160 | Custom_Widgets/QCustomButtonGroup.py |
| `QCustomCandlestickChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 501 | Custom_Widgets/QCustomCandlestickChart.py |
| `QCustomCard` | ✅ | ✅ | ✅ | ✅ | ✅ | 118 | Custom_Widgets/QCustomCard.py |
| `QCustomCardStack` | ✅ | ✅ | ✅ | ✅ | ✅ | 283 | Custom_Widgets/QCustomCardStack.py |
| `QCustomCarousel` | ✅ | ✅ | ✅ | ✅ | ✅ | 224 | Custom_Widgets/QCustomCarousel.py |
| `QCustomChatBubble` | ✅ | ✅ | ✅ | ✅ | ✅ | 410 | Custom_Widgets/QCustomChatBubble.py |
| `QCustomChatDivider` | ✅ | — | ✅ | ✅ | ✅ | 180 | Custom_Widgets/QCustomChatDivider.py |
| `QCustomChatInput` | ✅ | ✅ | ✅ | ✅ | ✅ | 174 | Custom_Widgets/QCustomChatInput.py |
| `QCustomChatList` | ✅ | ✅ | ✅ | ✅ | ✅ | 262 | Custom_Widgets/QCustomChatList.py |
| `QCustomChatListItem` | ✅ | ✅ | ✅ | ✅ | ✅ | 401 | Custom_Widgets/QCustomChatListItem.py |
| `QCustomChatThread` | ✅ | ✅ | ✅ | ✅ | ✅ | 412 | Custom_Widgets/QCustomChatThread.py |
| `QCustomCheckBox` | ✅ | ✅ | — | ✅ | — | 269 | Custom_Widgets/QCustomCheckBox.py |
| `QCustomChip` | ✅ | ✅ | ✅ | ✅ | ✅ | 181 | Custom_Widgets/QCustomChip.py |
| `QCustomClockLabel` | ✅ | ✅ | ✅ | ✅ | ✅ | 89 | Custom_Widgets/QCustomClockLabel.py |
| `QCustomCodeEditor` | ✅ | ✅ | — | — | — | 342 | Custom_Widgets/QCustomCodeEditor.py |
| `QCustomColorPicker` | ✅ | ✅ | ✅ | ✅ | ✅ | 139 | Custom_Widgets/QCustomColorPicker.py |
| `QCustomComboBox` | ✅ | ✅ | ✅ | ✅ | ✅ | 140 | Custom_Widgets/QCustomComboBox.py |
| `QCustomCommandPalette` | ✅ | ✅ | ✅ | — | ✅ | 247 | Custom_Widgets/QCustomCommandPalette.py |
| `QCustomCompass` | ✅ | ✅ | ✅ | ✅ | ✅ | 374 | Custom_Widgets/QCustomCompass.py |
| `QCustomCompassDial` | ✅ | ✅ | ✅ | ✅ | ✅ | 400 | Custom_Widgets/QCustomCompassDial.py |
| `QCustomCoverCard` | — | ✅ | ✅ | ✅ | ✅ | 406 | Custom_Widgets/QCustomCoverCard.py |
| `QCustomCoverFlow` | — | ✅ | ✅ | ✅ | ✅ | 539 | Custom_Widgets/QCustomCoverFlow.py |
| `QCustomDateEdit` | ✅ | ✅ | ✅ | ✅ | ✅ | 181 | Custom_Widgets/QCustomDateTimeEdit.py |
| `QCustomDateRangePicker` | ✅ | ✅ | ✅ | ✅ | ✅ | 413 | Custom_Widgets/QCustomDateRangePicker.py |
| `QCustomDivergingBarChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 412 | Custom_Widgets/QCustomDivergingBarChart.py |
| `QCustomDonut` | ✅ | ✅ | ✅ | — | ✅ | 398 | Custom_Widgets/QCustomDonut.py |
| `QCustomDotMatrix` | ✅ | ✅ | ✅ | ✅ | ✅ | 253 | Custom_Widgets/QCustomDotMatrix.py |
| `QCustomDrawer` | ✅ | ✅ | ✅ | — | ✅ | 138 | Custom_Widgets/QCustomDrawer.py |
| `QCustomEmbeddedWindow` | ✅ | ✅ | — | — | — | 266 | Custom_Widgets/QCustomEmbeddedWindow.py |
| `QCustomEmojiPicker` | ✅ | ✅ | — | — | — | 557 | Custom_Widgets/QCustomEmojiPicker.py |
| `QCustomEmptyState` | ✅ | ✅ | ✅ | ✅ | ✅ | 90 | Custom_Widgets/QCustomEmptyState.py |
| `QCustomFileCard` | — | ✅ | ✅ | ✅ | ✅ | 263 | Custom_Widgets/QCustomFileCard.py |
| `QCustomFileDropZone` | ✅ | ✅ | ✅ | ✅ | ✅ | 160 | Custom_Widgets/QCustomFileDropZone.py |
| `QCustomFlowLayout` | ✅ | ✅ | — | ✅ | — | 750 | Custom_Widgets/QCustomFlowLayout.py |
| `QCustomFlowWidget` | ✅ | ✅ | — | ✅ | — | 399 | Custom_Widgets/QCustomFlowWidget.py |
| `QCustomForm` | ✅ | ✅ | — | — | — | 114 | Custom_Widgets/QCustomForm.py |
| `QCustomGanttChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 361 | Custom_Widgets/QCustomGanttChart.py |
| `QCustomGlassFrame` | ✅ | ✅ | ✅ | ✅ | ✅ | 529 | Custom_Widgets/QCustomGlassFrame.py |
| `QCustomHamburgerMenu` | ✅ | — | — | ✅ | — | 839 | Custom_Widgets/QCustomHamburgerMenu.py |
| `QCustomHeatmap` | ✅ | ✅ | ✅ | ✅ | ✅ | 527 | Custom_Widgets/QCustomHeatmap.py |
| `QCustomHorizontalSeparator` | ✅ | — | — | ✅ | — | 119 | Custom_Widgets/QCustomHorizontalSeparator.py |
| `QCustomImageViewer` | — | ✅ | ✅ | ✅ | ✅ | 301 | Custom_Widgets/QCustomImageViewer.py |
| `QCustomInput` | ✅ | ✅ | ✅ | — | ✅ | 115 | Custom_Widgets/QCustomInput.py |
| `QCustomKbd` | ✅ | ✅ | ✅ | ✅ | ✅ | 112 | Custom_Widgets/QCustomKbd.py |
| `QCustomLinkPreview` | — | ✅ | ✅ | ✅ | ✅ | 211 | Custom_Widgets/QCustomLinkPreview.py |
| `QCustomLiquidGauge` | ✅ | ✅ | ✅ | ✅ | ✅ | 502 | Custom_Widgets/QCustomLiquidGauge.py |
| `QCustomListRow` | ✅ | ✅ | ✅ | ✅ | ✅ | 311 | Custom_Widgets/QCustomListRow.py |
| `QCustomLoadingIndicators` | ✅ | ✅ | — | ✅ | — | 7 | Custom_Widgets/QCustomLoadingIndicators.py |
| `QCustomMediaGrid` | ✅ | ✅ | ✅ | ✅ | ✅ | 198 | Custom_Widgets/QCustomMediaGrid.py |
| `QCustomMediaTimeline` | ✅ | ✅ | ✅ | ✅ | ✅ | 608 | Custom_Widgets/QCustomMediaTimeline.py |
| `QCustomMenu` | ✅ | ✅ | ✅ | ✅ | ✅ | 181 | Custom_Widgets/QCustomMenu.py |
| `QCustomMessageStatus` | — | — | ✅ | ✅ | — | 152 | Custom_Widgets/QCustomMessageStatus.py |
| `QCustomMiniBarChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 505 | Custom_Widgets/QCustomMiniBarChart.py |
| `QCustomModal` | ✅ | ✅ | ✅ | ✅ | ✅ | 289 | Custom_Widgets/QCustomModal.py |
| `QCustomModals` | ✅ | ✅ | — | — | — | 873 | Custom_Widgets/QCustomModals.py |
| `QCustomNodeGraph` | ✅ | ✅ | ✅ | ✅ | ✅ | 1031 | Custom_Widgets/QCustomNodeGraph.py |
| `QCustomNumberInput` | ✅ | ✅ | ✅ | ✅ | ✅ | 196 | Custom_Widgets/QCustomNumberInput.py |
| `QCustomPageDots` | ✅ | ✅ | ✅ | ✅ | ✅ | 256 | Custom_Widgets/QCustomPageDots.py |
| `QCustomPagination` | ✅ | ✅ | ✅ | ✅ | ✅ | 122 | Custom_Widgets/QCustomPagination.py |
| `QCustomPaymentCard` | ✅ | ✅ | ✅ | ✅ | ✅ | 358 | Custom_Widgets/QCustomPaymentCard.py |
| `QCustomPlayerBar` | ✅ | ✅ | ✅ | ✅ | ✅ | 678 | Custom_Widgets/QCustomPlayerBar.py |
| `QCustomPopover` | ✅ | ✅ | ✅ | — | ✅ | 171 | Custom_Widgets/QCustomPopover.py |
| `QCustomProgressBars` | ✅ | ✅ | — | ✅ | — | 1 | Custom_Widgets/QCustomProgressBars.py |
| `QCustomProgressIndicator` | ✅ | ✅ | — | — | — | 375 | Custom_Widgets/QCustomProgressIndicator.py |
| `QCustomProgressRing` | ✅ | ✅ | ✅ | ✅ | ✅ | 190 | Custom_Widgets/QCustomProgressRing.py |
| `QCustomQDialog` | ✅ | ✅ | — | — | — | 492 | Custom_Widgets/QCustomQDialog.py |
| `QCustomQLabel` | ✅ | ✅ | ✅ | ✅ | ✅ | 186 | Custom_Widgets/QCustomQLabel.py |
| `QCustomQMainWindow` | ✅ | ✅ | — | ✅ | — | 484 | Custom_Widgets/QCustomQMainWindow.py |
| `QCustomQPushButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 610 | Custom_Widgets/QCustomQPushButton.py |
| `QCustomQPushButtonGroup` | ✅ | ✅ | — | — | — | 60 | Custom_Widgets/QCustomQPushButtonGroup.py |
| `QCustomQRGenerator` | ✅ | — | — | ✅ | — | 721 | Custom_Widgets/QCustomQRGenerator.py |
| `QCustomQSlider` | ✅ | ✅ | — | — | — | 47 | Custom_Widgets/QCustomQSlider.py |
| `QCustomQStackedWidget` | ✅ | ✅ | — | ✅ | — | 816 | Custom_Widgets/QCustomQStackedWidget.py |
| `QCustomQToolTip` | ✅ | ✅ | — | — | — | 662 | Custom_Widgets/QCustomQToolTip.py |
| `QCustomRadialGauge` | ✅ | ✅ | ✅ | ✅ | ✅ | 1088 | Custom_Widgets/QCustomRadialGauge.py |
| `QCustomRadioButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 268 | Custom_Widgets/QCustomRadioButton.py |
| `QCustomRadioGroup` | ✅ | ✅ | ✅ | ✅ | ✅ | 304 | Custom_Widgets/QCustomRadioGroup.py |
| `QCustomRangeSlider` | ✅ | ✅ | ✅ | ✅ | ✅ | 220 | Custom_Widgets/QCustomRangeSlider.py |
| `QCustomRating` | ✅ | ✅ | ✅ | ✅ | ✅ | 135 | Custom_Widgets/QCustomRating.py |
| `QCustomReactionBar` | — | — | ✅ | ✅ | ✅ | 202 | Custom_Widgets/QCustomReactionBar.py |
| `QCustomRichTextEditor` | ✅ | ✅ | ✅ | ✅ | ✅ | 186 | Custom_Widgets/QCustomRichTextEditor.py |
| `QCustomRulerPicker` | ✅ | ✅ | ✅ | ✅ | ✅ | 467 | Custom_Widgets/QCustomRulerPicker.py |
| `QCustomSegmentedControl` | ✅ | ✅ | ✅ | ✅ | ✅ | 146 | Custom_Widgets/QCustomSegmentedControl.py |
| `QCustomSidebar` | ✅ | ✅ | — | ✅ | — | 310 | Custom_Widgets/QCustomSidebar.py |
| `QCustomSidebarButton` | ✅ | ✅ | — | ✅ | — | 543 | Custom_Widgets/QCustomSidebarButton.py |
| `QCustomSidebarContainer` | ✅ | — | — | ✅ | — | 246 | Custom_Widgets/QCustomSidebarContainer.py |
| `QCustomSidebarLabel` | ✅ | ✅ | — | ✅ | — | 241 | Custom_Widgets/QCustomSidebarLabel.py |
| `QCustomSkeleton` | ✅ | ✅ | ✅ | ✅ | ✅ | 134 | Custom_Widgets/QCustomSkeleton.py |
| `QCustomSlideMenu` | ✅ | ✅ | — | — | — | 607 | Custom_Widgets/QCustomSlideMenu.py |
| `QCustomSparkline` | ✅ | ✅ | ✅ | — | ✅ | 290 | Custom_Widgets/QCustomSparkline.py |
| `QCustomSplitter` | ✅ | ✅ | ✅ | ✅ | ✅ | 57 | Custom_Widgets/QCustomSplitter.py |
| `QCustomStatCard` | ✅ | ✅ | ✅ | ✅ | ✅ | 160 | Custom_Widgets/QCustomStatCard.py |
| `QCustomStepper` | ✅ | ✅ | ✅ | ✅ | ✅ | 132 | Custom_Widgets/QCustomStepper.py |
| `QCustomSwitch` | ✅ | ✅ | ✅ | ✅ | ✅ | 190 | Custom_Widgets/QCustomSwitch.py |
| `QCustomTableToolbar` | ✅ | ✅ | ✅ | ✅ | ✅ | 541 | Custom_Widgets/QCustomTableToolbar.py |
| `QCustomTabWidget` | ✅ | ✅ | ✅ | ✅ | ✅ | 120 | Custom_Widgets/QCustomTabWidget.py |
| `QCustomThemeDarkLightToggle` | ✅ | ✅ | — | ✅ | — | 168 | Custom_Widgets/QCustomThemeDarkLightToggle.py |
| `QCustomTileButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 257 | Custom_Widgets/QCustomTileButton.py |
| `QCustomTimeline` | ✅ | ✅ | ✅ | ✅ | ✅ | 143 | Custom_Widgets/QCustomTimeline.py |
| `QCustomTipOverlay` | ✅ | ✅ | — | — | — | 1043 | Custom_Widgets/QCustomTipOverlay.py |
| `QCustomToast` | ✅ | ✅ | ✅ | — | ✅ | 233 | Custom_Widgets/QCustomToast.py |
| `QCustomTreeWidget` | ✅ | ✅ | ✅ | ✅ | ✅ | 102 | Custom_Widgets/QCustomTreeWidget.py |
| `QCustomTrendChip` | ✅ | ✅ | ✅ | ✅ | ✅ | 251 | Custom_Widgets/QCustomTrendChip.py |
| `QCustomTypingIndicator` | ✅ | — | ✅ | ✅ | ✅ | 144 | Custom_Widgets/QCustomTypingIndicator.py |
| `QCustomVerticalSeparator` | ✅ | — | — | ✅ | — | 117 | Custom_Widgets/QCustomVerticalSeparator.py |
| `QCustomVideoPlayer` | — | — | ✅ | ✅ | ✅ | 327 | Custom_Widgets/QCustomVideoPlayer.py |
| `QCustomVoiceMessage` | ✅ | ✅ | ✅ | ✅ | ✅ | 302 | Custom_Widgets/QCustomVoiceMessage.py |
| `QCustomWallpaper` | ✅ | ✅ | ✅ | ✅ | ✅ | 131 | Custom_Widgets/QCustomWallpaper.py |
| `QCustomWaveform` | ✅ | ✅ | ✅ | ✅ | ✅ | 457 | Custom_Widgets/QCustomWaveform.py |
| `QFlowProgressBar` | ✅ | ✅ | — | — | — | 381 | Custom_Widgets/QFlowProgressBar.py |
| `QTagEdit` | ✅ | — | — | — | — | 269 | Custom_Widgets/QCustomTagEdit.py |

## Internal / engine -- not standalone widgets (19)

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
| `QCustomComponent` | ✅ | ✅ | — | ✅ | — | 114 | Custom_Widgets/QCustomComponent.py |
| `QCustomComponentContainer` | ✅ | ✅ | — | ✅ | — | 188 | Custom_Widgets/QCustomComponentContainer.py |
| `QCustomComponentLoader` | ✅ | — | — | — | — | 678 | Custom_Widgets/QCustomComponentLoader.py |
| `QCustomHorizontalBarSeries` | ✅ | — | — | ✅ | — | 271 | Custom_Widgets/QCustomCharts/QCustomHorizontalBarSeries.py |
| `QCustomLegendManager` | — | — | — | — | — | 431 | Custom_Widgets/QCustomCharts/QCustomLegendManager.py |
| `QCustomQLineSeries` | — | — | — | — | — | 127 | Custom_Widgets/QCustomCharts/QCustomQLineSeries.py |
| `QCustomTheme` | ✅ | ✅ | — | — | — | 1786 | Custom_Widgets/QCustomTheme.py |
| `QCustomThemeList` | ✅ | ✅ | — | ✅ | — | 139 | Custom_Widgets/QCustomThemeList.py |
| `QCustomVerticalBarSeries` | ✅ | — | — | ✅ | — | 272 | Custom_Widgets/QCustomCharts/QCustomVerticalBarSeries.py |

---

## Hardening backlog (drives the gate)

### Untested user-facing widgets (8) -- highest priority
- `QCustomCoverCard` (QCustomCoverCard.py)
- `QCustomCoverFlow` (QCustomCoverFlow.py)
- `QCustomFileCard` (QCustomFileCard.py)
- `QCustomImageViewer` (QCustomImageViewer.py)
- `QCustomLinkPreview` (QCustomLinkPreview.py)
- `QCustomMessageStatus` (QCustomMessageStatus.py)
- `QCustomReactionBar` (QCustomReactionBar.py)
- `QCustomVideoPlayer` (QCustomVideoPlayer.py)

### Missing `__catalog__` entry (36)
- `AnalogGaugeWidget`
- `QCustomAnnotationWidget`
- `QCustomAreaChart`
- `QCustomBarChart`
- `QCustomCheckBox`
- `QCustomCodeEditor`
- `QCustomEmbeddedWindow`
- `QCustomEmojiPicker`
- `QCustomFlowLayout`
- `QCustomFlowWidget`
- `QCustomForm`
- `QCustomHamburgerMenu`
- `QCustomHorizontalSeparator`
- `QCustomLineChart`
- `QCustomLoadingIndicators`
- `QCustomModals`
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
- `QCustomThemeDarkLightToggle`
- `QCustomTipOverlay`
- `QCustomVerticalSeparator`
- `QFlowProgressBar`
- `QTagEdit`

### Missing example (12)
- `QCustomAnnotationWidget`
- `QCustomChatDivider`
- `QCustomHamburgerMenu`
- `QCustomHorizontalSeparator`
- `QCustomMessageStatus`
- `QCustomQRGenerator`
- `QCustomReactionBar`
- `QCustomSidebarContainer`
- `QCustomTypingIndicator`
- `QCustomVerticalSeparator`
- `QCustomVideoPlayer`
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
