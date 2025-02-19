# Utheme-Tool
A tool to create Wii U Theme Archives (`.utheme`).

- Requires `.bps` patches made with [Flips](https://github.com/Alcaro/Flips) or any other `.bps` tool.

- Requires the original files that correspond to each `.bps` file (e.g. `Men.pack`). 

## Building
You can run `utheme-tool.py` if you have Python 3 installed, alternatively you can use `pyinstaller` to create a single executable.

Example usage: `pyinstaller --onefile --windowed --add-data "create_utheme.py;." utheme-tool.py`
