# JSON FOR READING THE JSON STYLESHEET
import json
import os
import re
import sys
import warnings

from qtpy.QtCore import QThreadPool, QSettings, Qt
from qtpy.QtGui import QColor, QFontDatabase, QIcon, QFont
from qtpy.QtWidgets import QGraphicsDropShadowEffect, QPushButton, QSizeGrip

from Custom_Widgets.FileMonitor import QSsFileMonitor
from Custom_Widgets.QCustomQPushButtonGroup import QCustomQPushButtonGroup
from Custom_Widgets.QCustomQPushButton import applyAnimationThemeStyle, applyButtonShadow, iconify, applyCustomAnimationThemeStyle, applyStylesFromColor
from Custom_Widgets.QPropertyAnimation import returnAnimationEasingCurve, returnQtDirection

from Custom_Widgets.Log import *
from Custom_Widgets.Utils import replace_url_prefix, SharedData, is_in_designer

## Read JSON stylesheet
def loadJsonStyle(self, update = False, **jsonFiles):
    # self.ui = ui
    self.jsonStyleSheets = []  # List to store loaded JSON style sheets
    self.jsonStyleData = {}

    if not jsonFiles:
        json_file_paths = ["style.json", "json/style.json", "jsonstyles/style.json", "json-styles/style.json"]
        for file_path in json_file_paths:
            if os.path.isfile(file_path):
                with open(file_path) as file:
                    data = json.load(file)
                    self.jsonStyleData.update(data)  # Update existing data with new data
                    self.jsonStyleSheets.append(file_path)

    else:
        for file_path in jsonFiles.get('jsonFiles', []):
            # Check if the path is absolute
            if not os.path.isabs(file_path):
                # If the path is relative, construct the absolute path based on the current script's directory
                current_script = os.path.dirname(os.path.realpath(sys.argv[0]))
                jsonFile = os.path.abspath(os.path.join(os.getcwd(), file_path))
                # jsonFile = os.path.abspath(os.path.join(json_file_path, file_path))
            else:
                # If the path is already absolute, use it as is
                jsonFile = file_path

            # Check if the file exists
            if os.path.isfile(jsonFile):
                try:
                    with open(jsonFile) as file:
                        data = json.load(file)
                        # APPLY JSON STYLESHEET
                        # self = QMainWindow class
                        # self.ui = Ui_MainWindow / user interface class
                        self.jsonStyleData.update(data)  # Update existing data with new data
                        self.jsonStyleSheets.append(file_path)
                except Exception as e:
                    logError(f"Error loading your JSON files: '{jsonFile}' could not be read. Exception: {e}")
            else:
                logError(f"Error loading your JSON files: '{jsonFile}' does not exist")

    applyJsonStyle(self, update = update)

## Apply JSon stylesheet
def applyJsonStyle(self, update: bool = False):
    data = self.jsonStyleData

    configure_custom_widgets(self, data, update)
    configure_settings(self, data, update)

    configure_cards(self, data, update)
    configure_button_group(self, data, update)
    configure_analog_gauge(self, data, update)
    configure_slide_menu(self, data, update)
    configure_main_window(self, data, update)
    configure_push_button(self, data, update)
    configure_custom_stacked_widget(self, data, update)
    configure_custom_progress_indicator(self, data, update)
    configure_custom_check_box(self, data, update)

def configure_custom_widgets(self, data, update: bool = False):
    ## Show logs
    if "ShowLogs" in data:
        if data["ShowLogs"]:
            # Show Logs
            self.showCustomWidgetsLogs = True
        else:
            # Hide Logs
            self.showCustomWidgetsLogs = False

        if self.showCustomWidgetsLogs:
            setupLogger(self = self)

    ## Live QSS compiler
    if "LiveCompileQss" in data:
        if data["LiveCompileQss"]:
            if not hasattr(self, 'qss_watcher') and not hasattr(self, 'liveCompileQss'):
                self.liveCompileQss = True
                try:
                    QSsFileMonitor.start_qss_file_listener(self)
                except Exception as e:
                    logError("Failed to start live file listener: "+str(e))
            
        else:
            self.liveCompileQss = False
            # QSsFileMonitor.stop_qss_file_listener(self)
            logInfo("File listener disabled")

    # Generate missing icons including qt designer icons
    if "CheckForMissingicons" in data:
        self.themeEngine.checkForMissingicons = data["CheckForMissingicons"]       

def configure_settings(self, data, update: bool = False):
    ## QSETTINGS
    if "QSettings" in data:
        settings = data['QSettings']  # Directly access the dictionary
        if "AppSettings" in settings:
            appSettings = settings['AppSettings']
            if "OrginizationName" in appSettings and len(str(appSettings["OrginizationName"])) > 0:
                self.themeEngine.orginazationName = str(appSettings["OrginizationName"])
            else:
                self.themeEngine.orginazationName = ""

            if "ApplicationName" in appSettings and len(str(appSettings["ApplicationName"])) > 0:
                self.themeEngine.applicationName = str(appSettings["ApplicationName"])
            else:
                self.themeEngine.applicationName = ""

            if "OrginizationDormain" in appSettings and len(str(appSettings["OrginizationDormain"])) > 0:
                self.themeEngine.orginazationDomain = str(appSettings["OrginizationDormain"]).replace(" ", "")
            else:
                self.themeEngine.orginazationDomain = ""

        if "ThemeSettings" in settings:
            setngs = QSettings()
            
            if "QtDesignerIconsColor" in settings['ThemeSettings']:
                designer_icons_color = settings['ThemeSettings']['QtDesignerIconsColor']
                if len(str(designer_icons_color)) > 0:
                    self.themeEngine.designerIconsColor = designer_icons_color

            if "CustomThemes" in settings['ThemeSettings']: #NOTE: Updated from "CustomTheme" to "CustomThemes"
                customThemes = settings['ThemeSettings']['CustomThemes']
                for customTheme in customThemes:
                    if "Theme-name" in customTheme and len(str(customTheme['Theme-name'])) > 0:
                        theme_name = str(customTheme['Theme-name'])

                        # Retrieve color values using the helper function
                        background_color = customTheme.get("Background-color", "")
                        text_color = customTheme.get("Text-color", "")
                        accent_color = customTheme.get("Accent-color", "")
                        icons_color = customTheme.get("Icons-color", "")

                        # Determine if this is the default theme
                        is_default_theme = customTheme.get("Default-Theme", False)
                        if is_default_theme and setngs.contains("THEME") and setngs.contains("THEME") is not None:
                            default_theme = False
                        else:
                            default_theme = is_default_theme

                        # Determine if new icons should be created
                        create_new_icons = customTheme.get("Create-icons", True)

                        # Create a new theme with retrieved values
                        theme = self.themeEngine.createNewTheme(
                            theme_name,        # Use the retrieved theme name
                            background_color,  # Background color
                            text_color,       # Text color
                            accent_color,     # Accent color
                            icons_color,      # Icons color
                            create_new_icons,
                            default_theme,    # Set as default theme if needed
                            customTheme.get("Other-variables", {})  # Add other variables
                        )
                    
                self.themeEngine.themesRead = True    

            if "Fonts" in settings["ThemeSettings"]:
                fonts_data = settings["ThemeSettings"]["Fonts"]
                # Load fonts from "LoadFonts"
                if "LoadFonts" in fonts_data:
                    for font in fonts_data["LoadFonts"]:
                        font_name = font.get("name", "")
                        font_path = font.get("path", "")
                        if font_name and font_path:
                            font_path_abs = os.path.join(os.getcwd(), font_path)  # Construct absolute path
                            if os.path.isfile(font_path_abs):
                                font_id = QFontDatabase.addApplicationFont(font_path_abs)
                                if font_id == -1:
                                    print(f"Error loading font: {font_name} from {font_path}")
                                else:
                                    # Set the font name to the font loaded
                                    self._fontName = QFontDatabase.applicationFontFamilies(font_id)[0]
                            else:
                                print(f"Font file does not exist: {font_path}")
                
                # Set the default font
                if "DefaultFont" in fonts_data:
                    default_font_name = fonts_data["DefaultFont"].get("name", "")

                    if default_font_name:
                        # Check if the default font exists in the font database
                        if default_font_name in QFontDatabase.families():  # Changed here
                            self._fontName = QFont(default_font_name)
                            self.setFont(self._fontName)
                        
                              
        if update:
            # create theme color variables(check Qss\scss\_variables.scss file inside your project folder)
            self.themeEngine.createVariables()

