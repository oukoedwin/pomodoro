# Pomodoro Command-Line Tool Documentation

## Overview
The Pomodoro command-line tool is a simple timer application that follows the Pomodoro technique to enhance productivity. It consists of configurable work and break sessions, with a user-friendly graphical interface for time tracking.

## Features
- Customizable session durations (work, short break, long break)
- UI display with a draggable window
- Motivational messages for work and break times
- Start/stop functionality
- Automatic session switching

## Installation
This tool requires Python and dependencies such as `AppKit`, `Quartz`, and `argparse`. Ensure you have these installed before running the script.

## Usage
Run the application from the command line with optional parameters:

```sh
python pomodoro.py --num_sessions <num> --work <minutes> --short_break <minutes> --long_break <minutes>
```

### Command-line Arguments
| Argument         | Type  | Default | Description |
|-----------------|-------|---------|-------------|
| `--num_sessions` | int   | 4       | Number of work sessions before a long break |
| `--work`        | int   | 30      | Duration of a work session in minutes |
| `--short_break` | int   | 5       | Duration of a short break in minutes |
| `--long_break`  | int   | 30      | Duration of a long break in minutes |

## User Interface
- The timer is displayed in a draggable window.
- The UI includes a large countdown timer, a start/stop button, and motivational messages below the timer.
- Background color is dark gray with light gray text for visibility.

## Functionality
- **Start Timer**: Click the "Start" button to begin a Pomodoro session.
- **Stop Timer**: Click "Stop" to pause the timer.
- **Automatic Switching**: The tool automatically transitions between work and break periods based on the session count.
- **Motivational Messages**: Work sessions display "YOU HAVE TO BE WILLING TO GO TO WAR WITH YOURSELF," while breaks show "TAKE A WELL DESERVED BREAK!"

## Example
Start a Pomodoro session with 25-minute work intervals, 5-minute short breaks, and a 15-minute long break after four sessions:

```sh
python pomodoro.py --num_sessions 4 --work 25 --short_break 5 --long_break 15
```

## Dependencies
Ensure you have the following installed:
```sh
pip install pyobjc-framework-AppKit pyobjc-framework-Quartz
```

## Notes
- The application uses the macOS-specific `AppKit` framework and may not work on other operating systems.
- The UI window remains on top for visibility.

## License
This tool is open-source and free to use. Contributions are welcome!

