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

## Coverage summary (175 widget modules)

| Signal | Coverage |
|---|---|
| Has a test | 155/175 (89%) |
| Has an example | 147/175 (84%) |
| In `__catalog__` | 117/175 (67%) |
| Designer-registered | 133/175 (76%) |
| `.pyi` type stub | 116/175 (66%) |

Breakdown: **5** free-base-with-Pro-extension, **151** free
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
| `QCustomAreaChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 1196 | Custom_Widgets/widgets/charts/qtcharts/QCustomAreaChart.py |
| `QCustomBarChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 1103 | Custom_Widgets/widgets/charts/qtcharts/QCustomBarChart.py |
| `QCustomDataTable` | ✅ | ✅ | ✅ | ✅ | ✅ | 1824 | Custom_Widgets/widgets/data/QCustomDataTable.py |
| `QCustomLineChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 791 | Custom_Widgets/widgets/charts/qtcharts/QCustomLineChart.py |
| `QCustomPieChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 1777 | Custom_Widgets/widgets/charts/qtcharts/QCustomPieChart.py |

Pro mapping:
- `QCustomDataTable` -> DataTable Pro (SKU-1, LOCKED - built)
- `QCustomAreaChart` -> Charts Pro (SKU-2, candidate)
- `QCustomLineChart` -> Charts Pro (SKU-2, candidate)
- `QCustomBarChart` -> Charts Pro (SKU-2, candidate)
- `QCustomPieChart` -> Charts Pro (SKU-2, candidate)

## Tier: free -- standalone (151)