def configure_cards(self, data, update: bool = False):
    ## QCARDS
    if "QCard" in data:
        for QCard in data['QCard']:
            if "cards" in QCard:
                for card in QCard['cards']:

                    if "shadow" in QCard:
                        cardWidget = get_widget_from_path(self, str(card))
                        if cardWidget:   
                            effect = QGraphicsDropShadowEffect(cardWidget)
                            for shadow in QCard['shadow']:
                                if "color" in shadow and len(str(shadow["color"])) > 0:
                                    effect.setColor(QColor(self.themeEngine.getThemeVariableValue(str(shadow["color"]))))
                                else:
                                    effect.setColor(QColor(0,0,0,0))
                                if "blurRadius" in shadow and int(shadow["blurRadius"]) > 0:
                                    effect.setBlurRadius(int(shadow["blurRadius"]))
                                else:
                                    effect.setBlurRadius(0)
                                if "xOffset" in shadow and int(shadow["xOffset"]) > 0:
                                    effect.setXOffset(int(shadow["xOffset"]))
                                else:
                                    effect.setXOffset(0)
                                if "yOffset" in shadow and int(shadow["yOffset"]) > 0:
                                    effect.setYOffset(int(shadow["yOffset"]))
                                else:
                                    effect.setYOffset(0)

                            cardWidget.setGraphicsEffect(effect)

def configure_button_group(self, data, update: bool = False):
    ## BUTTON GROUPS
    # Add Class To PushButtons
    QPushButton.getButtonGroup = QCustomQPushButtonGroup.getButtonGroup
    QPushButton.getButtonGroupActiveStyle = QCustomQPushButtonGroup.getButtonGroupActiveStyle
    QPushButton.getButtonGroupNotActiveStyle = QCustomQPushButtonGroup.getButtonGroupNotActiveStyle
    QPushButton.getButtonGroupButtons = QCustomQPushButtonGroup.getButtonGroupButtons
    QPushButton.getButtonGroupActiveStyle = QCustomQPushButtonGroup.getButtonGroupActiveStyle
    QPushButton.setButtonGroupActiveStyle = QCustomQPushButtonGroup.setButtonGroupActiveStyle

    if "QPushButtonGroup" in data:
        grp_count = 0  # Initialize group counter
        QPushButtonGroups = data["QPushButtonGroup"]
        
        for QPushButtonGroup in QPushButtonGroups:  # Iterate over each group in QPushButtonGroup
            grp_count += 1  # Increment the group count for each group
            
            if "Buttons" in QPushButtonGroup:
                for button in QPushButtonGroup["Buttons"]:
                    btn = get_widget_from_path(self, str(button))
                    if btn:
                        btn.groupParent = self

                        # Set 'active' attribute based on 'ActiveButton'
                        if not hasattr(btn, "active"):
                            if "ActiveButton" in QPushButtonGroup and QPushButtonGroup["ActiveButton"] == button:
                                btn.active = True
                            else:
                                btn.active = False

                        # Ensure the button is either a 'QPushButton' or 'QPushButtonThemed'
                        if not btn.metaObject().className() in ["QPushButton", "QPushButtonThemed", "QCustomSidebarButton"]:
                            if not is_in_designer(self):
                                raise Exception(f"Error: {button} is not a QPushButton object.")
                            else:
                                return
                        
                        # Set the button's group number
                        setattr(btn, "group", grp_count)

                        # Create a list for buttons in this group if it doesn't exist
                        if not hasattr(self, f"group_btns_{grp_count}"):
                            setattr(self, f"group_btns_{grp_count}", [])
                        
                        # Add the button to the group's button list
                        getattr(self, f"group_btns_{grp_count}").append(btn)

                        
                        btn.clicked.connect(self.checkButtonGroup)
                        
                    else:
                        if not is_in_designer(self):
                            warnings.warn(f"Warning: Button named {button} was not found.", RuntimeWarning)

            # Handle the common styles for all buttons in the current group
            activeStyle = ""
            notActiveStyle = ""
            if "Style" in QPushButtonGroup:
                try:
                    style = QPushButtonGroup["Style"][0]  # Styles are in the first dictionary in the list
                except:
                    style = QPushButtonGroup["Style"]

                # Process the 'Active' and 'NotActive' styles for the group
                if "Active" in style:
                    activeStyle = style["Active"]

                if "NotActive" in style:
                    notActiveStyle = style["NotActive"]

                # Store the styles for this group
                setattr(self, f"group_active_{grp_count}", activeStyle)
                setattr(self, f"group_not_active_{grp_count}", notActiveStyle)

                try:
                    self.checkButtonGroup(button=btn)
                except:
                    pass

