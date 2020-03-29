# -- Path setup --------------------------------------------------------------


# -- Project information -----------------------------------------------------
project = 'fastapi-for-firebase'
copyright = '2020, Kazuya Takei'
author = 'Kazuya Takei'
release = '0.0.2'

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",
]
templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
html_theme = 'alabaster'
html_static_path = ['_static']
