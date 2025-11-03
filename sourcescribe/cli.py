"""Command-line interface for SourceScribe."""

import sys
import click
from pathlib import Path
from typing import Optional
from sourcescribe import __version__
from sourcescribe.config.loader import ConfigLoader
from sourcescribe.config.models import SourceScribeConfig
from sourcescribe.engine.generator import DocumentationGenerator
from sourcescribe.watch.watcher import FileWatcher
from sourcescribe.utils.logger import setup_logger, get_logger
import logging


@click.group()
@click.version_option(version=__version__)
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--debug', is_flag=True, help='Enable debug output')
def main(verbose: bool, debug: bool):
    """SourceScribe - Auto-documentation engine using LLMs."""
    level = logging.DEBUG if debug else (logging.INFO if verbose else logging.WARNING)
    setup_logger(level=level)


@main.command()
@click.argument('project_path', type=click.Path(exists=True), default='.')
@click.option('--config', '-c', type=click.Path(), help='Configuration file path')
@click.option('--provider', type=click.Choice(['anthropic', 'openai', 'ollama']), 
              help='LLM provider')
@click.option('--model', help='Model name')
@click.option('--output', '-o', type=click.Path(), help='Output directory')
def generate(
    project_path: str,
    config: Optional[str],
    provider: Optional[str],
    model: Optional[str],
    output: Optional[str]
):
    """Generate documentation for a project."""
    logger = get_logger()
    
    try:
        # Load configuration
        if config:
            cfg = ConfigLoader.load_from_file(config)
        else:
            cfg = ConfigLoader.load_or_default()
        
        # Override with CLI arguments
        if provider:
            cfg.llm.provider = provider
        if model:
            cfg.llm.model = model
        if output:
            cfg.output.path = output
        
        # Set project path
        cfg.repository.path = str(Path(project_path).resolve())
        
        logger.info(f"Generating documentation for: {cfg.repository.path}")
        logger.info(f"Using {cfg.llm.provider} ({cfg.llm.model})")
        
        # Generate documentation
        generator = DocumentationGenerator(cfg)
        generator.generate_documentation()
        
        logger.info(f"Documentation generated at: {cfg.output.path}")
        click.echo(click.style('✓ Documentation generated successfully!', fg='green'))
        
    except ValueError as e:
        # Handle API key errors gracefully
        error_msg = str(e)
        if 'API_KEY' in error_msg:
            click.echo(click.style('\n✗ API Key Required', fg='red', bold=True), err=True)
            click.echo(f'\n{error_msg}\n', err=True)
            click.echo('To fix this, set your API key as an environment variable:\n', err=True)
            
            if 'ANTHROPIC' in error_msg:
                click.echo('  export ANTHROPIC_API_KEY="your-anthropic-api-key-here"', err=True)
                click.echo('\nGet your API key from: https://console.anthropic.com/settings/keys', err=True)
            elif 'OPENAI' in error_msg:
                click.echo('  export OPENAI_API_KEY="your-openai-api-key-here"', err=True)
                click.echo('\nGet your API key from: https://platform.openai.com/api-keys', err=True)
            
            click.echo('\nAlternatively, use Ollama for local LLMs (no API key needed):', err=True)
            click.echo('  sourcescribe generate --provider ollama --model llama2\n', err=True)
            sys.exit(1)
        else:
            logger.error(f"Generation failed: {e}")
            click.echo(click.style(f'✗ Error: {e}', fg='red'), err=True)
            sys.exit(1)
    except ImportError as e:
        # Handle missing SDK errors
        click.echo(click.style('\n✗ Missing Dependency', fg='red', bold=True), err=True)
        click.echo(f'\n{e}\n', err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        click.echo(click.style(f'✗ Error: {e}', fg='red'), err=True)
        sys.exit(1)


@main.command()
@click.argument('project_path', type=click.Path(exists=True), default='.')
@click.option('--config', '-c', type=click.Path(), help='Configuration file path')
@click.option('--provider', type=click.Choice(['anthropic', 'openai', 'ollama']), 
              help='LLM provider')
@click.option('--model', help='Model name')
def watch(
    project_path: str,
    config: Optional[str],
    provider: Optional[str],
    model: Optional[str]
):
    """Watch for changes and regenerate documentation automatically."""
    logger = get_logger()
    
    try:
        # Load configuration
        if config:
            cfg = ConfigLoader.load_from_file(config)
        else:
            cfg = ConfigLoader.load_or_default()
        
        # Override with CLI arguments
        if provider:
            cfg.llm.provider = provider
        if model:
            cfg.llm.model = model
        
        # Set project path
        cfg.repository.path = str(Path(project_path).resolve())
        
        logger.info(f"Watching: {cfg.repository.path}")
        logger.info(f"Using {cfg.llm.provider} ({cfg.llm.model})")
        
        # Create generator
        generator = DocumentationGenerator(cfg)
        
        # Initial generation
        logger.info("Generating initial documentation...")
        generator.generate_documentation()
        
        # Start watching
        def on_changes(files):
            logger.info(f"Changes detected in {len(files)} file(s)")
            generator.process_changes(files)
        
        watcher = FileWatcher(
            root_path=cfg.repository.path,
            callback=on_changes,
            watch_config=cfg.watch,
            repo_config=cfg.repository,
        )
        
        click.echo(click.style('👁  Watching for changes... (Press Ctrl+C to stop)', fg='blue'))
        watcher.run()
        
    except KeyboardInterrupt:
        logger.info("Watch mode stopped by user")
        click.echo(click.style('\n✓ Watch mode stopped', fg='yellow'))
    except ValueError as e:
        # Handle API key errors gracefully
        error_msg = str(e)
        if 'API_KEY' in error_msg:
            click.echo(click.style('\n✗ API Key Required', fg='red', bold=True), err=True)
            click.echo(f'\n{error_msg}\n', err=True)
            click.echo('To fix this, set your API key as an environment variable:\n', err=True)
            
            if 'ANTHROPIC' in error_msg:
                click.echo('  export ANTHROPIC_API_KEY="your-anthropic-api-key-here"', err=True)
                click.echo('\nGet your API key from: https://console.anthropic.com/settings/keys', err=True)
            elif 'OPENAI' in error_msg:
                click.echo('  export OPENAI_API_KEY="your-openai-api-key-here"', err=True)
                click.echo('\nGet your API key from: https://platform.openai.com/api-keys', err=True)
            
            click.echo('\nAlternatively, use Ollama for local LLMs (no API key needed):', err=True)
            click.echo('  sourcescribe watch --provider ollama --model llama2\n', err=True)
            sys.exit(1)
        else:
            logger.error(f"Watch failed: {e}")
            click.echo(click.style(f'✗ Error: {e}', fg='red'), err=True)
            sys.exit(1)
    except ImportError as e:
        # Handle missing SDK errors
        click.echo(click.style('\n✗ Missing Dependency', fg='red', bold=True), err=True)
        click.echo(f'\n{e}\n', err=True)
        sys.exit(1)
    except Exception as e:
        logger.error(f"Watch failed: {e}", exc_info=True)
        click.echo(click.style(f'✗ Error: {e}', fg='red'), err=True)
        sys.exit(1)


@main.command()
@click.argument('project_path', type=click.Path(exists=True), default='.')
@click.option('--force', '-f', is_flag=True, help='Overwrite existing config')
def init(project_path: str, force: bool):
    """Initialize a new SourceScribe configuration."""
    logger = get_logger()
    
    try:
        project_dir = Path(project_path).resolve()
        config_path = project_dir / '.sourcescribe.yaml'
        
        # Check if config exists
        if config_path.exists() and not force:
            click.echo(click.style(
                f'Configuration already exists at {config_path}\n'
                'Use --force to overwrite',
                fg='yellow'
            ))
            return
        
        # Create default config
        logger.info(f"Creating configuration at: {config_path}")
        config = ConfigLoader.create_default_config(str(config_path))
        
        click.echo(click.style(f'✓ Created configuration: {config_path}', fg='green'))
        click.echo('\nNext steps:')
        click.echo('  1. Edit .sourcescribe.yaml to customize settings')
        click.echo('  2. Set API keys as environment variables:')
        click.echo('     export ANTHROPIC_API_KEY="your-key"')
        click.echo('     export OPENAI_API_KEY="your-key"')
        click.echo('  3. Run: sourcescribe generate')
        
    except Exception as e:
        logger.error(f"Init failed: {e}", exc_info=True)
        click.echo(click.style(f'✗ Error: {e}', fg='red'), err=True)
        sys.exit(1)


@main.command()
@click.option('--config', '-c', type=click.Path(exists=True), help='Configuration file')
def validate(config: Optional[str]):
    """Validate configuration file."""
    logger = get_logger()
    
    try:
        # Load config
        if config:
            cfg = ConfigLoader.load_from_file(config)
            config_path = config
        else:
            found = ConfigLoader.find_config()
            if not found:
                click.echo(click.style('✗ No configuration file found', fg='red'), err=True)
                sys.exit(1)
            cfg = ConfigLoader.load_from_file(str(found))
            config_path = str(found)
        
        # Validate
        logger.info(f"Validating: {config_path}")
        
        # Check API keys
        if cfg.llm.provider in ['anthropic', 'openai'] and not cfg.llm.api_key:
            click.echo(click.style(
                f'⚠ Warning: No API key set for {cfg.llm.provider}',
                fg='yellow'
            ))
        
        # Check paths
        if not Path(cfg.repository.path).exists():
            click.echo(click.style(
                f'✗ Repository path does not exist: {cfg.repository.path}',
                fg='red'
            ), err=True)
            sys.exit(1)
        
        click.echo(click.style('✓ Configuration is valid', fg='green'))
        
        # Show summary
        click.echo(f'\nConfiguration Summary:')
        click.echo(f'  Provider: {cfg.llm.provider}')
        click.echo(f'  Model: {cfg.llm.model}')
        click.echo(f'  Repository: {cfg.repository.path}')
        click.echo(f'  Output: {cfg.output.path}')
        click.echo(f'  Watch enabled: {cfg.watch.enabled}')
        
    except Exception as e:
        logger.error(f"Validation failed: {e}", exc_info=True)
        click.echo(click.style(f'✗ Invalid configuration: {e}', fg='red'), err=True)
        sys.exit(1)


@main.command()
def info():
    """Show SourceScribe information."""
    click.echo(f'SourceScribe v{__version__}')
    click.echo('\nAuto-documentation engine using LLMs')
    click.echo('\nSupported LLM Providers:')
    click.echo('  • Anthropic Claude')
    click.echo('  • OpenAI GPT')
    click.echo('  • Ollama (local)')
    click.echo('\nSupported Languages:')
    click.echo('  • Python, JavaScript, TypeScript, Java, Go, Rust')
    click.echo('  • C/C++, C#, Ruby, PHP, Swift, Kotlin, and more')
    click.echo('\nDocumentation:')
    click.echo('  https://github.com/yourusername/sourcescribe')


if __name__ == '__main__':
    main()
