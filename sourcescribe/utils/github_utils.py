"""GitHub utilities for generating permalinks and repository information."""

import subprocess
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse


def get_github_url_from_git(repo_path: str = ".") -> Optional[str]:
    """
    Extract GitHub repository URL from git remote.
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        GitHub HTTPS URL or None if not found
    """
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return None
            
        remote_url = result.stdout.strip()
        
        # Convert SSH URL to HTTPS
        if remote_url.startswith("git@github.com:"):
            # git@github.com:user/repo.git -> https://github.com/user/repo
            remote_url = remote_url.replace("git@github.com:", "https://github.com/")
        
        # Remove .git suffix
        if remote_url.endswith(".git"):
            remote_url = remote_url[:-4]
            
        return remote_url if "github.com" in remote_url else None
        
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return None


def generate_github_permalink(
    file_path: str,
    github_url: str,
    branch: str = "main",
    line_start: Optional[int] = None,
    line_end: Optional[int] = None
) -> str:
    """
    Generate a GitHub permalink for a file and optional line range.
    
    Args:
        file_path: Relative path to the file from repository root
        github_url: Base GitHub repository URL (e.g., https://github.com/user/repo)
        branch: Branch name (default: main)
        line_start: Starting line number (1-indexed)
        line_end: Ending line number (1-indexed)
        
    Returns:
        GitHub permalink URL
    """
    # Normalize file path (remove leading ./ if present)
    file_path = file_path.lstrip("./")
    
    # Build base URL
    permalink = f"{github_url}/blob/{branch}/{file_path}"
    
    # Add line numbers if provided
    if line_start is not None:
        if line_end is not None and line_end != line_start:
            permalink += f"#L{line_start}-L{line_end}"
        else:
            permalink += f"#L{line_start}"
    
    return permalink


def format_github_link_markdown(
    file_path: str,
    github_url: str,
    branch: str = "main",
    line_start: Optional[int] = None,
    line_end: Optional[int] = None,
    link_text: Optional[str] = None
) -> str:
    """
    Generate a Markdown-formatted GitHub link.
    
    Args:
        file_path: Relative path to the file from repository root
        github_url: Base GitHub repository URL
        branch: Branch name (default: main)
        line_start: Starting line number (1-indexed)
        line_end: Ending line number (1-indexed)
        link_text: Custom link text (default: auto-generated from file and lines)
        
    Returns:
        Markdown link format: [text](url)
    """
    permalink = generate_github_permalink(file_path, github_url, branch, line_start, line_end)
    
    # Generate default link text if not provided
    if link_text is None:
        file_name = Path(file_path).name
        if line_start is not None:
            if line_end is not None and line_end != line_start:
                link_text = f"`{file_name}#L{line_start}-L{line_end}`"
            else:
                link_text = f"`{file_name}#L{line_start}`"
        else:
            link_text = f"`{file_path}`"
    
    return f"[{link_text}]({permalink})"


def get_current_commit_sha(repo_path: str = ".") -> Optional[str]:
    """
    Get the current commit SHA for more stable permalinks.
    
    Args:
        repo_path: Path to the repository root
        
    Returns:
        Commit SHA or None if not found
    """
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_path,
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return result.stdout.strip()
        return None
        
    except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
        return None
