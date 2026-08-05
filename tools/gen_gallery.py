#!/usr/bin/env python3
"""Generate the Docusaurus widget gallery from the manifest and the assets.

Kept as a tool rather than a one-off script because the gallery drifts
silently: it was generated once when 16 widgets had animations, and stayed
that way after 56 did, still advertising stills for widgets that move.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(os.path.dirname(ROOT), "Docs-QT-PyQt-PySide-Custom-Widgets")
SHOTS = os.path.join(DOCS, "static", "img", "showcase")
WIDGET_DOCS = os.path.join(DOCS, "docs", "01-Widgets")

#: Task-based grouping. Source folders make a bad table of contents — they put
#: a badge and a Gantt chart in the same bucket.
CATEGORIES = [
    ("Layout & containers", "Card CardStack CoverCard CoverFlow Splitter Accordion TabWidget QStackedWidget FlowWidget FlowLayout GlassFrame EmbeddedWindow EmbededWindow ComponentContainer Component ComponentLoader SidebarContainer QMainWindow Canvas LoadForm Ui_CustomMainWindow"),
    ("Navigation", "Sidebar SidebarButton SidebarLabel HamburgerMenu SlideMenu Menu HeaderNav Breadcrumbs Stepper Pagination PageDots CommandPalette TileButton Drawer"),
    ("Buttons & actions", "QPushButton QPushButtonGroup ButtonGroup ActionButton CopyButton SocialButton RainbowButton SegmentedControl Kbd"),
    ("Forms & input", "Input TextArea NumberInput ComboBox MultiSelect CheckBox RadioButton RadioGroup Switch QSlider RangeSlider DateEdit DateRangePicker ColorPicker GradientPicker ImagePicker FileDropZone TagEdit VerificationCode RulerPicker Form RichTextEditor CodeEditor AnnotationWidget Rating"),
    ("Data display", "DataTable DataTablePro TreeWidget ListRow TableToolbar AgendaList Timeline Badge Chip Avatar AvatarGroup AvatarWidget StatCard TrendChip FeaturedIcon LinkPreview FileCard PaymentCard EmptyState Skeleton BadgeWidget CardWidget DraggableWidget"),
    ("Charts & analytics", "AreaChart BarChart LineChart PieChart RadarChart Sankey GanttChart Heatmap CandlestickChart FunnelChart Beeswarm ScatterChart RadialBars RadialLines DivergingBarChart RangeBarChart NodeGraph BubbleChart DotMatrix Sparkline MiniBarChart Donut"),
    ("Gauges & meters", "ProgressRing RoundProgressBar LiquidGauge RadialGauge AnalogGaugeWidget Compass CompassDial FlowProgressBar QProgressBar ProgressIndicator"),
    ("Feedback & status", "Alert Toast Modal Modals QToolTip TipOverlay QDialog Spinner ArcLoader PerlinLoader 3CirclesLoader TypingIndicator MessageStatus Popover"),
    ("Chat & messaging", "ChatBubble ChatDivider ChatInput ChatList ChatListItem ChatThread ReactionBar VoiceMessage EmojiPicker"),
    ("Media", "VideoPlayer ImageViewer MediaGrid MediaTimeline PlayerBar Waveform Wallpaper QRGenerator Carousel"),
    ("Text & motion", "GradientText TypewriterText SparklesText NumberCounter ClockLabel QLabel HorizontalSeparator VerticalSeparator"),
    ("Theming", "ThemeDarkLightToggle"),
]


def slugFor(name):
    return re.sub(r"^QCustom|^Q", "", name).lower()


def main():
    lookup = {}
    for category, names in CATEGORIES:
        for short in names.split():
            lookup[short] = category

    rows = json.load(open(os.path.join(ROOT, "docs/design/tiering-manifest.json"),
                          encoding="utf-8"))
    rows = rows if isinstance(rows, list) else rows.get("widgets", rows)
    tier = {r["widget"]: r.get("tier") for r in rows}

    pages = sorted({os.path.splitext(f)[0] for f in os.listdir(WIDGET_DOCS)
                    if f.endswith((".md", ".mdx"))})
    groups, orphans = {}, []
    for page in pages:
        category = lookup.get(re.sub(r"^QCustom|^Q", "", page)) or lookup.get(page)
        (groups.setdefault(category, []) if category else orphans).append(page) \
            if category else orphans.append(page)
    for names in groups.values():
        names.sort()

    def thumbnail(name):
        # Prefer the animation — it is what the widget actually does.
        for candidate in ("%s.gif" % slugFor(name), "%s.png" % slugFor(name)):
            if os.path.isfile(os.path.join(SHOTS, candidate)):
                return "/img/showcase/" + candidate
        return None

    total = sum(len(v) for v in groups.values())
    pro = sum(1 for v in groups.values() for n in v if tier.get(n) == "pro-ext")
    animated = sum(1 for v in groups.values() for n in v
                   if os.path.isfile(os.path.join(SHOTS, "%s.gif" % slugFor(n))))

    # The gallery grid is raw JSX, not markdown constructs, so Docusaurus does
    # NOT rewrite its src/href with the site baseUrl the way it does for
    # markdown images. Root-absolute paths ("/img/…", "/Widgets/…") therefore
    # 404 on any project-page deployment (baseUrl "/Docs-…/"). Emitting .mdx
    # and routing every path through useBaseUrl() is the supported fix — which
    # is also why this file must NOT declare `mdx: format: md`.
    out = ["---", "title: Widget gallery", "sidebar_label: Gallery",
           "sidebar_position: 2",
           "description: Every Custom Widgets component, grouped by what you are building.",
           "---", "",
           "import useBaseUrl from '@docusaurus/useBaseUrl';", "",
           "# Widget gallery", "",
           "%d widgets, grouped by the job you are doing rather than by where "
           "they live in the source tree. %d of them animate here, showing the "
           "interaction rather than a frozen frame. %d ship in "
           "[Pro](https://customwidgets.spinncode.com/pricing/); the rest are "
           "free under GPLv3." % (total, animated, pro), ""]
    for category, _ in CATEGORIES:
        names = groups.get(category) or []
        if not names:
            continue
        out += ["## %s" % category, "", '<div className="widget-gallery">', ""]
        for name in names:
            source = thumbnail(name)
            badge = '<span className="wg-pro">PRO</span>' if tier.get(name) == "pro-ext" else ""
            media = ("<img src={useBaseUrl('%s')} alt=\"%s\" loading=\"lazy\" />" % (source, name)
                     if source else '<div className="wg-noshot">No preview</div>')
            out.append("<a className=\"wg-card\" href={useBaseUrl('/Widgets/%s')}>%s"
                       '<span className="wg-name">%s%s</span></a>' % (name, media, name, badge))
        out += ["", "</div>", ""]

    path = os.path.join(DOCS, "docs", "gallery.mdx")
    open(path, "w", encoding="utf-8").write("\n".join(out))
    stale = os.path.join(DOCS, "docs", "gallery.md")
    if os.path.isfile(stale):
        # a generated .md beside the .mdx is a doc-id collision, fatal at build
        os.remove(stale)
    print("gallery: %d widgets, %d animated, %d Pro" % (total, animated, pro))
    if orphans:
        print("NOT CATEGORISED (%d): %s" % (len(orphans), ", ".join(sorted(orphans))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