def configure_analog_gauge(self, data, update: bool = False):
    ## ANALOG GAUGE WIDGET
    if "AnalogGaugeWidget" in data:
        for AnalogGaugeWidget in data['AnalogGaugeWidget']:
            if "name" in AnalogGaugeWidget and len(str(AnalogGaugeWidget["name"])) > 0:
                gaugeWidget = get_widget_from_path(self, str(AnalogGaugeWidget["name"]))
                if gaugeWidget:

                    if not gaugeWidget.metaObject().className() == "AnalogGaugeWidget":
                        if not is_in_designer(self):
                            raise Exception("Error: "+str(AnalogGaugeWidget["name"])+" is not a AnalogGaugeWidget object")
                        else:
                            return

                    if "units" in AnalogGaugeWidget and len(str(AnalogGaugeWidget["units"])) > 0:
                        # Set gauge units
                        gaugeWidget.units = str(AnalogGaugeWidget["units"])

                    if "minValue" in AnalogGaugeWidget:
                        # Set gauge min value
                        gaugeWidget.minValue = int(AnalogGaugeWidget["minValue"])


                    if "maxValue" in AnalogGaugeWidget:
                        # Set gauge max value
                        gaugeWidget.maxValue = int(AnalogGaugeWidget["maxValue"])

                    if "scalaCount" in AnalogGaugeWidget:
                        # Set scala count
                        gaugeWidget.scalaCount = int(AnalogGaugeWidget["scalaCount"])

                    if "startValue" in AnalogGaugeWidget:
                        # Set start value
                        gaugeWidget.updateValue(int(AnalogGaugeWidget["startValue"]))

                    if "gaugeTheme" in AnalogGaugeWidget:
                        # Set gauge theme
                        gaugeWidget.setGaugeTheme(int(AnalogGaugeWidget["gaugeTheme"]))

                    if "offsetAngle" in AnalogGaugeWidget:
                        # Set offset angle
                        gaugeWidget.updateAngleOffset(int(AnalogGaugeWidget["offsetAngle"]))

                    if "innerRadius" in AnalogGaugeWidget:
                        # Set inner radius
                        gaugeWidget.setGaugeColorInnerRadiusFactor(int(AnalogGaugeWidget["innerRadius"]))

                    if "outerRadius" in AnalogGaugeWidget:
                        # Set outer radius
                        gaugeWidget.setGaugeColorOuterRadiusFactor(int(AnalogGaugeWidget["outerRadius"]))

                    if "scaleStartAngle" in AnalogGaugeWidget:
                        # Set start angle
                        gaugeWidget.setScaleStartAngle(int(AnalogGaugeWidget["scaleStartAngle"]))


                    if "totalScaleAngle" in AnalogGaugeWidget:
                        # Set total scale angle
                        gaugeWidget.setTotalScaleAngleSize(int(AnalogGaugeWidget["totalScaleAngle"]))

                    if "enableBarGraph" in AnalogGaugeWidget:
                        # Set enable bar graph
                        gaugeWidget.setEnableBarGraph(bool(AnalogGaugeWidget["enableBarGraph"]))

                    if "enableValueText" in AnalogGaugeWidget:
                        # Set enable text value
                        gaugeWidget.setEnableValueText(bool(AnalogGaugeWidget["enableValueText"]))

                    if "enableNeedlePolygon" in AnalogGaugeWidget:
                        # Set enable needle polygon
                        gaugeWidget.setEnableNeedlePolygon(bool(AnalogGaugeWidget["enableNeedlePolygon"]))

                    if "enableCenterPoint" in AnalogGaugeWidget:
                        # Set enable needle center
                        gaugeWidget.setEnableCenterPoint(bool(AnalogGaugeWidget["enableCenterPoint"]))


                    if "enableScaleText" in AnalogGaugeWidget:
                        # Set enable scale text
                        gaugeWidget.setEnableScaleText(bool(AnalogGaugeWidget["enableScaleText"]))

                    if "enableScaleBigGrid" in AnalogGaugeWidget:
                        # Set enable big scale grid
                        gaugeWidget.setEnableBigScaleGrid(bool(AnalogGaugeWidget["enableScaleBigGrid"]))

                    if "enableScaleFineGrid" in AnalogGaugeWidget:
                        # Set enable big scale grid
                        gaugeWidget.setEnableFineScaleGrid(bool(AnalogGaugeWidget["enableScaleFineGrid"]))

                    if "needleColor" in AnalogGaugeWidget and len(str(AnalogGaugeWidget["needleColor"])) > 0:
                        # Set needle color
                        gaugeWidget.NeedleColor = QColor(self.themeEngine.getThemeVariableValue(str(AnalogGaugeWidget["needleColor"])))
                        gaugeWidget.NeedleColorReleased = QColor(self.themeEngine.getThemeVariableValue(str(AnalogGaugeWidget["needleColor"])))


                    if "needleColorOnDrag" in AnalogGaugeWidget and len(str(AnalogGaugeWidget["needleColorOnDrag"])) > 0:
                        # Set needle color on drag
                        gaugeWidget.NeedleColorDrag = QColor(self.themeEngine.getThemeVariableValue(str(AnalogGaugeWidget["needleColorOnDrag"])))

                    if "scaleValueColor" in AnalogGaugeWidget and len(str(AnalogGaugeWidget["scaleValueColor"])) > 0:
                        # Set value color
                        gaugeWidget.ScaleValueColor = QColor(self.themeEngine.getThemeVariableValue(str(AnalogGaugeWidget["scaleValueColor"])))

                    if "displayValueColor" in AnalogGaugeWidget and len(str(AnalogGaugeWidget["displayValueColor"])) > 0:
                        # Set display value color
                        gaugeWidget.DisplayValueColor = QColor(self.themeEngine.getThemeVariableValue(str(AnalogGaugeWidget["displayValueColor"])))

                    if "bigScaleColor" in AnalogGaugeWidget and len(str(AnalogGaugeWidget["bigScaleColor"])) > 0:
                        # Set big scale color
                        gaugeWidget.setBigScaleColor(QColor(self.themeEngine.getThemeVariableValue(str(AnalogGaugeWidget["bigScaleColor"]))))

                    if "fineScaleColor" in AnalogGaugeWidget and len(str(AnalogGaugeWidget["fineScaleColor"])) > 0:
                        # Set fine scale color
                        gaugeWidget.setFineScaleColor(QColor(self.themeEngine.getThemeVariableValue(str(AnalogGaugeWidget["fineScaleColor"]))))

                    if "customGaugeTheme" in AnalogGaugeWidget:
                        # Set custom gauge theme
                        colors = AnalogGaugeWidget['customGaugeTheme']

                        for x in colors:

                            if "color1" in x and len(str(x['color1'])) > 0:
                                if "color2" in x and len(str(x['color2'])) > 0:
                                    if "color3" in x and len(str(x['color3'])) > 0:

                                        gaugeWidget.setCustomGaugeTheme(
                                                color1 = self.themeEngine.getThemeVariableValue(str(x['color1'])),
                                                color2= self.themeEngine.getThemeVariableValue(str(x['color2'])),
                                                color3 = self.themeEngine.getThemeVariableValue(str(x['color3']))
                                            )

                                    else:

                                        gaugeWidget.setCustomGaugeTheme(
                                                color1 = self.themeEngine.getThemeVariableValue(str(x['color1'])),
                                                color2= self.themeEngine.getThemeVariableValue(str(x['color2']))
                                            )

                                else:

                                    gaugeWidget.setCustomGaugeTheme(
                                            color1 = self.themeEngine.getThemeVariableValue(str(x['color1']))
                                        )

                    if "scalePolygonColor" in AnalogGaugeWidget:
                        # Set scale polygon color
                        colors = AnalogGaugeWidget['scalePolygonColor']

                        for x in colors:

                            if "color1" in x and len(str(x['color1'])) > 0:
                                if "color2" in x and len(str(x['color2'])) > 0:
                                    if "color3" in x and len(str(x['color3'])) > 0:

                                        gaugeWidget.setScalePolygonColor(
                                                color1 = self.themeEngine.getThemeVariableValue(str(x['color1'])),
                                                color2= self.themeEngine.getThemeVariableValue(str(x['color2'])),
                                                color3 = self.themeEngine.getThemeVariableValue(str(x['color3']))
                                            )

                                    else:

                                        gaugeWidget.setScalePolygonColor(
                                                color1 = self.themeEngine.getThemeVariableValue(str(x['color1'])),
                                                color2= self.themeEngine.getThemeVariableValue(str(x['color2'])),
                                            )

                                else:

                                    gaugeWidget.setScalePolygonColor(
                                            color1 = self.themeEngine.getThemeVariableValue(str(x['color1'])),
                                        )

                    if "needleCenterColor" in AnalogGaugeWidget:
                        # Set needle center color
                        colors = AnalogGaugeWidget['needleCenterColor']

                        for x in colors:

                            if "color1" in x and len(str(x['color1'])) > 0:
                                if "color2" in x and len(str(x['color2'])) > 0:
                                    if "color3" in x and len(str(x['color3'])) > 0:

                                        gaugeWidget.setNeedleCenterColor(
                                                color1 = self.themeEngine.getThemeVariableValue(str(x['color1'])),
                                                color2= self.themeEngine.getThemeVariableValue(str(x['color2'])),
                                                color3 = self.themeEngine.getThemeVariableValue(str(x['color3']))
                                            )

                                    else:

                                        gaugeWidget.setNeedleCenterColor(
                                                color1 = self.themeEngine.getThemeVariableValue(str(x['color1'])),
                                                color2= self.themeEngine.getThemeVariableValue(str(x['color2'])),
                                            )

                                else:

                                    gaugeWidget.setNeedleCenterColor(
                                            color1 = self.themeEngine.getThemeVariableValue(str(x['color1'])),
                                        )

                    if "outerCircleColor" in AnalogGaugeWidget:
                        # Set outer circle color
                        colors = AnalogGaugeWidget['outerCircleColor']

                        for x in colors:

                            if "color1" in x and len(str(x['color1'])) > 0:
                                if "color2" in x and len(str(x['color2'])) > 0:
                                    if "color3" in x and len(str(x['color3'])) > 0:

                                        gaugeWidget.setOuterCircleColor(
                                                color1 = self.themeEngine.getThemeVariableValue(str(x['color1'])),
                                                color2= self.themeEngine.getThemeVariableValue(str(x['color2'])),
                                                color3 = self.themeEngine.getThemeVariableValue(str(x['color3']))
                                            )

                                    else:

                                        gaugeWidget.setOuterCircleColor(
                                                color1 = self.themeEngine.getThemeVariableValue(str(x['color1'])),
                                                color2= self.themeEngine.getThemeVariableValue(str(x['color2'])),
                                            )

                                else:

                                    gaugeWidget.setOuterCircleColor(
                                            color1 = self.themeEngine.getThemeVariableValue(str(x['color1'])),
                                        )

                    if "valueFontFamily" in AnalogGaugeWidget:
                        # Set value font family
                        font = AnalogGaugeWidget['valueFontFamily']

                        for x in font:
                            if "path" in x and len(str(x['path'])) > 0:
                                QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), str(x['path'])) )

                            if "name" in x and len(str(x['name'])) > 0:
                                gaugeWidget.setValueFontFamily(str(x['name']))

                    if "scaleFontFamily" in AnalogGaugeWidget:
                        # Set scale font family
                        font = AnalogGaugeWidget['scaleFontFamily']
                        for x in font:
                            if "path" in x and len(str(x['path'])) > 0:

                                QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), str(x['path'])) )

                            if "name" in x and len(str(x['name'])) > 0:
                                gaugeWidget.setScaleFontFamily(str(x['name']))


                else:
                    if not is_in_designer(self):
                        raise Exception(str(AnalogGaugeWidget["name"])+" is not a AnalogGaugeWidget, no widget found")