| Widget | Test | Example | Catalog | Designer | .pyi | LOC | Module |
|---|:--:|:--:|:--:|:--:|:--:|--:|---|
| `AnalogGaugeWidget` | ✅ | ✅ | — | ✅ | — | 1015 | Custom_Widgets/widgets/display/AnalogGaugeWidget.py |
| `Canvas` | ✅ | — | — | — | — | 547 | Custom_Widgets/widgets/data/QCustomAnnotationWidget.py |
| `LoadForm` | ✅ | ✅ | — | — | — | 873 | Custom_Widgets/widgets/display/QCustomModals.py |
| `QCustom3CirclesLoader` | ✅ | ✅ | — | — | — | 188 | Custom_Widgets/widgets/loading/QCustom3CirclesLoader.py |
| `QCustomAccordion` | ✅ | ✅ | ✅ | ✅ | ✅ | 150 | Custom_Widgets/widgets/containers/QCustomAccordion.py |
| `QCustomActionButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 152 | Custom_Widgets/widgets/buttons/QCustomActionButton.py |
| `QCustomAgendaList` | ✅ | ✅ | ✅ | ✅ | ✅ | 365 | Custom_Widgets/widgets/display/QCustomAgendaList.py |
| `QCustomAlert` | ✅ | ✅ | ✅ | ✅ | ✅ | 166 | Custom_Widgets/widgets/display/QCustomAlert.py |
| `QCustomArcLoader` | ✅ | ✅ | — | — | — | 143 | Custom_Widgets/widgets/loading/QCustomArcLoader.py |
| `QCustomAvatar` | ✅ | ✅ | ✅ | ✅ | ✅ | 297 | Custom_Widgets/widgets/display/QCustomAvatar.py |
| `QCustomAvatarGroup` | ✅ | ✅ | ✅ | ✅ | ✅ | 150 | Custom_Widgets/widgets/display/QCustomAvatarGroup.py |
| `QCustomBadge` | ✅ | ✅ | ✅ | ✅ | ✅ | 224 | Custom_Widgets/widgets/display/QCustomBadge.py |
| `QCustomBeeswarm` | ✅ | ✅ | ✅ | ✅ | ✅ | 303 | Custom_Widgets/widgets/charts/QCustomBeeswarm.py |
| `QCustomBreadcrumbs` | ✅ | ✅ | ✅ | ✅ | ✅ | 89 | Custom_Widgets/widgets/navigation/QCustomBreadcrumbs.py |
| `QCustomBubbleChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 634 | Custom_Widgets/widgets/charts/QCustomBubbleChart.py |
| `QCustomButtonGroup` | ✅ | ✅ | ✅ | — | ✅ | 160 | Custom_Widgets/widgets/input/QCustomButtonGroup.py |
| `QCustomCandlestickChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 501 | Custom_Widgets/widgets/charts/QCustomCandlestickChart.py |
| `QCustomCard` | ✅ | ✅ | ✅ | ✅ | ✅ | 118 | Custom_Widgets/widgets/display/QCustomCard.py |
| `QCustomCardStack` | ✅ | ✅ | ✅ | ✅ | ✅ | 283 | Custom_Widgets/widgets/containers/QCustomCardStack.py |
| `QCustomCarousel` | ✅ | ✅ | ✅ | ✅ | ✅ | 224 | Custom_Widgets/widgets/containers/QCustomCarousel.py |
| `QCustomChatBubble` | ✅ | ✅ | ✅ | ✅ | ✅ | 410 | Custom_Widgets/widgets/chat/QCustomChatBubble.py |
| `QCustomChatDivider` | ✅ | — | ✅ | ✅ | ✅ | 180 | Custom_Widgets/widgets/chat/QCustomChatDivider.py |
| `QCustomChatInput` | ✅ | ✅ | ✅ | ✅ | ✅ | 174 | Custom_Widgets/widgets/chat/QCustomChatInput.py |
| `QCustomChatList` | ✅ | ✅ | ✅ | ✅ | ✅ | 262 | Custom_Widgets/widgets/chat/QCustomChatList.py |
| `QCustomChatListItem` | ✅ | ✅ | ✅ | ✅ | ✅ | 401 | Custom_Widgets/widgets/chat/QCustomChatListItem.py |
| `QCustomChatThread` | ✅ | ✅ | ✅ | ✅ | ✅ | 412 | Custom_Widgets/widgets/chat/QCustomChatThread.py |
| `QCustomCheckBox` | ✅ | ✅ | — | ✅ | — | 270 | Custom_Widgets/widgets/input/QCustomCheckBox.py |
| `QCustomChip` | ✅ | ✅ | ✅ | ✅ | ✅ | 181 | Custom_Widgets/widgets/display/QCustomChip.py |
| `QCustomClockLabel` | ✅ | ✅ | ✅ | ✅ | ✅ | 89 | Custom_Widgets/widgets/display/QCustomClockLabel.py |
| `QCustomCodeEditor` | ✅ | ✅ | — | — | — | 343 | Custom_Widgets/widgets/data/QCustomCodeEditor.py |
| `QCustomColorPicker` | ✅ | ✅ | ✅ | ✅ | ✅ | 139 | Custom_Widgets/widgets/input/QCustomColorPicker.py |
| `QCustomComboBox` | ✅ | ✅ | ✅ | ✅ | ✅ | 140 | Custom_Widgets/widgets/input/QCustomComboBox.py |
| `QCustomCommandPalette` | ✅ | ✅ | ✅ | — | ✅ | 247 | Custom_Widgets/widgets/navigation/QCustomCommandPalette.py |
| `QCustomCompass` | ✅ | ✅ | ✅ | ✅ | ✅ | 374 | Custom_Widgets/widgets/charts/QCustomCompass.py |
| `QCustomCompassDial` | ✅ | ✅ | ✅ | ✅ | ✅ | 400 | Custom_Widgets/widgets/charts/QCustomCompassDial.py |
| `QCustomCopyButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 306 | Custom_Widgets/widgets/buttons/QCustomCopyButton.py |
| `QCustomCoverCard` | — | ✅ | ✅ | ✅ | ✅ | 406 | Custom_Widgets/widgets/display/QCustomCoverCard.py |
| `QCustomCoverFlow` | — | ✅ | ✅ | ✅ | ✅ | 539 | Custom_Widgets/widgets/media/QCustomCoverFlow.py |
| `QCustomDateEdit` | ✅ | ✅ | ✅ | ✅ | ✅ | 181 | Custom_Widgets/widgets/input/QCustomDateTimeEdit.py |
| `QCustomDateRangePicker` | ✅ | ✅ | ✅ | ✅ | ✅ | 413 | Custom_Widgets/widgets/input/QCustomDateRangePicker.py |
| `QCustomDivergingBarChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 412 | Custom_Widgets/widgets/charts/QCustomDivergingBarChart.py |
| `QCustomDonut` | ✅ | ✅ | ✅ | — | ✅ | 398 | Custom_Widgets/widgets/charts/QCustomDonut.py |
| `QCustomDotMatrix` | ✅ | ✅ | ✅ | ✅ | ✅ | 253 | Custom_Widgets/widgets/charts/QCustomDotMatrix.py |
| `QCustomDrawer` | ✅ | ✅ | ✅ | — | ✅ | 138 | Custom_Widgets/widgets/navigation/QCustomDrawer.py |
| `QCustomEmbeddedWindow` | ✅ | ✅ | — | — | — | 266 | Custom_Widgets/widgets/containers/QCustomEmbeddedWindow.py |
| `QCustomEmojiPicker` | ✅ | ✅ | — | — | — | 558 | Custom_Widgets/widgets/input/QCustomEmojiPicker.py |
| `QCustomEmptyState` | ✅ | ✅ | ✅ | ✅ | ✅ | 90 | Custom_Widgets/widgets/display/QCustomEmptyState.py |
| `QCustomFeaturedIcon` | ✅ | ✅ | ✅ | ✅ | ✅ | 245 | Custom_Widgets/widgets/display/QCustomFeaturedIcon.py |
| `QCustomFileCard` | — | ✅ | ✅ | ✅ | ✅ | 263 | Custom_Widgets/widgets/display/QCustomFileCard.py |
| `QCustomFileDropZone` | ✅ | ✅ | ✅ | ✅ | ✅ | 160 | Custom_Widgets/widgets/input/QCustomFileDropZone.py |
| `QCustomFlowLayout` | ✅ | ✅ | — | ✅ | — | 750 | Custom_Widgets/widgets/containers/QCustomFlowLayout.py |
| `QCustomFlowWidget` | ✅ | ✅ | — | ✅ | — | 400 | Custom_Widgets/widgets/containers/QCustomFlowWidget.py |
| `QCustomForm` | ✅ | ✅ | — | — | — | 114 | Custom_Widgets/widgets/input/QCustomForm.py |
| `QCustomFunnelChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 458 | Custom_Widgets/widgets/charts/QCustomFunnelChart.py |
| `QCustomGanttChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 361 | Custom_Widgets/widgets/charts/QCustomGanttChart.py |
| `QCustomGlassFrame` | ✅ | ✅ | ✅ | ✅ | ✅ | 529 | Custom_Widgets/widgets/containers/QCustomGlassFrame.py |
| `QCustomGradientPicker` | ✅ | ✅ | ✅ | ✅ | ✅ | 519 | Custom_Widgets/widgets/input/QCustomGradientPicker.py |
| `QCustomGradientText` | ✅ | ✅ | ✅ | ✅ | ✅ | 297 | Custom_Widgets/widgets/display/QCustomGradientText.py |
| `QCustomHamburgerMenu` | ✅ | — | — | ✅ | — | 840 | Custom_Widgets/widgets/navigation/QCustomHamburgerMenu.py |
| `QCustomHeaderNav` | ✅ | ✅ | ✅ | ✅ | ✅ | 506 | Custom_Widgets/widgets/navigation/QCustomHeaderNav.py |
| `QCustomHeatmap` | ✅ | ✅ | ✅ | ✅ | ✅ | 527 | Custom_Widgets/widgets/charts/QCustomHeatmap.py |
| `QCustomHorizontalSeparator` | ✅ | — | — | ✅ | — | 120 | Custom_Widgets/widgets/display/QCustomHorizontalSeparator.py |
| `QCustomImagePicker` | ✅ | ✅ | ✅ | ✅ | ✅ | 475 | Custom_Widgets/widgets/input/QCustomImagePicker.py |
| `QCustomImageViewer` | — | ✅ | ✅ | ✅ | ✅ | 301 | Custom_Widgets/widgets/media/QCustomImageViewer.py |
| `QCustomInput` | ✅ | ✅ | ✅ | — | ✅ | 115 | Custom_Widgets/widgets/input/QCustomInput.py |
| `QCustomKbd` | ✅ | ✅ | ✅ | ✅ | ✅ | 112 | Custom_Widgets/widgets/display/QCustomKbd.py |
| `QCustomLinkPreview` | — | ✅ | ✅ | ✅ | ✅ | 211 | Custom_Widgets/widgets/display/QCustomLinkPreview.py |
| `QCustomLiquidGauge` | ✅ | ✅ | ✅ | ✅ | ✅ | 502 | Custom_Widgets/widgets/charts/QCustomLiquidGauge.py |
| `QCustomListRow` | ✅ | ✅ | ✅ | ✅ | ✅ | 311 | Custom_Widgets/widgets/display/QCustomListRow.py |
| `QCustomLoadingIndicators` | ✅ | ✅ | — | ✅ | — | 7 | Custom_Widgets/widgets/display/QCustomLoadingIndicators.py |
| `QCustomMediaGrid` | ✅ | ✅ | ✅ | ✅ | ✅ | 198 | Custom_Widgets/widgets/media/QCustomMediaGrid.py |
| `QCustomMediaTimeline` | ✅ | ✅ | ✅ | ✅ | ✅ | 608 | Custom_Widgets/widgets/media/QCustomMediaTimeline.py |
| `QCustomMenu` | ✅ | ✅ | ✅ | ✅ | ✅ | 181 | Custom_Widgets/widgets/navigation/QCustomMenu.py |
| `QCustomMessageStatus` | — | — | ✅ | ✅ | — | 152 | Custom_Widgets/widgets/chat/QCustomMessageStatus.py |
| `QCustomMiniBarChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 505 | Custom_Widgets/widgets/charts/QCustomMiniBarChart.py |
| `QCustomModal` | ✅ | ✅ | ✅ | ✅ | ✅ | 289 | Custom_Widgets/widgets/containers/QCustomModal.py |
| `QCustomMultiSelect` | ✅ | ✅ | ✅ | ✅ | ✅ | 534 | Custom_Widgets/widgets/input/QCustomMultiSelect.py |
| `QCustomNodeGraph` | ✅ | ✅ | ✅ | ✅ | ✅ | 1031 | Custom_Widgets/widgets/data/QCustomNodeGraph.py |
| `QCustomNumberCounter` | ✅ | ✅ | ✅ | ✅ | ✅ | 265 | Custom_Widgets/widgets/display/QCustomNumberCounter.py |
| `QCustomNumberInput` | ✅ | ✅ | ✅ | ✅ | ✅ | 196 | Custom_Widgets/widgets/input/QCustomNumberInput.py |
| `QCustomPageDots` | ✅ | ✅ | ✅ | ✅ | ✅ | 256 | Custom_Widgets/widgets/display/QCustomPageDots.py |
| `QCustomPagination` | ✅ | ✅ | ✅ | ✅ | ✅ | 122 | Custom_Widgets/widgets/navigation/QCustomPagination.py |
| `QCustomPaymentCard` | ✅ | ✅ | ✅ | ✅ | ✅ | 358 | Custom_Widgets/widgets/display/QCustomPaymentCard.py |
| `QCustomPerlinLoader` | ✅ | ✅ | — | — | — | 143 | Custom_Widgets/widgets/loading/QCustomPerlinLoader.py |
| `QCustomPlayerBar` | ✅ | ✅ | ✅ | ✅ | ✅ | 678 | Custom_Widgets/widgets/media/QCustomPlayerBar.py |
| `QCustomPopover` | ✅ | ✅ | ✅ | — | ✅ | 171 | Custom_Widgets/widgets/containers/QCustomPopover.py |
| `QCustomProgressBars` | ✅ | ✅ | — | ✅ | — | 1 | Custom_Widgets/widgets/display/QCustomProgressBars.py |
| `QCustomProgressIndicator` | ✅ | ✅ | — | — | — | 375 | Custom_Widgets/widgets/display/QCustomProgressIndicator.py |
| `QCustomProgressRing` | ✅ | ✅ | ✅ | ✅ | ✅ | 190 | Custom_Widgets/widgets/display/QCustomProgressRing.py |
| `QCustomQDialog` | ✅ | ✅ | — | — | — | 492 | Custom_Widgets/widgets/containers/QCustomQDialog.py |
| `QCustomQLabel` | ✅ | ✅ | ✅ | ✅ | ✅ | 186 | Custom_Widgets/widgets/display/QCustomQLabel.py |
| `QCustomQMainWindow` | ✅ | ✅ | — | ✅ | — | 494 | Custom_Widgets/widgets/containers/QCustomQMainWindow.py |
| `QCustomQProgressBar` | ✅ | ✅ | — | ✅ | — | 208 | Custom_Widgets/widgets/loading/QCustomQProgressBar.py |
| `QCustomQPushButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 610 | Custom_Widgets/widgets/buttons/QCustomQPushButton.py |
| `QCustomQPushButtonGroup` | ✅ | ✅ | — | — | — | 60 | Custom_Widgets/widgets/buttons/QCustomQPushButtonGroup.py |
| `QCustomQRGenerator` | ✅ | — | — | ✅ | — | 722 | Custom_Widgets/widgets/display/QCustomQRGenerator.py |
| `QCustomQSlider` | ✅ | ✅ | — | — | — | 47 | Custom_Widgets/widgets/input/QCustomQSlider.py |
| `QCustomQStackedWidget` | ✅ | ✅ | — | ✅ | — | 817 | Custom_Widgets/widgets/containers/QCustomQStackedWidget.py |
| `QCustomQToolTip` | ✅ | ✅ | — | — | — | 662 | Custom_Widgets/widgets/display/QCustomQToolTip.py |
| `QCustomRadarChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 576 | Custom_Widgets/widgets/charts/QCustomRadarChart.py |
| `QCustomRadialBars` | ✅ | ✅ | ✅ | ✅ | ✅ | 423 | Custom_Widgets/widgets/charts/QCustomRadialBars.py |
| `QCustomRadialGauge` | ✅ | ✅ | ✅ | ✅ | ✅ | 1088 | Custom_Widgets/widgets/charts/QCustomRadialGauge.py |
| `QCustomRadialLines` | ✅ | ✅ | ✅ | ✅ | ✅ | 531 | Custom_Widgets/widgets/charts/QCustomRadialLines.py |
| `QCustomRadioButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 268 | Custom_Widgets/widgets/input/QCustomRadioButton.py |
| `QCustomRadioGroup` | ✅ | ✅ | ✅ | ✅ | ✅ | 304 | Custom_Widgets/widgets/input/QCustomRadioGroup.py |
| `QCustomRainbowButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 319 | Custom_Widgets/widgets/buttons/QCustomRainbowButton.py |
| `QCustomRangeBarChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 484 | Custom_Widgets/widgets/charts/QCustomRangeBarChart.py |
| `QCustomRangeSlider` | ✅ | ✅ | ✅ | ✅ | ✅ | 220 | Custom_Widgets/widgets/input/QCustomRangeSlider.py |
| `QCustomRating` | ✅ | ✅ | ✅ | ✅ | ✅ | 135 | Custom_Widgets/widgets/input/QCustomRating.py |
| `QCustomReactionBar` | — | — | ✅ | ✅ | ✅ | 202 | Custom_Widgets/widgets/chat/QCustomReactionBar.py |
| `QCustomRichTextEditor` | ✅ | ✅ | ✅ | ✅ | ✅ | 186 | Custom_Widgets/widgets/data/QCustomRichTextEditor.py |
| `QCustomRoundProgressBar` | ✅ | ✅ | — | ✅ | — | 228 | Custom_Widgets/widgets/progressbars/QCustomRoundProgressBar.py |
| `QCustomRulerPicker` | ✅ | ✅ | ✅ | ✅ | ✅ | 467 | Custom_Widgets/widgets/input/QCustomRulerPicker.py |
| `QCustomSankey` | ✅ | ✅ | ✅ | ✅ | ✅ | 526 | Custom_Widgets/widgets/charts/QCustomSankey.py |
| `QCustomScatterChart` | ✅ | ✅ | ✅ | ✅ | ✅ | 598 | Custom_Widgets/widgets/charts/QCustomScatterChart.py |
| `QCustomSegmentedControl` | ✅ | ✅ | ✅ | ✅ | ✅ | 146 | Custom_Widgets/widgets/input/QCustomSegmentedControl.py |
| `QCustomSidebar` | ✅ | ✅ | — | ✅ | — | 311 | Custom_Widgets/widgets/navigation/QCustomSidebar.py |
| `QCustomSidebarButton` | ✅ | ✅ | — | ✅ | — | 544 | Custom_Widgets/widgets/navigation/QCustomSidebarButton.py |
| `QCustomSidebarContainer` | ✅ | — | — | ✅ | — | 247 | Custom_Widgets/widgets/navigation/QCustomSidebarContainer.py |
| `QCustomSidebarLabel` | ✅ | ✅ | — | ✅ | — | 242 | Custom_Widgets/widgets/navigation/QCustomSidebarLabel.py |
| `QCustomSkeleton` | ✅ | ✅ | ✅ | ✅ | ✅ | 134 | Custom_Widgets/widgets/display/QCustomSkeleton.py |
| `QCustomSlideMenu` | ✅ | ✅ | — | — | — | 607 | Custom_Widgets/widgets/navigation/QCustomSlideMenu.py |
| `QCustomSocialButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 336 | Custom_Widgets/widgets/buttons/QCustomSocialButton.py |
| `QCustomSparklesText` | ✅ | ✅ | ✅ | ✅ | ✅ | 303 | Custom_Widgets/widgets/display/QCustomSparklesText.py |
| `QCustomSparkline` | ✅ | ✅ | ✅ | — | ✅ | 290 | Custom_Widgets/widgets/charts/QCustomSparkline.py |
| `QCustomSpinner` | ✅ | ✅ | — | — | — | 79 | Custom_Widgets/widgets/loading/QCustomSpinner.py |
| `QCustomSplitter` | ✅ | ✅ | ✅ | ✅ | ✅ | 57 | Custom_Widgets/widgets/containers/QCustomSplitter.py |
| `QCustomStatCard` | ✅ | ✅ | ✅ | ✅ | ✅ | 160 | Custom_Widgets/widgets/display/QCustomStatCard.py |
| `QCustomStepper` | ✅ | ✅ | ✅ | ✅ | ✅ | 132 | Custom_Widgets/widgets/navigation/QCustomStepper.py |
| `QCustomSwitch` | ✅ | ✅ | ✅ | ✅ | ✅ | 190 | Custom_Widgets/widgets/input/QCustomSwitch.py |
| `QCustomTableToolbar` | ✅ | ✅ | ✅ | ✅ | ✅ | 541 | Custom_Widgets/widgets/data/QCustomTableToolbar.py |
| `QCustomTabWidget` | ✅ | ✅ | ✅ | ✅ | ✅ | 120 | Custom_Widgets/widgets/navigation/QCustomTabWidget.py |
| `QCustomTextArea` | ✅ | ✅ | ✅ | ✅ | ✅ | 344 | Custom_Widgets/widgets/input/QCustomTextArea.py |
| `QCustomThemeDarkLightToggle` | ✅ | ✅ | — | ✅ | — | 169 | Custom_Widgets/widgets/buttons/QCustomThemeDarkLightToggle.py |
| `QCustomTileButton` | ✅ | ✅ | ✅ | ✅ | ✅ | 257 | Custom_Widgets/widgets/buttons/QCustomTileButton.py |
| `QCustomTimeline` | ✅ | ✅ | ✅ | ✅ | ✅ | 143 | Custom_Widgets/widgets/display/QCustomTimeline.py |
| `QCustomTipOverlay` | ✅ | ✅ | — | — | — | 1043 | Custom_Widgets/widgets/display/QCustomTipOverlay.py |
| `QCustomToast` | ✅ | ✅ | ✅ | — | ✅ | 233 | Custom_Widgets/widgets/display/QCustomToast.py |
| `QCustomTreeWidget` | ✅ | ✅ | ✅ | ✅ | ✅ | 102 | Custom_Widgets/widgets/data/QCustomTreeWidget.py |
| `QCustomTrendChip` | ✅ | ✅ | ✅ | ✅ | ✅ | 251 | Custom_Widgets/widgets/display/QCustomTrendChip.py |
| `QCustomTypewriterText` | ✅ | ✅ | ✅ | ✅ | ✅ | 326 | Custom_Widgets/widgets/display/QCustomTypewriterText.py |
| `QCustomTypingIndicator` | ✅ | — | ✅ | ✅ | ✅ | 144 | Custom_Widgets/widgets/chat/QCustomTypingIndicator.py |
| `QCustomVerificationCode` | ✅ | ✅ | ✅ | ✅ | ✅ | 430 | Custom_Widgets/widgets/input/QCustomVerificationCode.py |
| `QCustomVerticalSeparator` | ✅ | — | — | ✅ | — | 118 | Custom_Widgets/widgets/display/QCustomVerticalSeparator.py |
| `QCustomVideoPlayer` | — | — | ✅ | ✅ | ✅ | 327 | Custom_Widgets/widgets/media/QCustomVideoPlayer.py |
| `QCustomVoiceMessage` | ✅ | ✅ | ✅ | ✅ | ✅ | 302 | Custom_Widgets/widgets/media/QCustomVoiceMessage.py |
| `QCustomWallpaper` | ✅ | ✅ | ✅ | ✅ | ✅ | 131 | Custom_Widgets/widgets/media/QCustomWallpaper.py |
| `QCustomWaveform` | ✅ | ✅ | ✅ | ✅ | ✅ | 457 | Custom_Widgets/widgets/charts/QCustomWaveform.py |
| `QFlowProgressBar` | ✅ | ✅ | — | — | — | 381 | Custom_Widgets/widgets/display/QFlowProgressBar.py |
| `QTagEdit` | ✅ | — | — | — | — | 269 | Custom_Widgets/widgets/input/QCustomTagEdit.py |
| `Ui_CustomMainWindow` | — | — | — | — | — | 40 | Custom_Widgets/components/uis/QCustomQMainWindow_ui.py |

