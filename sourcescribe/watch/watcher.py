"""File system watcher."""

import time
from typing import Callable, Set, Optional
from watchdog.observers import Observer
from pathlib import Path
from sourcescribe.watch.handler import ChangeHandler
from sourcescribe.config.models import WatchConfig, RepositoryConfig
from sourcescribe.utils.logger import get_logger


class FileWatcher:
    """Watches file system for changes."""
    
    def __init__(
        self,
        root_path: str,
        callback: Callable[[Set[str]], None],
        watch_config: Optional[WatchConfig] = None,
        repo_config: Optional[RepositoryConfig] = None,
    ):
        """
        Initialize file watcher.
        
        Args:
            root_path: Root directory to watch
            callback: Function to call with changed files
            watch_config: Watch configuration
            repo_config: Repository configuration
        """
        self.root_path = Path(root_path).resolve()
        self.callback = callback
        self.watch_config = watch_config or WatchConfig()
        self.repo_config = repo_config or RepositoryConfig()
        
        self.logger = get_logger(__name__)
        self.observer: Optional[Observer] = None
        self.handler: Optional[ChangeHandler] = None
        self._running = False
    
    def start(self) -> None:
        """Start watching for file changes."""
        if self._running:
            self.logger.warning("Watcher is already running")
            return
        
        if not self.watch_config.enabled:
            self.logger.info("Watch mode is disabled")
            return
        
        self.logger.info(f"Starting file watcher on: {self.root_path}")
        
        # Create handler
        self.handler = ChangeHandler(
            callback=self.callback,
            debounce_seconds=self.watch_config.debounce_seconds,
            include_patterns=set(self.repo_config.include_patterns),
            exclude_patterns=set(self.repo_config.exclude_patterns),
        )
        
        # Create and start observer
        self.observer = Observer()
        self.observer.schedule(
            self.handler,
            str(self.root_path),
            recursive=self.watch_config.recursive,
        )
        self.observer.start()
        self._running = True
        
        self.logger.info("File watcher started")
    
    def stop(self) -> None:
        """Stop watching for file changes."""
        if not self._running:
            return
        
        self.logger.info("Stopping file watcher")
        
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=5.0)
        
        self._running = False
        self.logger.info("File watcher stopped")
    
    def run(self) -> None:
        """
        Run watcher in blocking mode.
        
        Watches for changes and processes them. Press Ctrl+C to stop.
        """
        self.start()
        
        if not self._running:
            return
        
        try:
            self.logger.info("Watching for changes... Press Ctrl+C to stop")
            
            while self._running:
                # Check for pending changes
                if self.handler and self.handler.has_pending_changes():
                    self.handler.process_pending_changes()
                
                # Sleep briefly
                time.sleep(0.5)
        
        except KeyboardInterrupt:
            self.logger.info("Received interrupt signal")
        finally:
            self.stop()
    
    def is_running(self) -> bool:
        """Check if watcher is running."""
        return self._running
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