def configure_slide_menu(self, data, update: bool = False):
    if "QCustomSlideMenu" not in data:
        return

    # Iterate over each menu configuration in QCustomSlideMenu
    for menu_key, slide_menu in data["QCustomSlideMenu"].items():
        # Fetch the widget using get_widget_from_path
        container_widget = get_widget_from_path(self, menu_key)

        # Ensure the fetched widget is valid and is of type QCustomSlideMenu
        if not container_widget or container_widget.metaObject().className() != "QCustomSlideMenu":
            if not is_in_designer(self):
                raise Exception(f"{menu_key} is not a QCustomSlideMenu, no valid widget found or widget type mismatch")
            else:
                return

        # Helper functions to extract sizes and animations
        def get_size(size_data, default_size=(0, 0)):
            return size_data.get("width", default_size[0]), size_data.get("height", default_size[1])

        def get_animation(animation_data):
            return {
                "duration": animation_data.get("animationDuration", 2000),
                "easingCurve": returnAnimationEasingCurve(animation_data.get("animationEasingCurve", "Linear")),
                "collapsingDuration": animation_data.get("whenCollapsing", {}).get("animationDuration", 500),
                "collapsingEasingCurve": returnAnimationEasingCurve(animation_data.get("whenCollapsing", {}).get("animationEasingCurve", "Linear")),
                "expandingDuration": animation_data.get("whenExpanding", {}).get("animationDuration", 500),
                "expandingEasingCurve": returnAnimationEasingCurve(animation_data.get("whenExpanding", {}).get("animationEasingCurve", "Linear"))
            }

        # Extract sizes
        default_width, default_height = get_size(slide_menu.get("defaultSize", {}))
        collapsed_width, collapsed_height = get_size(slide_menu.get("collapsedSize", {}))
        expanded_width, expanded_height = get_size(slide_menu.get("expandedSize", {}))

        # Extract animation details
        animation = get_animation(slide_menu.get("menuTransitionAnimation", {}))

        # Extract styles
        collapsed_style = self.themeEngine.styleVariablesFromTheme(slide_menu.get("menuContainerStyle", {}).get("whenMenuIsCollapsed", ""))
        expanded_style = self.themeEngine.styleVariablesFromTheme(slide_menu.get("menuContainerStyle", {}).get("whenMenuIsExpanded", ""))

        # Process floating menu and shadow settings
        float_menu = slide_menu.get("floatPosition", None) is not None
        relative_to = ""
        position = ""
        shadow_color = ""
        shadow_blur_radius = 0
        shadow_x_offset = 0
        shadow_y_offset = 0
        auto_hide = True

        if float_menu:
            float_position = slide_menu["floatPosition"]
            relative_to = getattr(self.ui, float_position.get("relativeTo", ""), float_position.get("relativeTo", ""))
            position = float_position.get("position", "")
            shadow = float_position.get("shadow", {})
            shadow_color = self.themeEngine.getThemeVariableValue(shadow.get("color", "#000"))
            shadow_blur_radius = shadow.get("blurRadius", 20)
            shadow_x_offset = shadow.get("xOffset", 0)
            shadow_y_offset = shadow.get("yOffset", 0)
            auto_hide = float_position.get("autoHide", True)

        # Process toggle button
        button_name = slide_menu.get("toggleButton", {}).get("buttonName", "")
        menu_collapsed_icon = ""
        menu_expanded_icon = ""
        menu_collapsed_style = ""
        menu_expanded_style = ""

        if button_name:
            # Use the dynamic widget fetching function to handle nested widget paths
            button_widget = get_widget_from_path(self, button_name)

            if button_widget:
                toggle_button = slide_menu.get("toggleButton", {})
                icons = toggle_button.get("icons", {})

                # Replace the icon URLs with the correct prefix
                menu_collapsed_icon = replace_url_prefix(icons.get("whenMenuIsCollapsed", ""), "Qss/icons")
                menu_expanded_icon = replace_url_prefix(icons.get("whenMenuIsExpanded", ""), "Qss/icons")

                # Get the styles from the theme, for collapsed and expanded states
                menu_collapsed_style = self.themeEngine.styleVariablesFromTheme(toggle_button.get("style", {}).get("whenMenuIsCollapsed", ""))
                menu_expanded_style = self.themeEngine.styleVariablesFromTheme(toggle_button.get("style", {}).get("whenMenuIsExpanded", ""))

                # Apply the styles or icons to the button as needed
                button_widget.setStyleSheet(menu_collapsed_style)  # Example application, update as per your need
                button_widget.setIcon(QIcon(menu_collapsed_icon))  # Set the collapsed icon
            else:
                if not is_in_designer(self):
                    # Raise an exception if the button widget doesn't exist
                    raise Exception(f"Error: '{button_name}' widget does not exist")


        # Apply customization to the widget
        container_widget.customizeQCustomSlideMenu(
            defaultWidth=default_width,
            defaultHeight=default_height,
            collapsedWidth=collapsed_width,
            collapsedHeight=collapsed_height,
            expandedWidth=expanded_width,
            expandedHeight=expanded_height,
            animationDuration=animation["duration"],
            animationEasingCurve=animation["easingCurve"],
            collapsingAnimationDuration=animation["collapsingDuration"],
            collapsingAnimationEasingCurve=animation["collapsingEasingCurve"],
            expandingAnimationDuration=animation["expandingDuration"],
            expandingAnimationEasingCurve=animation["expandingEasingCurve"],
            collapsedStyle=collapsed_style,
            expandedStyle=expanded_style,
            floatMenu=float_menu,
            relativeTo=relative_to,
            position=position,
            shadowColor=shadow_color,
            shadowBlurRadius=shadow_blur_radius,
            shadowXOffset=shadow_x_offset,
            shadowYOffset=shadow_y_offset,
            autoHide=auto_hide,
            update=update
        )

        # Apply toggle button customization if button exists
        if button_name:
            container_widget.toggleButton(
                buttonName=button_name,
                iconWhenMenuIsCollapsed=menu_collapsed_icon,
                iconWhenMenuIsExpanded=menu_expanded_icon,
                styleWhenMenuIsCollapsed=menu_collapsed_style,
                styleWhenMenuIsExpanded=menu_expanded_style,
                update=update
            )

        # Optionally refresh the widget
        if not update:
            container_widget.refresh()