## Internal / engine -- not standalone widgets (19)

Chart-subsystem engine + shared helpers. Ship as free library internals; no
separate tier. (Most surface through the public chart types above.)

| Widget | Test | Example | Catalog | Designer | .pyi | LOC | Module |
|---|:--:|:--:|:--:|:--:|:--:|--:|---|
| `QCustomBarChartBase` | — | — | — | — | — | 1932 | Custom_Widgets/widgets/charts/qtcharts/QCustomBarChartBase.py |
| `QCustomChartBase` | — | — | — | — | — | 379 | Custom_Widgets/widgets/charts/qtcharts/QCustomChartBase.py |
| `QCustomChartConstants` | ✅ | — | — | — | — | 372 | Custom_Widgets/widgets/charts/qtcharts/QCustomChartConstants.py |
| `QCustomChartDataManager` | — | — | — | — | — | 605 | Custom_Widgets/widgets/charts/qtcharts/QCustomChartDataManager.py |
| `QCustomChartExporter` | — | — | — | — | — | 575 | Custom_Widgets/widgets/charts/qtcharts/QCustomChartExporter.py |
| `QCustomChartProps` | — | — | — | — | — | 485 | Custom_Widgets/widgets/charts/qtcharts/QCustomChartProps.py |
| `QCustomChartThemeManager` | — | — | — | — | — | 444 | Custom_Widgets/widgets/charts/qtcharts/QCustomChartThemeManager.py |
| `QCustomChartToolbar` | — | — | — | — | — | 511 | Custom_Widgets/widgets/charts/qtcharts/QCustomChartToolbar.py |
| `QCustomChartTooltip` | — | — | — | — | — | 415 | Custom_Widgets/widgets/charts/qtcharts/QCustomChartTooltip.py |
| `QCustomChartView` | — | — | — | — | — | 483 | Custom_Widgets/widgets/charts/qtcharts/QCustomChartView.py |
| `QCustomComponent` | ✅ | ✅ | — | ✅ | — | 115 | Custom_Widgets/widgets/containers/QCustomComponent.py |
| `QCustomComponentContainer` | ✅ | ✅ | — | ✅ | — | 189 | Custom_Widgets/widgets/containers/QCustomComponentContainer.py |
| `QCustomComponentLoader` | ✅ | — | — | — | — | 678 | Custom_Widgets/widgets/containers/QCustomComponentLoader.py |
| `QCustomHorizontalBarSeries` | ✅ | — | — | ✅ | — | 271 | Custom_Widgets/widgets/charts/qtcharts/QCustomHorizontalBarSeries.py |
| `QCustomLegendManager` | — | — | — | — | — | 431 | Custom_Widgets/widgets/charts/qtcharts/QCustomLegendManager.py |
| `QCustomQLineSeries` | — | — | — | — | — | 127 | Custom_Widgets/widgets/charts/qtcharts/QCustomQLineSeries.py |
| `QCustomTheme` | ✅ | ✅ | — | — | — | 1787 | Custom_Widgets/theming/QCustomTheme.py |
| `QCustomThemeList` | ✅ | ✅ | — | ✅ | — | 140 | Custom_Widgets/widgets/input/QCustomThemeList.py |
| `QCustomVerticalBarSeries` | ✅ | — | — | ✅ | — | 272 | Custom_Widgets/widgets/charts/qtcharts/QCustomVerticalBarSeries.py |

