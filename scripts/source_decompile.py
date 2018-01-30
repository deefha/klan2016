#!/usr/bin/python

# common imports
import os, sys, datetime
from pprint import pprint
from colorama import init as colorama_init, Fore, Back, Style

# specific imports
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")
import tools.KlanTools as KlanTools
from decompilers import *



colorama_init(autoreset=True)

if len(sys.argv) != 3:
	# TODO message
	sys.exit()

ARG_ISSUE_NUMBER = sys.argv[1]
ARG_LIBRARY = sys.argv[2]

CONFIG_PATH = "../data/config.yml"
CHECK_PATH = "../data/sources/%s.check"
ISSUE_PATH = "../data/sources/%s.iso"



def decompile_loop(config, issue, library):
	if library == "all":
		for sources_library, sources in issue.sources.iteritems():
			if sources:
				for source_index, source in enumerate(sources):
					decompile(config, issue, source, source_index)
	else:
		if issue.sources[library]:
			for source_index, source in enumerate(issue.sources[library]):
				decompile(config, issue, source, source_index)

	return True



def decompile(config, issue, source, source_index):
	print "Issue: %s" % issue.number
	print "Path: %s" % source.path
	print "Library: %s" % source.library
	print "Version: %s" % source.version
	print "Index: %s" % source_index

	if source.library == "cursors":
		decompiler = CursorsDecompiler.CursorsDecompiler(issue, source, source_index)

	elif source.library == "fonts":
		decompiler = FontDecompiler.FontDecompiler(issue, source, source_index)

	elif source.library == "images":
		decompiler = ImgsDecompiler.ImgsDecompiler(issue, source, source_index)

	elif source.library == "audios":
		decompiler = WaveDecompiler.WaveDecompiler(issue, source, source_index)

	elif source.library == "music":
		decompiler = ModsDecompiler.ModsDecompiler(issue, source, source_index)

	else:
		return False

	decompiler.fill_meta_header()
	decompiler.fill_meta_fat()
	decompiler.fill_meta_data()
	decompiler.export_meta()

	return True



def main():
	config = KlanTools.config_load(CONFIG_PATH)

	if ARG_ISSUE_NUMBER == "all":
		for issue_id, issue in sorted(config.issues.iteritems()):
			decompile_loop(config, issue, ARG_LIBRARY)
	else:
		try:
			decompile_loop(config, config.issues[ARG_ISSUE_NUMBER], ARG_LIBRARY)
		except KeyError, e:
			print 'I got a KeyError - reason "%s"' % str(e) # TODO message



if __name__ == "__main__":
	main()
