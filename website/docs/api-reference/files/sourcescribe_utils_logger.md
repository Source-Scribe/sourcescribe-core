# SourceScribe Logging Utilities

## File Purpose and Overview
The `logger.py` file in the `sourcescribe/utils` directory provides logging configuration and utilities for the SourceScribe project. It sets up a logger with optional Rich formatting for enhanced log output, and provides a function to easily retrieve a logger instance.

## Main Components

### `setup_logger` Function
```python
def setup_logger(
    name: str = "sourcescribe",
    level: int = logging.INFO,
    use_rich: bool = True
) -> logging.Logger:
    """
    Set up logger with optional Rich formatting.
    
    Args:
        name: Logger name
        level: Logging level
        use_rich: Use Rich handler for pretty output
        
    Returns:
        Configured logger
    """
    # Function implementation
```

The `setup_logger` function is responsible for configuring and returning a logger instance. It allows you to specify the logger name, logging level, and whether to use the Rich handler for enhanced log formatting.

### `get_logger` Function
```python
def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (defaults to sourcescribe)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name or "sourcescribe")
```

The `get_logger` function provides a convenient way to retrieve a logger instance. If no name is provided, it will use the default "sourcescribe" logger.

## Key Functionality
The main functionality of this module is to set up and manage logging for the SourceScribe project. It provides the following key features:

1. **Logger Configuration**: The `setup_logger` function allows you to configure a logger with custom settings, such as the logger name, logging level, and whether to use the Rich handler for enhanced log formatting.
2. **Logger Retrieval**: The `get_logger` function makes it easy to obtain a logger instance, either with a custom name or the default "sourcescribe" logger.
3. **Rich Formatting**: When the `use_rich` option is enabled, the logger will use the Rich handler, which provides a more visually appealing and informative log output, including rich tracebacks and support for ANSI escape codes.

## Dependencies and Imports
The `logger.py` file imports the following modules and dependencies:

- `logging`: The standard Python logging module, used for the core logging functionality.
- `sys`: Provides access to the standard error stream (`sys.stderr`), used for the default logging handler.
- `typing`: Includes the `Optional` type hint, used in the `get_logger` function.
- `rich.logging`: Provides the `RichHandler` class, which enables the Rich formatting for log output.
- `rich.console`: Includes the `Console` class, used to configure the Rich handler.

## Usage Examples
To use the logging utilities provided in this module, you can follow these steps:

1. Import the `setup_logger` and `get_logger` functions:
   ```python
   from sourcescribe.utils.logger import setup_logger, get_logger
   ```
2. Set up a logger using the `setup_logger` function:
   ```python
   logger = setup_logger(name="my-module", level=logging.DEBUG, use_rich=True)
   ```
3. Use the logger instance to log messages:
   ```python
   logger.debug("This is a debug message.")
   logger.info("This is an informational message.")
   logger.warning("This is a warning message.")
   logger.error("This is an error message.")
   logger.critical("This is a critical message.")
   ```

## Important Implementation Details
1. **Removing Existing Handlers**: The `setup_logger` function clears any existing handlers from the logger before adding a new one. This ensures that the logger is properly configured and doesn't have any leftover handlers from previous setups.
2. **Rich Formatting**: When the `use_rich` option is enabled, the logger uses the `RichHandler` from the `rich.logging` module. This handler provides a more visually appealing and informative log output, including rich tracebacks and support for ANSI escape codes.
3. **Default Logger Name**: If no logger name is provided to the `get_logger` function, it will use the default "sourcescribe" logger name.