---

## Hardening backlog (drives the gate)

### Untested user-facing widgets (9) -- highest priority
- `QCustomCoverCard` (QCustomCoverCard.py)
- `QCustomCoverFlow` (QCustomCoverFlow.py)
- `QCustomFileCard` (QCustomFileCard.py)
- `QCustomImageViewer` (QCustomImageViewer.py)
- `QCustomLinkPreview` (QCustomLinkPreview.py)
- `QCustomMessageStatus` (QCustomMessageStatus.py)
- `QCustomReactionBar` (QCustomReactionBar.py)
- `QCustomVideoPlayer` (QCustomVideoPlayer.py)
- `Ui_CustomMainWindow` (QCustomQMainWindow_ui.py)

### Missing `__catalog__` entry (39)
- `AnalogGaugeWidget`
- `Canvas`
- `LoadForm`
- `QCustom3CirclesLoader`
- `QCustomArcLoader`
- `QCustomCheckBox`
- `QCustomCodeEditor`
- `QCustomEmbeddedWindow`
- `QCustomEmojiPicker`
- `QCustomFlowLayout`
- `QCustomFlowWidget`
- `QCustomForm`
- `QCustomHamburgerMenu`
- `QCustomHorizontalSeparator`
- `QCustomLoadingIndicators`
- `QCustomPerlinLoader`
- `QCustomProgressBars`
- `QCustomProgressIndicator`
- `QCustomQDialog`
- `QCustomQMainWindow`
- `QCustomQProgressBar`
- `QCustomQPushButtonGroup`
- `QCustomQRGenerator`
- `QCustomQSlider`
- `QCustomQStackedWidget`
- `QCustomQToolTip`
- `QCustomRoundProgressBar`
- `QCustomSidebar`
- `QCustomSidebarButton`
- `QCustomSidebarContainer`
- `QCustomSidebarLabel`
- `QCustomSlideMenu`
- `QCustomSpinner`
- `QCustomThemeDarkLightToggle`
- `QCustomTipOverlay`
- `QCustomVerticalSeparator`
- `QFlowProgressBar`
- `QTagEdit`
- `Ui_CustomMainWindow`

### Missing example (13)
- `Canvas`
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
- `Ui_CustomMainWindow`

## Per-widget hardening checklist (fill during the pass)

Before a tier is locked, each user-facing widget needs:
- [ ] Test present & passing (headless)
- [ ] Example present & runs
- [ ] `__catalog__` entry (name, group, capabilities, edition)
- [ ] `.pyi` stub for IDE/Designer typing
- [ ] Stability: no crash on empty/huge/edge inputs; theme-switch safe
- [ ] Security: no eval/exec/network/file-write on untrusted input; QSS-injection safe
- [ ] Tier ratified (free / free-to-Pro / internal)
