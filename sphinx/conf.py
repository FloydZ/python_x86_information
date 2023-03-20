import sphinx_bootstrap_theme
from opcodes import __version__


extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

source_suffix = '.rst'
master_doc = 'index'

project = u'Python x86 Instruction'
copyright = u'Floyd Zweydinger'

version = __version__
release = __version__

pygments_style = 'sphinx'

html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