def configure_main_window(self, data, update: bool = False):
    ## WINDOWS FLAG
    if "QMainWindow" in data and not is_in_designer(self):
        # Accessing values
        qmainwindow = data.get("QMainWindow", {})

        title = qmainwindow.get("tittle", "")
        icon = qmainwindow.get("icon", "")
        frameless = qmainwindow.get("frameless", False)
        translucent_bg = qmainwindow.get("transluscentBg", False)
        size_grip = qmainwindow.get("sizeGrip", "")
        border_radius = qmainwindow.get("borderRadius", 0)
        self.borderRadius = border_radius

        shadow = qmainwindow.get("shadow", {})
        shadow_color = shadow.get("color", "")
        self.shadowColor = shadow_color
        shadow_blur_radius = shadow.get("blurRadius", 0)
        self.shadowBlurRadius = shadow_blur_radius
        shadow_x_offset = shadow.get("xOffset", 0)
        self.shadowXOffset = shadow_x_offset
        shadow_y_offset = shadow.get("yOffset", 0)
        self.shadowYOffset = shadow_y_offset

        navigation = qmainwindow.get("navigation", {})
        minimize_button = navigation.get("minimize", "")
        close_button = navigation.get("close", "")

        restore = navigation.get("restore", {})
        restore_button_name = restore.get("buttonName", "")
        restore_normal_icon = restore.get("normalIcon", "")
        restore_maximized_icon = restore.get("maximizedIcon", "")

        move_window = navigation.get("moveWindow", "")
        title_bar = navigation.get("tittleBar", "")

        if title:
            # Set window title
            self.setWindowTitle(title)

        if icon:
            # Set window Icon
            self.setWindowIcon(QIcon(icon))

        try:
            # if not update:
            if frameless:
                # Remove window title bar
                self.setWindowFlags(Qt.FramelessWindowHint)

            if translucent_bg:
                # Set main background to transparent
                self.setAttribute(Qt.WA_TranslucentBackground)
        except:
            pass

        if size_grip:
            # Add a size grip to the window
            try:
                size_grip_widget = get_widget_from_path(self, size_grip)
                if size_grip_widget:
                    QSizeGrip(size_grip_widget)
                else:
                    if not is_in_designer(self):
                        raise Exception(f"Size grip widget '{size_grip}' not found.")
            except Exception as e:
                logException(e)

        # Configure shadow (handled inside the class)

        if minimize_button:
            # Minimize window
            try:
                minimize_btn = get_widget_from_path(self, minimize_button)
                if minimize_btn:
                    minimize_btn.clicked.connect(lambda: self.showMinimized())
                else:
                    if not is_in_designer(self):
                        raise Exception(f"Minimize button '{minimize_button}' not found.")
            except Exception as e:
                logException(e)

        if close_button:
            # Close window
            try:
                close_btn = get_widget_from_path(self, close_button)
                if close_btn:
                    close_btn.clicked.connect(lambda: self.close())
                else:
                    if not is_in_designer(self):
                        raise Exception(f"Close button '{close_button}' not found.")
            except Exception as e:
                logException(e)

        if restore_button_name:
            try:
                prevbtn = self.restoreBtn
            except:
                prevbtn = None

            try:
                restore_button = get_widget_from_path(self, restore_button_name)
                # Check if the button is valid and has connections before trying to disconnect
                if restore_button is not None:
                    if prevbtn != restore_button:
                        self.restoreBtn = restore_button
                        restore_button.clicked.connect(lambda: self.toggleWindowSize(""))
        
                else:
                    if not is_in_designer(self):
                        raise Exception(f"Restore button '{restore_button_name}' not found.")
            except Exception as e:
                logException(e)

        # Handle the restore icons
        if restore_normal_icon:
            self.normalIcon = replace_url_prefix(restore_normal_icon, "Qss/icons")
            self.normalIcon = replace_url_prefix(self.normalIcon, "PATH_RESOURCES")
        else:
            self.normalIcon = ""

        if restore_maximized_icon:
            self.maximizedIcon = replace_url_prefix(restore_maximized_icon, "Qss/icons")
            self.maximizedIcon = replace_url_prefix(self.maximizedIcon, "PATH_RESOURCES")
        else:
            self.maximizedIcon = ""

        if move_window:
            # Add click event/Mouse move event/drag event to the top header to move the window
            try:
                move_window_widget = get_widget_from_path(self, move_window)
                if move_window_widget:
                    move_window_widget.mouseMoveEvent = self.moveWindow
                else:
                    if not is_in_designer(self):
                        raise Exception(f"Move window widget '{move_window}' not found.")
            except Exception as e:
                logException(e)

        if title_bar:
            # Add click event/Mouse move event/drag event to the title bar to move the window
            try:
                title_bar_widget = get_widget_from_path(self, title_bar)
                if title_bar_widget:
                    title_bar_widget.mouseDoubleClickEvent = self.toggleWindowSize
                else:
                    if not is_in_designer(self):
                        raise Exception(f"Title bar widget '{title_bar}' not found.")
            except Exception as e:
                logException(e)

