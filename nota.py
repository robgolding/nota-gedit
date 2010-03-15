VERSION = "0.1"
NOTA_EXTENSIONS = ['nota', 'note']

import os, sys

sys.path = ['/home/rob/Dropbox/bin'] + sys.path

import gedit, nota

class NotaPlugin(gedit.Plugin):
    
	def __init__(self):
		gedit.Plugin.__init__(self)
		self._instances = {}
	
	def connect_document(self, doc):
		"""Connect to document's 'saving' signal."""
		
		handler_id = doc.connect("saved", self.on_save)
		doc.set_data(self.__class__.__name__, handler_id)
	
	def activate(self, window):
		"""Activate plugin."""
		
		handler_id = window.connect("tab-added", self.on_window_tab_added)
		window.set_data(self.__class__.__name__, handler_id)
		for doc in window.get_documents():
			self.connect_document(doc)
	
	def on_save(self, doc, *args):
		"""Compile the file using Nota on save."""
		filename = doc.get_uri_for_display()
		if filename and os.path.basename(filename).split('.')[-1] in NOTA_EXTENSIONS:
			nota.convert_file(filename)
	
	def on_window_tab_added(self, window, tab):
		"""Connect the document in tab."""
		
		name = self.__class__.__name__
		doc = tab.get_document()
		handler_id = doc.get_data(name)
		if handler_id is None:
			self.connect_document(doc)
	
	def deactivate(self, window):
		pass
	
	def update_ui(self, window):
		pass
