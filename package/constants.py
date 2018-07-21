# Naming
APP_NAME = "Sideview Controller"
APP_VERSION = "0.1a"
APP_TITLE = "{}    version {}".format(APP_NAME, APP_VERSION)

# Dimensions
MW_DEFAULT_WIDTH = 600
MW_DEFAULT_HEIGHT = 600
RES_HIGH_HD = "1920x1080"
RES_LOW_HD = "1280x720"
RES_HQ = "640x480"

# Directories
DIR_ICON = "icons/"
DIR_CONFIG = "configs/"

# States
STATE_MW_IDLE = 0
STATE_MW_RUN = 1
STATE_DIALOG_ADD = 0
STATE_DIALOG_EDIT = 1
STATE_DIALOG_OPEN = 2

# Indices
IDX_TAB_CAM = 0
IDX_TAB_SCREEN = 1
IDX_TAB_COM = 2

# Labels
LABEL_LABEL_OUTPUT = "Output"
LABEL_PB_OUTPUT = "Browse..."
LABEL_PB_ADD = "Add"
LABEL_PB_EDIT = "Edit"
LABEL_PB_OPEN = "Open"
LABEL_PB_REMOVE = "Remove"
LABEL_PB_REFRESH_CAM = "Refresh Cams"
LABEL_LABEL_CONTROLS = "Stop recording after:"
LABEL_RB_TIME = "Specified time:"
LABEL_RB_LOOP = "Video plays:"
LABEL_LABEL_LOOPS = "loops"
LABEL_TAB_CAM = "Cameras"
LABEL_TAB_SCREEN = "Screens"
LABEL_TAB_COM = "COMs"
LABEL_CAM_DIALOG_TITLE_ADD = "Add a Camera"
LABEL_CAM_DIALOG_TITLE_EDIT = "Edit an Existing Camera"
LABEL_LABEL_CAM_NAME = "Name"
LABEL_LABEL_CAM_LINK = "Camera"
LABEL_LABEL_CAM_RES = "Resolution"
LABEL_LABEL_COM_NAME = "Name"
LABEL_LABEL_COM_LINK = "Link"
LABEL_LABEL_COM_SIGNAL = "Signal"
LABEL_LABEL_COM_BAUD_RATE = "Baud Rate"
LABEL_LABEL_COM_RULES = "Rules"
LABEL_LABEL_RULE_NUM = "Rule Number"
LABEL_RB_RULE_AT = "Signal at:"
LABEL_RB_RULE_EVERY = "Signal every:"
LABEL_SCREEN_DIALOG_TITLE_ADD = "Add a Screen"
LABEL_SCREEN_DIALOG_TITLE_EDIT = "Edit an Existing Screen"
LABEL_LABEL_SCREEN_NAME = "Name"
LABEL_LABEL_MONITOR_NUM = "Monitor"
LABEL_RB_SCREEN_VIDEO = "Video"
LABEL_RB_SCREEN_COLOR = "Flat Color"
LABEL_PB_SCREEN_VIDEO = "Browse..."
LABEL_PB_SCREEN_COLOR = "Choose..."
LABEL_CB_MON_NUM_NA = "N/A"
LABEL_CB_NEW_RULE = "Create a new rule..."
LABEL_COM_DIALOG_TITLE_ADD = "Add a COM Device"
LABEL_COM_DIALOG_TITLE_EDIT = "Edit an Existing COM Device"
LABEL_RULE_DIALOG_TITLE_ADD = "Add a New Rule"
LABEL_RULE_DIALOG_TITLE_EDIT = "Edit an Existing Rule"
LABEL_PB_RULE_REMOVE = "Delete"

# Icons
ICON_PLAYBUTTON = DIR_ICON + "play_button.png"
ICON_PLAYBUTTON_LIGHT = DIR_ICON + "play_button_light.png"
ICON_PLAYBUTTON_DARK = DIR_ICON + "play_button_dark.png"
ICON_PLAYBUTTON_GRAY = DIR_ICON + "play_button_gray.png"

ICON_STOPBUTTON = DIR_ICON + "stop_button.png"
ICON_STOPBUTTON_LIGHT = DIR_ICON + "stop_button_light.png"
ICON_STOPBUTTON_DARK = DIR_ICON + "stop_button_dark.png"
ICON_STOPBUTTON_GRAY = DIR_ICON + "stop_button_gray.png"

ICON_LOGO_SMALL = "sv_logo_small.png"

# Prompts
PROMPT_FOLDER_SELECT = "Select a directory:"
PROMPT_CONFIG_SELECT = "Select a configuration file:"

# Dialogs
DIALOG_TITLE_ERROR = "Error"
DIALOG_TITLE_VW = "Video Writer"
DIALOG_MESSAGE_NO_OUTPUT = "No output folder selected."
DIALOG_MESSAGE_NO_VIDEO = "No video selected for loop termination."
DIALOG_MESSAGE_NO_CAM = "No camera is currently open for recording."
DIALOG_MESSAGE_DUP_NAME = "A device with that name already exists."
DIALOG_MESSAGE_BLANK_FIELDS = "All fields are required."
DIALOG_MESSAGE_CAM_TAKEN = "The selected camera link is being used by \"{}\""
DIALOG_OPEN_VIDEO_TITLE = "Open a Video"
DIALOG_WRITING_VIDEO = "Writing video to file:"

# Overlay
OVERLAY_IDLE = "Idle"
OVERLAY_REC = "Recording..."
OVERLAY_FONT_SCALE = 1
OVERLAY_FONT_SCALE_LARGE = 2
OVERLAY_FONT_REC_COLOR = (0, 0, 228)
OVERLAY_FONT_IDLE_COLOR = (224, 171, 140)
OVERLAY_FONT_WHITE_COLOR = (255, 255, 255)
OVERLAY_FONT_POINT = (10, 30)
OVERLAY_FONT_POINT_LARGE = (20, 60)
OVERLAY_FONT_THICKNESS = 2

# Other
IDLE_COLOR_RGB = (140, 171, 224)
REC_COLOR_RGB = (228, 0, 0)
FILTER_VIDEO = "Video files (*.avi *.mp4)"
FILTER_CONFIG = "Config files (*.ini)"
CAM_FPS = 60
CAM_IDX_RANGE = 4
OUTPUT_FILE_EXT = ".avi"
