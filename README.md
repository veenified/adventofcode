# Advent of Code

A repo where I maintain all my Advent of Code solutions over the years... mostly in Go and Python.

This project includes a Textual TUI to easily browse and run solutions.

## Getting Started

This project uses `uv` for Python package and virtual environment management.

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv)

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/veenified/adventofcode.git
    cd adventofcode
    ```

2.  **Create a virtual environment:**
    ```bash
    uv venv
    ```

3.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate
    ```

4.  **Install dependencies:**
    ```bash
    uv pip sync pyproject.toml
    ```

## How to Run

### Using the TUI

To launch the Textual TUI, simply run:

```bash
python main.py
```

From the TUI, you can navigate the years and days to run any available solution.

#### Debug Mode

To run the TUI with debug mode enabled, use the `--debug` flag:

```bash
python main.py --debug
```

**Debug mode provides:**

- **Debug Log Panel**: A dedicated debug log panel at the bottom of the screen that displays troubleshooting information, including:
  - App initialization status
  - File selection events
  - ContentSwitcher state changes
  - Worker thread execution flow
  - Error messages and stack traces
  
- **Copy Debug Log Command**: Press `d` to copy the entire debug log to your clipboard for easy sharing or analysis. The "Copy Debug Log" command will appear in the footer after you press `d` for the first time.

Debug mode is useful for troubleshooting issues with script execution, understanding the application flow, or diagnosing problems with the spinner or content switching.

### Running Solutions Directly

You can also run any day's solution directly from the command line.

To do so, you must set the `PYTHONPATH` to include the project's root directory.

```bash
PYTHONPATH=. python <year>/<day_file>.py
```

For example:

```bash
PYTHONPATH=. python 2015/day01.py
```

## Configuration

To automatically download your puzzle input, you must set the `AOC_USER_ID` environment variable.

1.  **Find your Session ID:**
    - Log in to the [Advent of Code website](https'://adventofcode.com).
    - Open your browser's developer tools.
    - Go to the "Cookies" or "Application" -> "Storage" section.
    - Find the cookie named `session` for the `adventofcode.com` domain.
    - Copy the value of this cookie.

2.  **Set the Environment Variable:**

    - **For the current terminal session:**
      ```bash
      export AOC_USER_ID='your_session_id_here'
      ```
      (On Windows PowerShell, use `$env:AOC_USER_ID='your_session_id_here'`)

    - **To set it permanently:**
      Add the `export` command to your shell's startup file (e.g., `~/.zshrc`, `~/.bashrc`, `~/.profile`).

Once the environment variable is set, the scripts will be able to download your puzzle input automatically.
