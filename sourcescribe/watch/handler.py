"""File change event handler."""

import time
from typing import Set, Callable, Optional
from watchdog.events import FileSystemEventHandler, FileSystemEvent
from pathlib import Path
from sourcescribe.utils.logger import get_logger


class ChangeHandler(FileSystemEventHandler):
    """Handles file system change events."""
    
    def __init__(
        self,
        callback: Callable[[Set[str]], None],
        debounce_seconds: float = 2.0,
        include_patterns: Optional[Set[str]] = None,
        exclude_patterns: Optional[Set[str]] = None,
    ):
        """
        Initialize change handler.
        
        Args:
            callback: Function to call with changed files
            debounce_seconds: Seconds to wait before processing changes
            include_patterns: File patterns to include
            exclude_patterns: File patterns to exclude
        """
        super().__init__()
        self.callback = callback
        self.debounce_seconds = debounce_seconds
        self.include_patterns = include_patterns or set()
        self.exclude_patterns = exclude_patterns or set()
        
        self.changed_files: Set[str] = set()
        self.last_change_time: float = 0
        self.logger = get_logger(__name__)
    
    def on_modified(self, event: FileSystemEvent) -> None:
        """Handle file modification."""
        if not event.is_directory:
            self._handle_change(event.src_path)
    
    def on_created(self, event: FileSystemEvent) -> None:
        """Handle file creation."""
        if not event.is_directory:
            self._handle_change(event.src_path)
    
    def on_deleted(self, event: FileSystemEvent) -> None:
        """Handle file deletion."""
        if not event.is_directory:
            self._handle_change(event.src_path, deleted=True)
    
    def _handle_change(self, file_path: str, deleted: bool = False) -> None:
        """
        Handle a file change.
        
        Args:
            file_path: Path to changed file
            deleted: Whether file was deleted
        """
        # Check if file matches patterns
        if not self._should_process(file_path):
            return
        
        # Add to changed files
        self.changed_files.add(file_path)
        self.last_change_time = time.time()
        
        action = "deleted" if deleted else "modified"
        self.logger.debug(f"File {action}: {file_path}")
    
    def _should_process(self, file_path: str) -> bool:
        """
        Check if file should be processed.
        
        Args:
            file_path: Path to file
            
        Returns:
            True if file should be processed
        """
        path = Path(file_path)
        
        # Check exclude patterns
        for pattern in self.exclude_patterns:
            if path.match(pattern):
                return False
        
        # If include patterns specified, check them
        if self.include_patterns:
            for pattern in self.include_patterns:
                if path.match(pattern):
                    return True
            return False
        
        return True
    
    def process_pending_changes(self) -> None:
        """Process pending changes if debounce time has elapsed."""
        if not self.changed_files:
            return
        
        # Check if enough time has passed
        elapsed = time.time() - self.last_change_time
        if elapsed >= self.debounce_seconds:
            # Process changes
            files_to_process = self.changed_files.copy()
            self.changed_files.clear()
            
            self.logger.info(f"Processing {len(files_to_process)} changed file(s)")
            self.callback(files_to_process)
    
    def has_pending_changes(self) -> bool:
        """Check if there are pending changes."""
        return len(self.changed_files) > 0
