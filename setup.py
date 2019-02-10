from cx_Freeze import setup, Executable

base = None

executables = [Executable("main.py", base=base)]

packages = ["idna", "os", "sys", "math", "platform"]
options = {
    'build_exe': {
        'packages': packages,
    },
}

setup(
    name = "Base calculator",
    options = options,
    version = "1.0.0",
    description = 'It calculates stuff',
    executables = executables
)