# Sphinx Documentation

This directory contains the Sphinx documentation for the ML Systems Evaluation Framework.

## Overview

The Sphinx documentation provides comprehensive, structured documentation for the ML Systems Evaluation Framework, including:

- Installation and setup guides
- Configuration documentation
- User guides and tutorials
- API reference
- Industry-specific guides
- Developer documentation

## Building the Documentation

### Prerequisites

Make sure you have the documentation dependencies installed:

```bash
# From the project root
uv sync --extra dev
```

### Build Commands

From the project root:

```bash
# Build HTML documentation
make docs-sphinx

# Build and serve documentation locally
make docs-sphinx-serve
```

From the `docs_sphinx` directory:

```bash
# Build HTML documentation
uv run make html

# Build with parallel processing
uv run make html-fast

# Build with full error checking
uv run make html-full

# Clean build artifacts
uv run make clean-all

# Serve documentation locally
uv run make serve

# Check links
uv run make check

# Spell check
uv run make spelling
```

## Documentation Structure

```
docs_sphinx/
├── source/
│   ├── index.rst              # Main documentation index
│   ├── conf.py                # Sphinx configuration
│   ├── installation.rst       # Installation guide
│   ├── configuration.rst      # Configuration guide
│   ├── getting-started.rst    # Getting started guide
│   ├── user-guides/           # User guides (to be created)
│   ├── developer/             # Developer docs (to be created)
│   ├── industries/            # Industry guides (to be created)
│   ├── reference/             # Reference docs (to be created)
│   ├── api/                   # API reference (to be created)
│   └── examples/              # Examples (to be created)
├── build/                     # Built documentation
├── Makefile                   # Build commands
└── README.md                  # This file
```

## Configuration

The Sphinx configuration is in `source/conf.py` and includes:

- Read the Docs theme
- AutoDoc for API documentation
- Napoleon for Google-style docstrings
- Intersphinx for external references
- MathJax for mathematical expressions
- GitHub integration

## Adding New Documentation

1. Create new `.rst` files in the appropriate directory
2. Add them to the relevant `toctree` in `index.rst`
3. Build and test the documentation
4. Commit your changes

## Integration with Existing Documentation

The Sphinx documentation complements the existing Markdown documentation in the `docs/` directory. The Sphinx docs provide:

- Structured, searchable documentation
- API reference with auto-generated docs
- Cross-references and linking
- Multiple output formats (HTML, PDF, etc.)

## Customization

### Theme Options

The documentation uses the Read the Docs theme with custom options defined in `conf.py`:

- Navigation depth: 4 levels
- Sticky navigation
- GitHub integration
- Custom styling

### Extensions

The following Sphinx extensions are enabled:

- `sphinx.ext.autodoc` - Auto-generate API docs
- `sphinx.ext.viewcode` - Link to source code
- `sphinx.ext.napoleon` - Google-style docstrings
- `sphinx.ext.intersphinx` - External references
- `sphinx.ext.todo` - TODO items
- `sphinx.ext.coverage` - Coverage reporting
- `sphinx.ext.mathjax` - Mathematical expressions
- `sphinx.ext.githubpages` - GitHub Pages integration

## Troubleshooting

### Common Issues

1. **Missing dependencies**: Run `uv sync --extra dev` to install all dependencies
2. **Build errors**: Check for syntax errors in `.rst` files
3. **Missing files**: Create placeholder files for referenced documents
4. **Theme issues**: Ensure `sphinx_rtd_theme` is installed

### Build Warnings

The build may show warnings for:
- Missing referenced documents (create placeholder files)
- Title underline length (fix underline length)
- Unknown theme options (check theme documentation)

## Contributing

When contributing to the documentation:

1. Follow the existing structure and style
2. Use reStructuredText syntax
3. Test your changes by building the docs
4. Update the table of contents as needed
5. Add cross-references where appropriate

## Deployment

The documentation can be deployed to:

- GitHub Pages (using `sphinx.ext.githubpages`)
- Read the Docs (automatic from GitHub)
- Any static hosting service

## Links

- [Sphinx Documentation](https://www.sphinx-doc.org/)
- [Read the Docs Theme](https://sphinx-rtd-theme.readthedocs.io/)
- [reStructuredText Primer](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)