def configure_push_button(self, data, update: bool = False):
    if "QPushButton" in data:
        for button in data['QPushButton']:
            if "name" in button and len(button["name"]) > 0:
                # GET BUTTON OBJECT
                buttonObject = get_widget_from_path(self, str(button["name"]))
                if buttonObject:
                    # VERIFY IF THE OBJECT IS A BUTTON
                    if not str(buttonObject.metaObject().className()) == "QCustomQPushButton" and not buttonObject.metaObject().className() == "QPushButtonThemed":
                        if not is_in_designer(self):
                            raise Exception(buttonObject.metaObject().className(), buttonObject, " is not of type QPushButton")
                        else:
                            return

                    buttonObject.wasFound = False
                    buttonObject.wasThemed = False

                    if buttonObject.objectName() == button["name"]:
                        if "theme" in button and len(button["theme"]) > 0:
                            buttonObject.setObjectTheme(button["theme"])

                        if "customTheme" in button and len(button["customTheme"]) > 0:
                            for x in button["customTheme"]:
                                if len(x["color1"]) > 0 and len(x["color1"]) > 0 :
                                    buttonObject.setObjectCustomTheme(self.themeEngine.getThemeVariableValue(x["color1"]), self.themeEngine.getThemeVariableValue(x["color2"]))

                        if "animateOn" in button and len(button["animateOn"]) > 0:
                            buttonObject.setObjectAnimateOn(button["animateOn"])

                        if "animation" in button and len(button["animation"]) > 0:
                            buttonObject.setObjectAnimation(button["animation"])

                        if "animationDuration" in button and int(button['animationDuration']) > 0:
                            buttonObject._animation.setDuration(int(button["animationDuration"]))

                        if "animationEasingCurve" in button and len(button['animationEasingCurve']) > 0:
                            easingCurve = returnAnimationEasingCurve(button['animationEasingCurve'])
                            buttonObject._animation.setEasingCurve(easingCurve)


                        fallBackStyle = ""
                        if "fallBackStyle" in button:
                            for x in button["fallBackStyle"]:
                                fallBackStyle += x

                        defaultStyle = ""
                        if "defaultStyle" in button:
                            for x in button["defaultStyle"]:
                                defaultStyle += x

                        buttonObject.wasThemed = True

                        if len(fallBackStyle) > 0:
                            buttonObject.setObjectFallBackStyle(self.themeEngine.styleVariablesFromTheme(fallBackStyle))

                        if len(defaultStyle) > 0:
                            buttonObject.setObjectDefaultStyle(self.themeEngine.styleVariablesFromTheme(defaultStyle))

                        if len(fallBackStyle) > 0:
                            buttonObject.setStyleSheet(defaultStyle + fallBackStyle)
                        elif "theme" in button and len(button["theme"]) > 0:
                            #
                            applyAnimationThemeStyle(buttonObject, button["theme"])
                        elif "customTheme" in button and len(button["customTheme"]) > 0:
                            for x in button["customTheme"]:
                                if len(x["color1"]) > 0 and len(x["color1"]) > 0 :
                                    applyCustomAnimationThemeStyle(buttonObject, self.themeEngine.getThemeVariableValue(x["color1"]), self.themeEngine.getThemeVariableValue(x["color2"]))
                        else:
                            buttonObject.wasThemed = False

                        ## ICONIFY STYLESHEET
                        if "iconify" in button:
                            for icon in button['iconify']:
                                if "icon" in icon and len(icon['icon']) > 0:
                                    btnIcon = icon['icon']
                                    if "color" in icon and len(icon['color']) > 0:
                                        color = self.themeEngine.getThemeVariableValue(icon['color'])
                                    else:
                                        color = ""

                                    if "size" in icon and int(icon['size']) > 0:
                                        size = icon['size']
                                    else:
                                        size = ""

                                    if "animateOn" in icon and len(icon['animateOn']) > 0:
                                        animateOn = icon['animateOn']
                                    else:
                                        animateOn = ""

                                    if "animation" in icon and len(icon['animation']) > 0:
                                        animation = icon['animation']
                                    else:
                                        animation = ""

                                    iconify(buttonObject, icon = btnIcon, color = color, size = size, animation = animation, animateOn = animateOn)


                        ## BUTTON SHADOW STYLESHEET
                        if "shadow" in button:
                            for shadow in button["shadow"]:
                                if "color" in shadow and len(str(shadow['color'])) > 0:
                                    shadowColor = self.themeEngine.getThemeVariableValue(shadow['color'])
                                else:
                                    shadowColor = ""

                                if "applyShadowOn" in shadow and len(str(shadow['applyShadowOn'])) > 0:
                                    applyShadowOn = shadow['applyShadowOn']
                                else:
                                    applyShadowOn = ""

                                if "animateShadow" in shadow:
                                    animateShadow = shadow['animateShadow']
                                else:
                                    animateShadow = False

                                if "animateShadowDuration" in shadow and int(shadow['animateShadowDuration']) > 0:
                                    animateShadowDuration = shadow['animateShadowDuration']
                                else:
                                    animateShadowDuration = 0

                                if "blurRadius" in shadow and int(shadow['blurRadius']) > 0:
                                    blurRadius = shadow['blurRadius']
                                else:
                                    blurRadius = 0

                                if "xOffset" in shadow and int(shadow['xOffset']) > 0:
                                    xOffset = shadow['xOffset']
                                else:
                                    xOffset = 0

                                if "yOffset" in shadow and int(shadow['yOffset']) > 0:
                                    yOffset = shadow['yOffset']
                                else:
                                    yOffset = 0

                                applyButtonShadow(
                                    buttonObject,
                                    color= shadowColor,
                                    applyShadowOn= applyShadowOn,
                                    animateShadow = animateShadow,
                                    blurRadius = blurRadius,
                                    animateShadowDuration = animateShadowDuration,
                                    xOffset = xOffset,
                                    yOffset = yOffset
                                )

                        buttonObject.wasFound = True

