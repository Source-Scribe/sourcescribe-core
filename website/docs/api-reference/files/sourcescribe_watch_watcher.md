# File Watcher Documentation

## File Purpose and Overview
The `watcher.py` file in the `sourcescribe-core` project contains the implementation of the `FileWatcher` class, which is responsible for monitoring a file system directory for changes and triggering a callback function when changes are detected.

The `FileWatcher` class provides a way to watch a specified directory for file system events, such as file creation, modification, and deletion. It uses the `watchdog` library to observe the file system and detect changes. When changes are detected, the `FileWatcher` class calls a user-provided callback function, passing a set of changed file paths.

## Main Components

### `FileWatcher` Class
The `FileWatcher` class is the main component of this file. It has the following key functionality:

1. **Initialization**: The `__init__` method initializes the `FileWatcher` instance with the following parameters:
   - `root_path`: The root directory to be watched for changes.
   - `callback`: A function to be called when changes are detected.
   - `watch_config`: An optional `WatchConfig` object containing configuration settings for the watcher.
   - `repo_config`: An optional `RepositoryConfig` object containing configuration settings for the repository.

2. **Start Watching**: The `start` method sets up the file watcher and starts observing the file system for changes. It creates a `ChangeHandler` instance to handle the detected changes and an `Observer` instance from the `watchdog` library to monitor the file system.

3. **Stop Watching**: The `stop` method stops the file watcher and releases the resources used by the `Observer` instance.

4. **Blocking Mode**: The `run` method starts the file watcher and enters a blocking mode, where it continuously checks for pending changes and processes them. This method can be used to run the watcher in a blocking manner, and it can be stopped by pressing Ctrl+C.

5. **Context Manager**: The `FileWatcher` class implements the context manager protocol, allowing it to be used with the `with` statement. The `__enter__` method starts the watcher, and the `__exit__` method stops the watcher.

6. **Utility Methods**: The `is_running` method returns a boolean indicating whether the watcher is currently running.

### `ChangeHandler` Class
The `ChangeHandler` class is responsible for processing the file system events detected by the `Observer` instance. It has the following key functionality:

1. **Initialization**: The `ChangeHandler` is initialized with the following parameters:
   - `callback`: The function to be called when changes are detected.
   - `debounce_seconds`: The number of seconds to wait before processing changes to avoid duplicate events.
   - `include_patterns`: A set of file patterns to include in the watch.
   - `exclude_patterns`: A set of file patterns to exclude from the watch.

2. **Event Handling**: The `on_any_event` method is called by the `Observer` instance whenever a file system event is detected. This method adds the changed file path to a set of pending changes.

3. **Change Processing**: The `process_pending_changes` method processes the set of pending changes by calling the user-provided `callback` function with the set of changed file paths.

4. **Pending Changes Tracking**: The `has_pending_changes` method returns a boolean indicating whether there are any pending changes that need to be processed.

## Dependencies and Imports
The `watcher.py` file imports the following dependencies:

- `time`: Used for adding a delay between processing changes to avoid duplicate events.
- `typing`: Used for type annotations.
- `watchdog.observers`: Used for monitoring the file system for changes.
- `pathlib.Path`: Used for working with file paths.
- `sourcescribe.watch.handler`: Used for the `ChangeHandler` class.
- `sourcescribe.config.models`: Used for the `WatchConfig` and `RepositoryConfig` classes.
- `sourcescribe.utils.logger`: Used for logging.

## Usage Examples
Here's an example of how to use the `FileWatcher` class:

```python
from sourcescribe.watch.watcher import FileWatcher
from sourcescribe.config.models import WatchConfig, RepositoryConfig

def on_changes(changed_files: set[str]):
    print(f"Files changed: {', '.join(changed_files)}")

watch_config = WatchConfig(
    enabled=True,
    recursive=True,
    debounce_seconds=1,
)

repo_config = RepositoryConfig(
    include_patterns=["*.py", "*.md"],
    exclude_patterns=["*__pycache__*"],
)

with FileWatcher("/path/to/directory", on_changes, watch_config, repo_config) as watcher:
    watcher.run()
```

In this example, the `FileWatcher` is created with the following configuration:

- The root directory to watch is `/path/to/directory`.
- The `on_changes` function will be called whenever files are changed.
- The `WatchConfig` enables the watcher, sets it to watch recursively, and sets a debounce time of 1 second.
- The `RepositoryConfig` includes Python and Markdown files, and excludes any `__pycache__` directories.

The `FileWatcher` is then used as a context manager, and the `run` method is called to start the watcher in blocking mode.

## Important Implementation Details
1. **Debouncing**: The `ChangeHandler` class uses a debouncing mechanism to avoid processing duplicate events. This is achieved by waiting a specified number of seconds (`debounce_seconds`) before processing the pending changes.

2. **Include and Exclude Patterns**: The `ChangeHandler` class uses the `include_patterns` and `exclude_patterns` settings from the `RepositoryConfig` to filter the file system events that are processed.

3. **Logging**: The `FileWatcher` class uses the `sourcescribe.utils.logger` module to log relevant information about the watcher's state and actions.

4. **Blocking Mode**: The `run` method of the `FileWatcher` class enters a blocking mode, where it continuously checks for pending changes and processes them. This allows the watcher to run indefinitely until the user interrupts it (e.g., by pressing Ctrl+C).

5. **Context Manager**: The `FileWatcher` class implements the context manager protocol, allowing it to be used with the `with` statement. This simplifies the management of the watcher's lifecycle, as the `start` and `stop` methods are automatically called when entering and exiting the context, respectively.