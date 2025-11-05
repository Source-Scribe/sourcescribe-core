# `sourcescribe/watch/__init__.py` Documentation

## File Purpose and Overview

This Python file is part of the `sourcescribe-core` project and serves as the entry point for the file system watching and change detection functionality. It provides access to the main components, the `FileWatcher` and `ChangeHandler` classes, which are responsible for monitoring file system changes and handling those changes, respectively.

## Main Components

### `FileWatcher` Class
The `FileWatcher` class is responsible for monitoring the file system for changes. It uses platform-specific file system watching mechanisms (e.g., `watchdog` on Unix-like systems, `win32_api` on Windows) to detect file creation, modification, and deletion events.

### `ChangeHandler` Class
The `ChangeHandler` class is responsible for handling file system changes detected by the `FileWatcher`. It provides a set of callback functions that can be used to define custom actions to be performed when specific types of changes occur.

## Key Functionality

The main functionality provided by this module includes:

1. **File System Monitoring**: The `FileWatcher` class monitors the file system for changes, such as file creation, modification, and deletion.
2. **Change Handling**: The `ChangeHandler` class provides a way to define custom actions to be performed when specific types of file system changes occur.

## Dependencies and Imports

This module imports the following components from other parts of the `sourcescribe-core` project:

- `sourcescribe.watch.watcher.FileWatcher`
- `sourcescribe.watch.handler.ChangeHandler`

## Usage Examples

To use the file system watching and change detection functionality provided by this module, you can import the `FileWatcher` and `ChangeHandler` classes and create instances of them, like this:

```python
from sourcescribe.watch import FileWatcher, ChangeHandler

# Create a file watcher
watcher = FileWatcher()

# Create a change handler
handler = ChangeHandler()

# Register callbacks for specific change events
handler.on_create(my_create_callback)
handler.on_modify(my_modify_callback)
handler.on_delete(my_delete_callback)

# Start watching the file system
watcher.start(handler)
```

In this example, `my_create_callback`, `my_modify_callback`, and `my_delete_callback` are custom functions that will be called when the corresponding file system events occur.

## Important Implementation Details

The `__all__` variable in this module is used to control which objects are imported when the module is imported using the `from sourcescribe.watch import *` syntax. By limiting the content to `["FileWatcher", "ChangeHandler"]`, the module ensures that only these two classes are imported, preventing potential naming conflicts with other parts of the `sourcescribe-core` project.