def configure_custom_stacked_widget(self, data, update: bool = False):
    ## Qstacked Widget
    if "QCustomQStackedWidget" in data:
        for stackedWidget in data['QCustomQStackedWidget']:
            if "name" in stackedWidget and len(str(stackedWidget["name"])) > 0:
                widget = get_widget_from_path(self, str(stackedWidget["name"]))
                if widget:
                    if "transitionAnimation" in stackedWidget:
                        transitionAnimation = stackedWidget["transitionAnimation"]
                        if "fade" in transitionAnimation:
                            fade = transitionAnimation["fade"]
                            if "active" in fade and fade["active"]:
                                widget.fadeTransition = True
                                if "duration" in fade and fade["duration"] > 0:
                                    widget.fadeTime = fade["duration"]
                                if "easingCurve" in fade and len(str(fade["easingCurve"])) > 0:
                                    widget.fadeEasingCurve = fade["easingCurve"]

                        if "slide" in transitionAnimation:
                            slide = transitionAnimation["slide"]
                            if "active" in slide and slide["active"]:
                                widget.slideTransition = True
                                if "duration" in slide and slide["duration"] > 0:
                                    widget.transitionTime = slide["duration"]
                                if "easingCurve" in slide and len(str(slide["easingCurve"])) > 0:
                                    widget.transitionEasingCurve = slide["easingCurve"]
                                if "direction" in slide and len(str(slide["direction"])) > 0:
                                    widget.transitionDirection = returnQtDirection(slide["direction"])

                    if "navigation" in stackedWidget:
                        navigation = stackedWidget["navigation"]
                        if "nextPage" in navigation:
                            button = get_widget_from_path(self, str(navigation["nextPage"]))
                            if button:
                                button.clicked.connect(lambda: widget.slideToNextWidget())
                            else:
                                if not is_in_designer(self):
                                    raise Exception("Unknown button '" +str(button)+ "'. Please check your JSon file")

                        if "previousPage" in navigation:
                            button = get_widget_from_path(self, str(navigation["previousPage"]))
                            if button:
                                button.clicked.connect(lambda: widget.slideToPreviousWidget())
                            else:
                                if not is_in_designer(self):
                                    raise Exception("Unknown button '" +str(button)+ "'. Please check your JSon file")

                        if "navigationButtons" in navigation:
                            navigationButton = navigation["navigationButtons"]
                            for button, widgetPage in navigationButton.items():
                                # Get button and widget page dynamically
                                pushBtn = get_widget_from_path(self, str(button))
                                widgetPg = get_widget_from_path(self, str(widgetPage))
                                
                                # Raise an exception if the widget or button is not found
                                if not pushBtn:
                                    if not is_in_designer(self):
                                        raise Exception(f"Unknown button '{button}'. Please check your JSON file.")
                                if not widgetPg:
                                    if not is_in_designer(self):
                                        raise Exception(f"Unknown widget '{widgetPage}'. Please check your JSON file.")
                                
                                # Proceed with navigation configuration if both button and widget page are found
                                navigationButtons(widget, pushBtn, widgetPg)

                else:
                    if not is_in_designer(self):
                        warnings.warn("Error: QCustomQStackedWidget "+str(stackedWidget["name"])+" not found", RuntimeWarning)

def configure_custom_progress_indicator(self, data, update: bool = False):
    ## QCustomProgressIndicator
    if "QCustomProgressIndicator" in data:
        for QCustomProgressIndicator in data['QCustomProgressIndicator']:
            if "name" in QCustomProgressIndicator and len(str(QCustomProgressIndicator["name"])) > 0:
                containerWidget = get_widget_from_path(self, str(QCustomProgressIndicator["name"]))
                if containerWidget:
                    if not containerWidget.metaObject().className() == "QCustomProgressIndicator":
                        if not is_in_designer(self):
                            raise Exception("Error: "+str(QCustomProgressIndicator["name"])+" is not a QCustomProgressIndicator widget")
                        else:
                            return
                    
                    if "color" in QCustomProgressIndicator:
                        containerWidget.color = self.themeEngine.getThemeVariableValue(str(QCustomProgressIndicator["color"]))
                        containerWidget.updateFormProgressIndicator(color = containerWidget.color)
                    
                    if "fillColor" in QCustomProgressIndicator:
                        containerWidget.fillColor = self.themeEngine.getThemeVariableValue(str(QCustomProgressIndicator["fillColor"]))
                        containerWidget.updateFormProgressIndicator(fillColor = containerWidget.fillColor)

                    if "warningFillColor" in QCustomProgressIndicator:
                        containerWidget.warningFillColor = self.themeEngine.getThemeVariableValue(str(QCustomProgressIndicator["warningFillColor"]))
                        containerWidget.updateFormProgressIndicator(warningFillColor = containerWidget.warningFillColor)

                    if "errorFillColor" in QCustomProgressIndicator:
                        containerWidget.errorFillColor = self.themeEngine.getThemeVariableValue(str(QCustomProgressIndicator["errorFillColor"]))
                        containerWidget.updateFormProgressIndicator(errorFillColor = containerWidget.errorFillColor)

                    if "successFillColor" in QCustomProgressIndicator:
                        containerWidget.successFillColor = self.themeEngine.getThemeVariableValue(str(QCustomProgressIndicator["successFillColor"]))
                        containerWidget.updateFormProgressIndicator(successFillColor = containerWidget.successFillColor)

                    if "formProgressCount" in QCustomProgressIndicator:
                        containerWidget.formProgressCount = int(QCustomProgressIndicator["formProgressCount"])
                        containerWidget.updateFormProgressIndicator(formProgressCount = containerWidget.formProgressCount)

                    if "formProgressAnimationDuration" in QCustomProgressIndicator:
                        containerWidget.formProgressAnimationDuration = int(QCustomProgressIndicator["formProgressAnimationDuration"])
                        containerWidget.updateFormProgressIndicator(formProgressAnimationDuration = containerWidget.formProgressAnimationDuration)
                    
                    if "formProgressAnimationEasingCurve" in QCustomProgressIndicator:
                        containerWidget.formProgressAnimationEasingCurve = str(QCustomProgressIndicator["formProgressAnimationEasingCurve"])
                        containerWidget.updateFormProgressIndicator(formProgressAnimationEasingCurve = containerWidget.formProgressAnimationEasingCurve)
                    
                    if "height" in QCustomProgressIndicator:
                        containerWidget.height = int(QCustomProgressIndicator["height"])
                        containerWidget.updateFormProgressIndicator(height = containerWidget.height)

                    if "width" in QCustomProgressIndicator:
                        containerWidget.width = int(QCustomProgressIndicator["width"])
                        containerWidget.updateFormProgressIndicator(width = containerWidget.width)
                    
                    if "startPercentage" in QCustomProgressIndicator:
                        containerWidget.startPercentage = int(QCustomProgressIndicator["startPercentage"])
                        containerWidget.updateFormProgressIndicator(startPercentage = containerWidget.startPercentage)

                    if "theme" in QCustomProgressIndicator:
                        containerWidget.theme = int(QCustomProgressIndicator["theme"])
                        containerWidget.selectFormProgressIndicatorTheme(containerWidget.theme)

                    # containerWidget.updateFormProgress(value)
                    
