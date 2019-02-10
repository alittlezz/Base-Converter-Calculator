from console_ui import ConsoleUI
import platform
import sys

if __name__ == "__main__":
    ui = ConsoleUI(platform.system())
    ui.run()
    sys.exit()