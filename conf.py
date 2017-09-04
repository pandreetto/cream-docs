import sys
import os
extensions = []
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'CREAM_Guide'
copyright = u'2017, Paolo Andreetto'
author = u'Paolo Andreetto'
version = u'0.1'
release = u'0.1'
language = None
exclude_patterns = ['_build']
pygments_style = 'sphinx'
todo_include_todos = False
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_show_sourcelink = False
htmlhelp_basename = 'CREAM_Guidedoc'
latex_elements = {}
latex_documents = [
    (master_doc, 'CREAM_Guide.tex', u'CREAM_Guide Documentation', u'Paolo Andreetto', 'manual'),
]
man_pages = [
    (master_doc, 'cream_guide', u'CREAM_Guide Documentation', [author], 1)
]
texinfo_documents = [
    (master_doc, 'CREAM_Guide', u'CREAM_Guide Documentation',
     author, 'CREAM_Guide', 'One line description of project.',
     'Miscellaneous'),
]