def configure_custom_check_box(self, data, update: bool = False):
    ## QCustomCheckBox
    if "QCustomCheckBox" in data:
        for QCustomCheckBox in data['QCustomCheckBox']:

            checkBoxes = []

            # Collect checkbox names (single or multiple)
            if "name" in QCustomCheckBox and len(str(QCustomCheckBox["name"])) > 0:
                checkBoxes.append(QCustomCheckBox["name"])

            if "names" in QCustomCheckBox:
                checkBoxes.extend(QCustomCheckBox["names"])

            if checkBoxes:
                for checkBox in checkBoxes:
                    # Fetch the widget dynamically using the path
                    containerWidget = get_widget_from_path(self, str(checkBox))
                    
                    if containerWidget:
                        # Ensure the widget is of type QCustomCheckBox
                        if containerWidget.metaObject().className() != "QCustomCheckBox":
                            if not is_in_designer(self):
                                raise Exception(f"Error: '{checkBox}' is not a QCustomCheckBox widget")
                            else:
                                return
                        
                        # Apply customization based on the JSON attributes
                        if "bgColor" in QCustomCheckBox:
                            containerWidget.bgColor = QColor(self.themeEngine.getThemeVariableValue(str(QCustomCheckBox["bgColor"])))
                            containerWidget.customizeQCustomCheckBox(bgColor=containerWidget.bgColor)

                        if "circleColor" in QCustomCheckBox:
                            containerWidget.circleColor = QColor(self.themeEngine.getThemeVariableValue(str(QCustomCheckBox["circleColor"])))
                            containerWidget.customizeQCustomCheckBox(circleColor=containerWidget.circleColor)

                        if "activeColor" in QCustomCheckBox:
                            containerWidget.activeColor = QColor(self.themeEngine.getThemeVariableValue(str(QCustomCheckBox["activeColor"])))
                            containerWidget.customizeQCustomCheckBox(activeColor=containerWidget.activeColor)

                        if "animationEasingCurve" in QCustomCheckBox:
                            containerWidget.animationEasingCurve = self.returnAnimationEasingCurve(str(QCustomCheckBox["animationEasingCurve"]))
                            containerWidget.customizeQCustomCheckBox(animationEasingCurve=containerWidget.animationEasingCurve)

                        if "animationDuration" in QCustomCheckBox:
                            containerWidget.animationDuration = int(QCustomCheckBox["animationDuration"])
                            containerWidget.customizeQCustomCheckBox(animationDuration=containerWidget.animationDuration)

                    else:
                        if not is_in_designer(self):
                            # Raise an exception if the widget doesn't exist
                            raise Exception(f"Error: '{checkBox}' widget does not exist")

def updateJson(file_path, key_path, value, self=None):
    if self:
        tempFMOnitor = self.liveCompileQss
        self.liveCompileQss = False

    # Helper function to update nested dictionary or list
    def update_nested_dict_or_list(d, keys, value):
        for key in keys[:-1]:
            if isinstance(d, list):
                if key.isdigit():
                    d = d[int(key)]
                else:
                    d = d.setdefault(key, {})
            else:
                d = d.setdefault(key, {})
        if isinstance(d, list):
            if keys[-1].isdigit():
                if d[int(keys[-1])] != value:  # Check if value differs
                    d[int(keys[-1])] = value
            else:
                d.append(value)  # Assuming appending to list if key is not index
        else:
            if d.get(keys[-1]) != value:  # Only update if value is different
                d[keys[-1]] = value

    try:
        # Read JSON data from the file
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Split the key_path into a list of keys
        keys = key_path.split('.')

        # Check if the value at the key_path is different before updating
        current_value = data
        try:
            for key in keys:
                if isinstance(current_value, list):
                    current_value = current_value[int(key)]
                else:
                    current_value = current_value[key]

            if current_value == value:
                logInfo(f"No change for {key_path}. Value is already {value}.")
                return  # Exit if the value is the same
        except (KeyError, IndexError):
            pass  # If key does not exist, proceed with the update

        # Update the JSON data with the given key and value
        update_nested_dict_or_list(data, keys, value)

        # Write the updated JSON data back to the file
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

        logInfo(f"Updated {key_path} with value: {value}")

    except Exception as e:
        logError(f"An error occurred: {e}")

    if self:
        self.liveCompileQss = tempFMOnitor


def navigationButtons(stackedWidget, pushButton, widgetPage):
    pushButton.clicked.connect(lambda: stackedWidget.setCurrentWidget(widgetPage))

def get_widget_from_path(self, path: str):
    """
    Fetches the widget based on a dot-separated string path.
    For example, "FooterComponentContainer.shownForm.activityProgress" will return self.ui.FooterComponentContainer.shownForm.activityProgress if it exists.
    
    :param path: Dot-separated string path to the widget.
    :return: The widget if found, None otherwise.
    """
    if not hasattr(self, "ui"):
        print(self)
        return None
    # Start from self.ui
    current_attr = self.ui

    # Split the path by '.' to navigate through nested objects
    for attr in path.split('.'):
        # Check if the current attribute exists in the current context
        if hasattr(current_attr, attr):
            current_attr = getattr(current_attr, attr)
        else:
            # If any part of the path doesn't exist, return None
            print(f"Widget '{attr}' in path '{path}' not found.")
            return None
    
    # Return the final widget
    return current_attr

class Object(object):
    pass