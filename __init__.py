# A little something... For you, From Shubh
from aqt import mw
from aqt.utils import qconnect
from aqt.qt import *
from aqt.gui_hooks import browser_menus_did_init

# Function to filter the QListWidget based on search text
def filter_decks(search_text, list_widget):
    # Filter items in the list
    for index in range(list_widget.count()):
        item = list_widget.item(index)
        if search_text.lower() in item.text().lower():
            item.setHidden(False)  # Show matching item
        else:
            item.setHidden(True)  # Hide non-matching item

# Function to show all decks in a new window
def show_deck_list():
    # Get all deck names
    deck_manager = mw.col.decks
    all_decks = deck_manager.all_names_and_ids()  # Returns a list of DeckNameId objects

    # Create a new main window
    window = QMainWindow(mw)
    window.setWindowTitle("Deck List")
    window.setMinimumSize(1200, 900)

    # Create a central widget to hold everything
    central_widget = QWidget(window)
    window.setCentralWidget(central_widget)

    # Create a layout for the central widget
    layout = QVBoxLayout(central_widget)

    # Create a search bar
    search_bar = QLineEdit()
    search_bar.setPlaceholderText("Search decks...")

    # Create a QListWidget to display deck names
    list_widget = QListWidget()

    # Add all deck names to the QListWidget
    for deck in all_decks:
        list_item = QListWidgetItem(deck.name)
        list_widget.addItem(list_item)

    # Connect search bar input to filter function
    search_bar.textChanged.connect(lambda: filter_decks(search_bar.text(), list_widget))

    # Add the search bar and list widget to the layout
    layout.addWidget(search_bar)
    layout.addWidget(list_widget)

    # Reimplement the minimize behavior
    def eventFilter(obj, event):
        if event.type() == QEvent.WindowStateChange and window.windowState() & Qt.WindowMinimized:
            # Get the screen's geometry
            screen_geometry = QDesktopWidget().availableGeometry(window)
            # Set a new small size for the minimized window (e.g., 150x150 for a visible icon)
            new_width, new_height = 150, 150
            window.resize(new_width, new_height)
            return True
        return False

    # Install the event filter on the window
    window.installEventFilter(window)

    # Show the new main window
    window.show()

# Function to add "Deck List" to the Tools menu
def setup_tools_menu():
    action = QAction("Deck List", mw)
    qconnect(action.triggered, show_deck_list)
    mw.form.menuTools.addAction(action)

# Function to add "Deck List" to the Browse menu
def setup_browser_menu(browser):
    menu = browser.form.menuEdit  # Add under the "Edit" menu in the browser
    action = QAction("Deck List", browser)
    qconnect(action.triggered, show_deck_list)
    menu.addSeparator()
    menu.addAction(action)

    # Set up a shortcut for the deck list in the Browse window
    browse_shortcut = QShortcut(QKeySequence("Ctrl+Alt+D"), browser)
    qconnect(browse_shortcut.activated, show_deck_list)

# Register the setup_browser_menu function to the browser menu initialization hook
browser_menus_did_init.append(setup_browser_menu)

# Set up a shortcut for the deck list in the main window
def setup_main_shortcut():
    main_shortcut = QShortcut(QKeySequence("Ctrl+Alt+D"), mw)
    qconnect(main_shortcut.activated, show_deck_list)

# Call the setup functions to add the Deck List option to both menus and the shortcut
setup_tools_menu()
setup_main_shortcut()
