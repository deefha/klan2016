#!/usr/bin/python

# common imports
import os, sys, datetime
from pprint import pprint
from colorama import init as colorama_init, Fore, Back, Style

# specific imports
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")
import tools.KlanTools as KlanTools
from remakers import *



colorama_init(autoreset=True)

if len(sys.argv) != 3:
	# TODO message
	sys.exit()

ARG_ISSUE_NUMBER = sys.argv[1]
ARG_LIBRARY = sys.argv[2]

CONFIG_PATH = "../data/config.yml"
CHECK_PATH = "../data/origins/%s.check"
ISSUE_PATH = "../data/origins/%s.iso"



def remake_loop_issues(config, issue_number, library):
	if issue_number == "all":
		for issue_id, issue in sorted(config.issues.iteritems()):
			remake_loop_libraries(config, issue, library)
	else:
		try:
			remake_loop_libraries(config, config.issues[issue_number], library)
		except KeyError, e:
			print 'I got a KeyError - reason "%s"' % str(e) # TODO message



def remake_loop_libraries(config, issue, library):
	if library == "all":
		for library, sources in issue.libraries.iteritems():
			if sources:
				for source_index, source in enumerate(sources):
					remake(config, issue, source, source_index)
	else:
		if issue.libraries[library]:
			for source_index, source in enumerate(issue.libraries[library]):
				remake(config, issue, source, source_index)

	return True



def remake(config, issue, source, source_index):
	print "Issue: %s" % issue.number
	print "Path: %s" % source.path
	print "Library: %s" % source.library
	print "Version: %s" % source.version
	print "Index: %s" % source_index

	if source.library == "cursors":
		remaker = CursorsRemaker.CursorsRemaker(issue, source, source_index)

	elif source.library == "fonts":
		remaker = FontsRemaker.FontsRemaker(issue, source, source_index)

	elif source.library == "images":
		remaker = ImagesRemaker.ImagesRemaker(issue, source, source_index)

	elif source.library == "audio":
		remaker = AudioRemaker.AudioRemaker(issue, source, source_index)

	elif source.library == "music":
		remaker = MusicRemaker.MusicRemaker(issue, source, source_index)

	else:
		return False

	remaker.fill_scheme()
	remaker.export_scheme()
	remaker.export_assets()

	return True



def main():
	config = KlanTools.config_load(CONFIG_PATH)
	remake_loop_issues(config, ARG_ISSUE_NUMBER, ARG_LIBRARY)



if __name__ == "__main__":
	main()