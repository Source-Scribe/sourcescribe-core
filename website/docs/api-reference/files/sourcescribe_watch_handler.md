# SourceScribe File Change Event Handler

## Overview

The `ChangeHandler` class in the `handler.py` file is responsible for monitoring and handling file system change events in the SourceScribe project. It is designed to provide a flexible and efficient way to track modifications, creations, and deletions of files, and to notify a callback function when such changes occur.

## Main Components

### `ChangeHandler` Class

The `ChangeHandler` class is the main component of this file. It inherits from the `FileSystemEventHandler` class provided by the `watchdog` library, which allows it to listen for and respond to various file system events.

#### Initialization

The `ChangeHandler` class is initialized with the following parameters:

- `callback`: A function to be called when changes are detected.
- `debounce_seconds`: The number of seconds to wait before processing changes, to avoid unnecessary callbacks.
- `include_patterns`: A set of file patterns to include in the monitoring process.
- `exclude_patterns`: A set of file patterns to exclude from the monitoring process.

#### Event Handling Methods

The class overrides the following event handling methods from the `FileSystemEventHandler` class:

- `on_modified(self, event: FileSystemEvent) -> None`: Handles file modification events.
- `on_created(self, event: FileSystemEvent) -> None`: Handles file creation events.
- `on_deleted(self, event: FileSystemEvent) -> None`: Handles file deletion events.

These methods call the `_handle_change()` method to process the file system events.

#### Change Handling Logic

The `_handle_change()` method is responsible for processing file system changes. It checks if the file matches the include and exclude patterns, and then adds the file path to the `changed_files` set. It also updates the `last_change_time` attribute to track the time of the last change.

The `_should_process()` method is used to determine whether a file should be processed based on the include and exclude patterns.

The `process_pending_changes()` method is responsible for processing the accumulated changes. It checks if the debounce time has elapsed, and if so, it calls the provided `callback` function with the set of changed files.

The `has_pending_changes()` method can be used to check if there are any pending changes that have not yet been processed.

## Dependencies and Imports

The `ChangeHandler` class depends on the following imports:

- `time`: For tracking the time of the last change.
- `typing`: For type annotations.
- `watchdog.events`: For the `FileSystemEventHandler` and `FileSystemEvent` classes.
- `pathlib`: For working with file paths.
- `sourcescribe.utils.logger`: For the `get_logger()` function.

## Usage Example

Here's an example of how the `ChangeHandler` class can be used:

```python
from sourcescribe.watch.handler import ChangeHandler

def on_files_changed(changed_files: Set[str]):
    for file_path in changed_files:
        print(f"File changed: {file_path}")

handler = ChangeHandler(
    callback=on_files_changed,
    debounce_seconds=2.0,
    include_patterns={
        "*.py",
        "*.md",
    },
    exclude_patterns={
        "*__pycache__*",
        "*.pyc",
    },
)

# Start monitoring file system changes
handler.process_pending_changes()

# Check for pending changes periodically
while True:
    if handler.has_pending_changes():
        handler.process_pending_changes()
    time.sleep(0.1)
```

In this example, the `ChangeHandler` is initialized with a callback function `on_files_changed()`, which will be called whenever files are changed. The `include_patterns` and `exclude_patterns` parameters are used to specify which files should be monitored.

The `process_pending_changes()` method is called to start the monitoring process, and the `has_pending_changes()` and `process_pending_changes()` methods are used to check for and process any pending changes.

## Implementation Details

The `ChangeHandler` class uses the `watchdog` library to monitor file system events. It maintains a set of changed files (`changed_files`) and the time of the last change (`last_change_time`). The `_handle_change()` method is responsible for adding file paths to the `changed_files` set and updating the `last_change_time`.

The `process_pending_changes()` method checks if the debounce time has elapsed since the last change, and if so, it calls the provided `callback` function with the set of changed files. This helps to avoid unnecessary callbacks and improve the efficiency of the file monitoring process.

The `_should_process()` method is used to determine whether a file should be processed based on the include and exclude patterns. This allows the `ChangeHandler` to be configured to only monitor specific files or file types.