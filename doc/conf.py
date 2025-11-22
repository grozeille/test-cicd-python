# Sphinx configuration for test-cicd-python
import os
import sys

project = 'test-cicd-python'
author = 'project'
release = '0.1'

# Add project root to sys.path so autodoc can import the package
sys.path.insert(0, os.path.abspath('..'))

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Try to use ReadTheDocs theme if available, fall back to alabaster
try:
    html_theme = 'sphinx_rtd_theme'
except Exception:
    html_theme = 'alabaster'

html_static_path = ['_static']

# Autodoc settings
autodoc_typehints = 'description'
