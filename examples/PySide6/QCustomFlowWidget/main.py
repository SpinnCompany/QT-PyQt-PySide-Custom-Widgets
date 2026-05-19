"""
test_flow_widget.py
Test script for QCustomFlowWidget - Complete test suite
"""

import sys
import random
from qtpy.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QComboBox, QCheckBox, QScrollArea,
    QFrame, QMessageBox, QSpinBox, QGroupBox, QRadioButton, QSplitter,
    QTabWidget, QToolButton, QLineEdit
)
from qtpy.QtCore import Qt, QTimer, QSize
from qtpy.QtGui import QColor, QPalette, QFont

from Custom_Widgets.QCustomFlowWidget import QCustomFlowWidget


class TestWidget(QFrame):
    """A test widget with customizable appearance"""
    
    def __init__(self, text: str, color: str, size: tuple = (120, 100), parent=None):
        super().__init__(parent)
        self.setFixedSize(size[0], size[1])
        self.text = text
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                border: 2px solid rgba(255,255,255,0.8);
            }}
            QFrame:hover {{
                border: 3px solid #f39c12;
                background-color: {color};
            }}
            QLabel {{
                color: white;
                font-weight: bold;
                font-size: 14px;
                background-color: rgba(0,0,0,0.3);
                border-radius: 4px;
                padding: 4px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)
        
        self.setProperty("color", color)
        self.click_callback = None
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.click_callback:
            self.click_callback(self)
    
    def set_text(self, text):
        """Update the text of the widget"""
        self.text = text
        self.label.setText(text)


class TestFlowWidgetDemo(QMainWindow):
    """Main demo window for testing QCustomFlowWidget"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QCustomFlowWidget - Complete Test Suite")
        self.setGeometry(100, 100, 1300, 900)
        
        # Set application style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a2e;
            }
            QGroupBox {
                font-weight: bold;
                border: 2px solid #16213e;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 12px;
                color: #eee;
                background-color: #0f3460;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 8px 0 8px;
                color: #e94560;
            }
            QPushButton {
                background-color: #e94560;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #ff6b6b;
            }
            QPushButton:pressed {
                background-color: #c73e54;
            }
            QPushButton#danger {
                background-color: #dc3545;
            }
            QPushButton#danger:hover {
                background-color: #c82333;
            }
            QPushButton#warning {
                background-color: #ffc107;
                color: #1a1a2e;
            }
            QPushButton#warning:hover {
                background-color: #e0a800;
            }
            QPushButton#success {
                background-color: #28a745;
            }
            QPushButton#success:hover {
                background-color: #218838;
            }
            QLabel {
                color: #eee;
            }
            QComboBox, QSpinBox, QLineEdit {
                background-color: #1a1a2e;
                color: #eee;
                border: 1px solid #e94560;
                border-radius: 4px;
                padding: 5px;
                min-width: 100px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #e94560;
                margin-right: 5px;
            }
            QSlider::groove:horizontal {
                border: 1px solid #e94560;
                height: 6px;
                background: #1a1a2e;
                margin: 2px 0;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #e94560;
                width: 18px;
                margin: -4px 0;
                border-radius: 9px;
            }
            QSlider::handle:horizontal:hover {
                background: #ff6b6b;
            }
            QCheckBox, QRadioButton {
                color: #eee;
                spacing: 8px;
            }
            QCheckBox::indicator, QRadioButton::indicator {
                width: 16px;
                height: 16px;
            }
            QScrollArea {
                border: 2px solid #16213e;
                border-radius: 8px;
                background-color: #0f3460;
            }
            QTabWidget::pane {
                border: 1px solid #16213e;
                border-radius: 6px;
                background-color: #0f3460;
            }
            QTabBar::tab {
                background-color: #16213e;
                color: #eee;
                padding: 8px 16px;
                margin-right: 2px;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
            }
            QTabBar::tab:selected {
                background-color: #e94560;
            }
            QTabBar::tab:hover:!selected {
                background-color: #ff6b6b;
            }
        """)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Create splitter for better organization
        splitter = QSplitter(Qt.Vertical)
        main_layout.addWidget(splitter)
        
        # Create control panels
        control_panel = self.create_control_panels()
        splitter.addWidget(control_panel)
        
        # Scroll area for flow widget
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumHeight(400)
        
        # Create the flow widget
        self.flow_widget = QCustomFlowWidget()
        self.flow_widget.setStyleSheet("""
            QCustomFlowWidget {
                background-color: #0f3460;
                border-radius: 8px;
            }
        """)
        
        scroll_area.setWidget(self.flow_widget)
        splitter.addWidget(scroll_area)
        
        # Set splitter sizes
        splitter.setSizes([400, 500])
        
        # Status bar
        self.statusBar = self.statusBar()
        self.statusBar.setStyleSheet("QStatusBar { color: #eee; }")
        self.statusBar.showMessage("Ready - Test the flow widget with various controls!")
        
        # Connect signals
        flow_layout = self.flow_widget.getFlowLayout()
        if flow_layout:
            flow_layout.animationStarted.connect(
                lambda: self.statusBar.showMessage("✨ Layout animation started...")
            )
            flow_layout.animationFinished.connect(
                lambda: self.statusBar.showMessage("✅ Animation complete!", 2000)
            )
        
        # Add sample widgets
        self.add_sample_widgets()
        
        # Track widget counter
        self.update_counter()
    
    def create_control_panels(self):
        """Create organized control panels using tabs"""
        tabs = QTabWidget()
        tabs.setStyleSheet("QTabWidget::tab-bar { alignment: center; }")
        
        # Create different tab panels
        tabs.addTab(self.create_widget_management_panel(), "📦 Widget Management")
        tabs.addTab(self.create_animation_panel(), "🎬 Animation Settings")
        tabs.addTab(self.create_layout_panel(), "📐 Layout Properties")
        tabs.addTab(self.create_test_panel(), "🧪 Test Scenarios")
        tabs.addTab(self.create_info_panel(), "ℹ️ Information")
        
        return tabs
    
    def create_widget_management_panel(self):
        """Panel for adding/removing widgets"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        # Widget type selection
        type_group = QGroupBox("Widget Type")
        type_layout = QHBoxLayout(type_group)
        
        self.widget_type = QComboBox()
        self.widget_type.addItems([
            "Color Box", "Number Box", "Letter Box", "Icon Box", 
            "Button", "Custom Size", "Random Color", "Gradient Box"
        ])
        type_layout.addWidget(QLabel("Type:"))
        type_layout.addWidget(self.widget_type)
        layout.addWidget(type_group)
        
        # Add controls
        add_group = QGroupBox("Add Widgets")
        add_layout = QVBoxLayout(add_group)
        
        # Single add
        add_btn = QPushButton("➕ Add Widget")
        add_btn.clicked.connect(self.add_widget)
        add_layout.addWidget(add_btn)
        
        # Batch add
        batch_layout = QHBoxLayout()
        batch_layout.addWidget(QLabel("Batch:"))
        add_5_btn = QPushButton("5")
        add_5_btn.clicked.connect(lambda: self.add_batch_widgets(5))
        batch_layout.addWidget(add_5_btn)
        
        add_10_btn = QPushButton("10")
        add_10_btn.clicked.connect(lambda: self.add_batch_widgets(10))
        batch_layout.addWidget(add_10_btn)
        
        add_20_btn = QPushButton("20")
        add_20_btn.clicked.connect(lambda: self.add_batch_widgets(20))
        batch_layout.addWidget(add_20_btn)
        
        add_50_btn = QPushButton("50")
        add_50_btn.setObjectName("warning")
        add_50_btn.clicked.connect(lambda: self.add_batch_widgets(50))
        batch_layout.addWidget(add_50_btn)
        
        add_layout.addLayout(batch_layout)
        layout.addWidget(add_group)
        
        # Remove controls
        remove_group = QGroupBox("Remove Widgets")
        remove_layout = QVBoxLayout(remove_group)
        
        remove_last_btn = QPushButton("➖ Remove Last")
        remove_last_btn.setObjectName("danger")
        remove_last_btn.clicked.connect(self.remove_last_widget)
        remove_layout.addWidget(remove_last_btn)
        
        remove_random_btn = QPushButton("🎲 Remove Random")
        remove_random_btn.setObjectName("warning")
        remove_random_btn.clicked.connect(self.remove_random_widget)
        remove_layout.addWidget(remove_random_btn)
        
        clear_all_btn = QPushButton("🗑 Clear All")
        clear_all_btn.setObjectName("danger")
        clear_all_btn.clicked.connect(self.clear_all)
        remove_layout.addWidget(clear_all_btn)
        
        layout.addWidget(remove_group)
        
        # Widget counter
        counter_group = QGroupBox("Statistics")
        counter_layout = QVBoxLayout(counter_group)
        
        self.counter_label = QLabel("Widgets: 0")
        self.counter_label.setStyleSheet("color: #28a745; font-weight: bold; font-size: 16px;")
        self.counter_label.setAlignment(Qt.AlignCenter)
        counter_layout.addWidget(self.counter_label)
        
        # Add spacer
        counter_layout.addStretch()
        layout.addWidget(counter_group)
        
        layout.addStretch()
        return widget
    
    def create_animation_panel(self):
        """Panel for animation settings"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Enable animations
        enable_group = QGroupBox("Animation State")
        enable_layout = QVBoxLayout(enable_group)
        
        self.animate_cb = QCheckBox("Enable Animations")
        self.animate_cb.setChecked(True)
        self.animate_cb.toggled.connect(self.toggle_animations)
        enable_layout.addWidget(self.animate_cb)
        
        layout.addWidget(enable_group)
        
        # Duration control
        duration_group = QGroupBox("Duration")
        duration_layout = QVBoxLayout(duration_group)
        
        duration_slider_layout = QHBoxLayout()
        duration_slider_layout.addWidget(QLabel("Time:"))
        self.duration_slider = QSlider(Qt.Horizontal)
        self.duration_slider.setRange(0, 1000)
        self.duration_slider.setValue(300)
        self.duration_slider.valueChanged.connect(self.change_duration)
        duration_slider_layout.addWidget(self.duration_slider)
        self.duration_label = QLabel("300ms")
        duration_slider_layout.addWidget(self.duration_label)
        duration_layout.addLayout(duration_slider_layout)
        
        layout.addWidget(duration_group)
        
        # Easing curve
        easing_group = QGroupBox("Easing Curve")
        easing_layout = QVBoxLayout(easing_group)
        
        self.easing_combo = QComboBox()
        easing_curves = [
            "Linear", "InQuad", "OutQuad", "InOutQuad",
            "InCubic", "OutCubic", "InOutCubic",
            "InQuart", "OutQuart", "InOutQuart",
            "InQuint", "OutQuint", "InOutQuint",
            "InSine", "OutSine", "InOutSine",
            "InExpo", "OutExpo", "InOutExpo",
            "InCirc", "OutCirc", "InOutCirc",
            "InBack", "OutBack", "InOutBack",
            "InBounce", "OutBounce", "InOutBounce"
        ]
        self.easing_combo.addItems(easing_curves)
        self.easing_combo.setCurrentText("OutCubic")
        self.easing_combo.currentTextChanged.connect(self.change_easing)
        easing_layout.addWidget(self.easing_combo)
        
        layout.addWidget(easing_group)
        
        # Animation status
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout(status_group)
        
        self.anim_status = QLabel("● Idle")
        self.anim_status.setStyleSheet("color: #28a745; font-weight: bold; font-size: 14px;")
        self.anim_status.setAlignment(Qt.AlignCenter)
        status_layout.addWidget(self.anim_status)
        
        layout.addWidget(status_group)
        
        # Update status periodically
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_animation_status)
        self.status_timer.start(100)
        
        layout.addStretch()
        return widget
    
    def create_layout_panel(self):
        """Panel for layout properties"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        # Margin control
        margin_group = QGroupBox("Margin")
        margin_layout = QVBoxLayout(margin_group)
        
        margin_slider_layout = QHBoxLayout()
        margin_slider_layout.addWidget(QLabel("Value:"))
        self.margin_slider = QSlider(Qt.Horizontal)
        self.margin_slider.setRange(0, 50)
        self.margin_slider.setValue(15)
        self.margin_slider.valueChanged.connect(self.change_margin)
        margin_slider_layout.addWidget(self.margin_slider)
        self.margin_label = QLabel("15px")
        margin_slider_layout.addWidget(self.margin_label)
        margin_layout.addLayout(margin_slider_layout)
        
        layout.addWidget(margin_group)
        
        # Spacing control
        spacing_group = QGroupBox("Spacing")
        spacing_layout = QVBoxLayout(spacing_group)
        
        spacing_slider_layout = QHBoxLayout()
        spacing_slider_layout.addWidget(QLabel("Value:"))
        self.spacing_slider = QSlider(Qt.Horizontal)
        self.spacing_slider.setRange(0, 50)
        self.spacing_slider.setValue(15)
        self.spacing_slider.valueChanged.connect(self.change_spacing)
        spacing_slider_layout.addWidget(self.spacing_slider)
        self.spacing_label = QLabel("15px")
        spacing_slider_layout.addWidget(self.spacing_label)
        spacing_layout.addLayout(spacing_slider_layout)
        
        layout.addWidget(spacing_group)
        
        # Separate horizontal/vertical spacing
        hv_group = QGroupBox("Separate Spacing")
        hv_layout = QVBoxLayout(hv_group)
        
        # Horizontal spacing
        h_layout = QHBoxLayout()
        h_layout.addWidget(QLabel("Horizontal:"))
        self.h_spin = QSpinBox()
        self.h_spin.setRange(0, 50)
        self.h_spin.setValue(15)
        self.h_spin.valueChanged.connect(self.change_horizontal_spacing)
        h_layout.addWidget(self.h_spin)
        hv_layout.addLayout(h_layout)
        
        # Vertical spacing
        v_layout = QHBoxLayout()
        v_layout.addWidget(QLabel("Vertical:"))
        self.v_spin = QSpinBox()
        self.v_spin.setRange(0, 50)
        self.v_spin.setValue(15)
        self.v_spin.valueChanged.connect(self.change_vertical_spacing)
        v_layout.addWidget(self.v_spin)
        hv_layout.addLayout(v_layout)
        
        layout.addWidget(hv_group)
        
        # Apply button for separate spacing
        apply_btn = QPushButton("Apply Separate Spacing")
        apply_btn.clicked.connect(self.apply_separate_spacing)
        layout.addWidget(apply_btn)
        
        layout.addStretch()
        return widget
    
    def create_test_panel(self):
        """Panel for test scenarios"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        # Performance test
        perf_btn = QPushButton("⚡ Performance Test (100 widgets)")
        perf_btn.setObjectName("warning")
        perf_btn.clicked.connect(self.performance_test)
        layout.addWidget(perf_btn)
        
        # Extreme test
        extreme_btn = QPushButton("🚀 Extreme Test (500 widgets)")
        extreme_btn.setObjectName("danger")
        extreme_btn.clicked.connect(self.extreme_test)
        layout.addWidget(extreme_btn)
        
        # Reorder tests
        reorder_group = QGroupBox("Reorder Tests")
        reorder_layout = QVBoxLayout(reorder_group)
        
        shuffle_btn = QPushButton("🔄 Shuffle Widgets")
        shuffle_btn.clicked.connect(self.shuffle_widgets)
        reorder_layout.addWidget(shuffle_btn)
        
        reverse_btn = QPushButton("🔃 Reverse Order")
        reverse_btn.clicked.connect(self.reverse_order)
        reorder_layout.addWidget(reverse_btn)
        
        sort_btn = QPushButton("📊 Sort by Size")
        sort_btn.clicked.connect(self.sort_by_size)
        reorder_layout.addWidget(sort_btn)
        
        layout.addWidget(reorder_group)
        
        # Stress test
        stress_group = QGroupBox("Stress Tests")
        stress_layout = QVBoxLayout(stress_group)
        
        resize_btn = QPushButton("💪 Resize Stress Test")
        resize_btn.clicked.connect(self.stress_test)
        stress_layout.addWidget(resize_btn)
        
        rapid_add_btn = QPushButton("⚡ Rapid Add/Remove")
        rapid_add_btn.setObjectName("warning")
        rapid_add_btn.clicked.connect(self.rapid_add_remove)
        stress_layout.addWidget(rapid_add_btn)
        
        layout.addWidget(stress_group)
        
        layout.addStretch()
        return widget
    
    def create_info_panel(self):
        """Information panel with usage tips"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_text = QLabel("""
        <h2 style='color: #e94560;'>QCustomFlowWidget - Information</h2>
        
        <b>Features:</b><br>
        • Smooth animated repositioning of widgets<br>
        • Fully customizable in Qt Designer<br>
        • Supports widgets of different sizes<br>
        • Automatic wrapping to next line<br>
        • Configurable margins and spacing<br>
        • Various easing curves for animations<br>
        • Performance optimized for many widgets<br>
        
        <b>Usage Tips:</b><br>
        • Resize the window to see widgets reposition smoothly<br>
        • Try different easing curves for different animation feels<br>
        • Use batch operations to test performance<br>
        • Separate horizontal/vertical spacing for fine control<br>
        
        <b>Test Scenarios:</b><br>
        • Add many widgets to test layout performance<br>
        • Shuffle widgets to see reordering animation<br>
        • Stress test to check stability<br>
        • Try different widget sizes for complex layouts<br>
        
        <b>Properties:</b><br>
        • animationEnabled - Toggle animations on/off<br>
        • animationDuration - Set animation speed (ms)<br>
        • animationEasingCurve - Choose easing curve<br>
        • margin - Space around layout edges<br>
        • spacing - Space between widgets<br>
        • horizontalSpacing - Horizontal space between widgets<br>
        • verticalSpacing - Vertical space between widgets<br>
        """)
        info_text.setWordWrap(True)
        info_text.setStyleSheet("QLabel { background-color: #1a1a2e; padding: 15px; border-radius: 8px; }")
        
        layout.addWidget(info_text)
        layout.addStretch()
        
        return widget
    
    def add_sample_widgets(self):
        """Add initial sample widgets"""
        colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
            "#FFEAA7", "#DDA0DD", "#98D8C8", "#FF9999",
            "#FFB347", "#87CEEB", "#98FB98", "#DDA0DD"
        ]
        
        for i in range(12):
            widget = self.create_colored_widget(f"Item {i+1}", colors[i % len(colors)])
            self.flow_widget.addWidget(widget)
    
    def create_colored_widget(self, text: str, color: str, size: tuple = (120, 100)):
        """Create a colored test widget"""
        widget = TestWidget(text, color, size)
        widget.click_callback = self.on_widget_clicked
        return widget
    
    def create_gradient_widget(self, text: str):
        """Create a gradient widget"""
        widget = QFrame()
        widget.setFixedSize(140, 100)
        widget.setStyleSheet(f"""
            QFrame {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #e94560, stop:1 #ff6b6b);
                border-radius: 8px;
                border: 2px solid white;
            }}
            QLabel {{
                color: white;
                font-weight: bold;
                font-size: 14px;
                background-color: rgba(0,0,0,0.3);
                border-radius: 4px;
                padding: 4px;
            }}
        """)
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        return widget
    
    def create_number_widget(self, number: int):
        """Create a number widget"""
        widget = QFrame()
        widget.setFixedSize(100, 80)
        colors = ["#e94560", "#28a745", "#ffc107", "#17a2b8", "#6f42c1"]
        color = colors[number % len(colors)]
        widget.setStyleSheet(f"""
            QFrame {{
                background-color: {color};
                border-radius: 8px;
                border: 2px solid white;
            }}
            QLabel {{
                color: white;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }}
        """)
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        label = QLabel(str(number))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        return widget
    
    def create_letter_widget(self, letter: str):
        """Create a letter widget"""
        widget = QFrame()
        widget.setFixedSize(90, 90)
        widget.setStyleSheet("""
            QFrame {
                background-color: #dc3545;
                border-radius: 45px;
                border: 2px solid white;
            }
            QLabel {
                color: white;
                font-size: 36px;
                font-weight: bold;
                background-color: transparent;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        label = QLabel(letter)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        return widget
    
    def create_icon_widget(self, icon: str):
        """Create an icon widget"""
        widget = QFrame()
        widget.setFixedSize(100, 100)
        widget.setStyleSheet("""
            QFrame {
                background-color: #6f42c1;
                border-radius: 10px;
                border: 2px solid white;
            }
            QLabel {
                color: white;
                font-size: 48px;
                background-color: transparent;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        label = QLabel(icon)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        return widget
    
    def create_custom_size_widget(self):
        """Create a widget with random size"""
        width = random.randint(80, 200)
        height = random.randint(60, 150)
        widget = QFrame()
        widget.setFixedSize(width, height)
        widget.setStyleSheet("""
            QFrame {
                background-color: #20c997;
                border-radius: 5px;
                border: 2px solid white;
            }
            QLabel {
                color: white;
                font-weight: bold;
                background-color: rgba(0,0,0,0.3);
                padding: 5px;
                border-radius: 4px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        label = QLabel(f"{width}x{height}")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
        
        return widget
    
    def add_widget(self):
        """Add a new widget based on selected type"""
        widget_type = self.widget_type.currentText()
        count = self.flow_widget.getFlowLayout().count()
        
        if widget_type == "Color Box":
            colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7", "#DDA0DD"]
            color = colors[count % len(colors)]
            widget = self.create_colored_widget(f"Item {count+1}", color)
        elif widget_type == "Number Box":
            widget = self.create_number_widget(count + 1)
        elif widget_type == "Letter Box":
            letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
            letter = letters[count % len(letters)]
            widget = self.create_letter_widget(letter)
        elif widget_type == "Icon Box":
            icons = ["⭐", "❤️", "🎨", "🚀", "💎", "🌟", "🎯", "💡", "🔥", "✨"]
            icon = icons[count % len(icons)]
            widget = self.create_icon_widget(icon)
        elif widget_type == "Button":
            widget = QPushButton(f"Button {count+1}")
            widget.setFixedSize(120, 60)
            widget.setStyleSheet("""
                QPushButton {
                    background-color: #e94560;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #ff6b6b;
                }
            """)
            widget.clicked.connect(lambda checked, btn=widget: self.show_message(f"Button {btn.text()} clicked!"))
        elif widget_type == "Custom Size":
            widget = self.create_custom_size_widget()
        elif widget_type == "Gradient Box":
            widget = self.create_gradient_widget(f"Grad {count+1}")
        else:  # Random Color
            color = f"#{random.randint(0, 0xFFFFFF):06x}"
            widget = self.create_colored_widget(f"Random {count+1}", color)
        
        self.flow_widget.addWidget(widget)
        self.update_counter()
    
    def add_batch_widgets(self, count: int):
        """Add multiple widgets at once"""
        # Disable animations temporarily for faster addition
        animations_enabled = self.animate_cb.isChecked()
        if animations_enabled:
            self.flow_widget.animationEnabled = False
        
        for i in range(count):
            self.add_widget()
        
        # Re-enable animations
        if animations_enabled:
            self.flow_widget.animationEnabled = True
        
        self.statusBar.showMessage(f"Added {count} widgets", 2000)
    
    def remove_last_widget(self):
        """Remove the last widget"""
        flow_layout = self.flow_widget.getFlowLayout()
        if flow_layout.count() > 0:
            item = flow_layout.takeAt(flow_layout.count() - 1)
            if item and item.widget():
                item.widget().deleteLater()
            self.update_counter()
    
    def remove_random_widget(self):
        """Remove a random widget"""
        flow_layout = self.flow_widget.getFlowLayout()
        count = flow_layout.count()
        if count > 0:
            index = random.randint(0, count - 1)
            item = flow_layout.takeAt(index)
            if item and item.widget():
                item.widget().deleteLater()
            self.update_counter()
            self.statusBar.showMessage(f"Removed widget at position {index}", 2000)
    
    def clear_all(self):
        """Clear all widgets"""
        reply = QMessageBox.question(
            self, "Clear All", 
            "Are you sure you want to clear all widgets?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.flow_widget.stopAllAnimations()
            self.flow_widget.clear()
            self.update_counter()
            self.statusBar.showMessage("Cleared all widgets", 2000)
    
    def shuffle_widgets(self):
        """Shuffle the order of widgets"""
        flow_layout = self.flow_widget.getFlowLayout()
        widgets = []
        for i in range(flow_layout.count()):
            item = flow_layout.takeAt(0)
            if item and item.widget():
                widgets.append(item.widget())
        
        random.shuffle(widgets)
        
        for widget in widgets:
            flow_layout.addWidget(widget)
        
        self.update_counter()
        self.statusBar.showMessage("Widgets shuffled!", 2000)
    
    def reverse_order(self):
        """Reverse the order of widgets"""
        flow_layout = self.flow_widget.getFlowLayout()
        widgets = []
        for i in range(flow_layout.count()):
            item = flow_layout.takeAt(0)
            if item and item.widget():
                widgets.append(item.widget())
        
        widgets.reverse()
        
        for widget in widgets:
            flow_layout.addWidget(widget)
        
        self.update_counter()
        self.statusBar.showMessage("Widget order reversed!", 2000)
    
    def sort_by_size(self):
        """Sort widgets by size"""
        flow_layout = self.flow_widget.getFlowLayout()
        widgets = []
        for i in range(flow_layout.count()):
            item = flow_layout.takeAt(0)
            if item and item.widget():
                widgets.append(item.widget())
        
        # Sort by area (width * height)
        widgets.sort(key=lambda w: w.width() * w.height())
        
        for widget in widgets:
            flow_layout.addWidget(widget)
        
        self.update_counter()
        self.statusBar.showMessage("Widgets sorted by size!", 2000)
    
    def performance_test(self):
        """Test performance with many widgets"""
        reply = QMessageBox.question(
            self, "Performance Test",
            "This will add 100 widgets. Continue?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.clear_all()
            
            # Disable animations for faster addition
            animations_enabled = self.animate_cb.isChecked()
            self.flow_widget.animationEnabled = False
            
            # Add 100 widgets
            for i in range(100):
                widget = self.create_number_widget(i + 1)
                self.flow_widget.addWidget(widget)
            
            # Re-enable animations
            self.flow_widget.animationEnabled = animations_enabled
            
            self.update_counter()
            self.statusBar.showMessage("Performance test: 100 widgets added!", 3000)
    
    def extreme_test(self):
        """Extreme performance test with many widgets"""
        reply = QMessageBox.question(
            self, "Extreme Test",
            "This will add 500 widgets. Continue?\n(This may take a moment)",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.clear_all()
            
            # Disable animations for faster addition
            animations_enabled = self.animate_cb.isChecked()
            self.flow_widget.animationEnabled = False
            
            # Add 500 widgets
            for i in range(500):
                if i % 50 == 0:
                    QApplication.processEvents()  # Keep UI responsive
                widget = self.create_number_widget(i + 1)
                self.flow_widget.addWidget(widget)
            
            # Re-enable animations
            self.flow_widget.animationEnabled = animations_enabled
            
            self.update_counter()
            self.statusBar.showMessage("Extreme test: 500 widgets added!", 3000)
    
    def stress_test(self):
        """Stress test with rapid resize events"""
        self.statusBar.showMessage("Starting stress test...", 2000)
        
        original_width = self.width()
        
        def resize_loop(iteration=0):
            if iteration < 30:
                width = original_width + (100 if iteration % 2 == 0 else -100)
                self.resize(width, self.height())
                QTimer.singleShot(30, lambda: resize_loop(iteration + 1))
            else:
                self.resize(original_width, self.height())
                self.statusBar.showMessage("Stress test completed!", 2000)
        
        resize_loop()
    
    def rapid_add_remove(self):
        """Rapid add and remove test"""
        self.statusBar.showMessage("Starting rapid add/remove test...", 2000)
        
        def rapid_loop(iteration=0):
            if iteration < 50:
                if iteration % 2 == 0:
                    # Add a widget
                    widget = self.create_number_widget(iteration)
                    self.flow_widget.addWidget(widget)
                else:
                    # Remove a widget
                    flow_layout = self.flow_widget.getFlowLayout()
                    if flow_layout.count() > 0:
                        item = flow_layout.takeAt(0)
                        if item and item.widget():
                            item.widget().deleteLater()
                self.update_counter()
                QTimer.singleShot(50, lambda: rapid_loop(iteration + 1))
            else:
                self.statusBar.showMessage("Rapid add/remove test completed!", 2000)
        
        rapid_loop()
    
    def toggle_animations(self, enabled: bool):
        """Toggle animations on/off"""
        self.flow_widget.animationEnabled = enabled
        status = "enabled" if enabled else "disabled"
        self.statusBar.showMessage(f"Animations {status}", 2000)
    
    def change_duration(self, value: int):
        """Change animation duration"""
        self.flow_widget.animationDuration = value
        self.duration_label.setText(f"{value}ms")
    
    def change_easing(self, curve: str):
        """Change easing curve"""
        self.flow_widget.animationEasingCurve = curve
        self.statusBar.showMessage(f"Easing: {curve}", 2000)
    
    def change_margin(self, value: int):
        """Change layout margin"""
        self.flow_widget.margin = value
        self.margin_label.setText(f"{value}px")
    
    def change_spacing(self, value: int):
        """Change layout spacing"""
        self.flow_widget.spacing = value
        self.spacing_label.setText(f"{value}px")
    
    def change_horizontal_spacing(self, value: int):
        """Change horizontal spacing"""
        self.h_spin.setValue(value)
    
    def change_vertical_spacing(self, value: int):
        """Change vertical spacing"""
        self.v_spin.setValue(value)
    
    def apply_separate_spacing(self):
        """Apply separate horizontal and vertical spacing"""
        self.flow_widget.horizontalSpacing = self.h_spin.value()
        self.flow_widget.verticalSpacing = self.v_spin.value()
        self.statusBar.showMessage(f"Applied H:{self.h_spin.value()}px V:{self.v_spin.value()}px", 2000)
    
    def update_counter(self):
        """Update widget counter"""
        flow_layout = self.flow_widget.getFlowLayout()
        count = flow_layout.count() if flow_layout else 0
        self.counter_label.setText(f"Widgets: {count}")
        
        if count == 0:
            self.counter_label.setStyleSheet("color: #dc3545; font-weight: bold; font-size: 16px;")
        else:
            self.counter_label.setStyleSheet("color: #28a745; font-weight: bold; font-size: 16px;")
    
    def update_animation_status(self):
        """Update animation status display"""
        if self.flow_widget.isAnimating():
            self.anim_status.setText("● Animating...")
            self.anim_status.setStyleSheet("color: #ffc107; font-weight: bold; font-size: 14px;")
        else:
            self.anim_status.setText("● Idle")
            self.anim_status.setStyleSheet("color: #28a745; font-weight: bold; font-size: 14px;")
    
    def on_widget_clicked(self, widget):
        """Handle widget click"""
        text = getattr(widget, 'text', 'widget')
        self.statusBar.showMessage(f"Clicked: {text}", 2000)
        
        # Flash effect
        original_style = widget.styleSheet()
        widget.setStyleSheet(original_style + "border: 3px solid #ffc107;")
        QTimer.singleShot(200, lambda: widget.setStyleSheet(original_style))
    
    def show_message(self, message: str):
        """Show message dialog"""
        QMessageBox.information(self, "Info", message)


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show demo
    demo = TestFlowWidgetDemo()
    demo.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()