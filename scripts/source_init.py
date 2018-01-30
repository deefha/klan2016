#!/usr/bin/python

# common imports
import os, sys, datetime
from pprint import pprint
from tqdm import tqdm
from objdict import ObjDict
from colorama import init, Fore, Back, Style
init(autoreset=True)
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/../libs/")

# specific imports
#import pycdlib
#from io import BytesIO
#from structs.klan_mods_v1 import KlanModsV1
import requests, hashlib
from yaml import load


#iso = pycdlib.PyCdlib()
#extracted = BytesIO()

#iso.open("/mnt/bigboss/backup/deefha/klan2011/klan-00.iso")

##for child in iso.list_dir(iso_path='/'):
	##print(child.file_identifier())

#iso.get_file_from_iso_fp(extracted, iso_path="/MODS.LIB;1")
#iso.close()

#extracted.seek(0)

#library = KlanModsV1.from_io(extracted)



def issue_download(config, issue, issue_path):
	session = requests.Session()
	response = session.get(config.origin.main % issue.origin.id, stream = True)

	for key, value in response.cookies.items():
		if key.startswith(config.origin.confirm_key):
			response = session.get(config.origin.confirm % (issue.origin.id, value), stream = True)

	with open(issue_path, "wb") as f:
		with tqdm(total=issue.origin.size, unit="B", unit_scale=True, ascii=True, leave=False) as pbar: 
			for chunk in response.iter_content(32 * 1024):
				if chunk:
					f.write(chunk)
					pbar.update(len(chunk))



def issue_get_md5(config, issue, issue_path):
	hash_md5 = hashlib.md5()

	with tqdm(total=issue.origin.size, unit="B", unit_scale=True, ascii=True, leave=False) as pbar:
		with open(issue_path, "rb") as f:
			for chunk in iter(lambda: f.read(4 * 1024), b""):
				hash_md5.update(chunk)
				pbar.update(len(chunk))

		pbar.update(abs(issue.origin.size - pbar.n))

	return hash_md5.hexdigest()



# load YML data config
with open("../data/config.yml") as f:
	config_yaml = load(f)

# convert dict to ObjDict
# TODO load from JSON?
config = ObjDict()
config.origin = ObjDict()
config.origin.main = config_yaml["origin"]["main"]
config.origin.confirm = config_yaml["origin"]["confirm"]
config.origin.confirm_key = config_yaml["origin"]["confirm_key"]
config.issues = ObjDict()

for issue_yaml in config_yaml["issues"]:
	issue = ObjDict()
	issue.id = issue_yaml["id"]
	issue.origin = ObjDict()
	issue.origin.id = issue_yaml["origin"]["id"]
	issue.origin.size = issue_yaml["origin"]["size"]
	issue.origin.md5 = issue_yaml["origin"]["md5"]

	config.issues[str(issue.id)] = issue



# iterate over issues in config
for issue_id, issue in config.issues.iteritems():
	print Fore.BLACK + Back.GREEN + "Issue #%s" % issue.id

	issue_path = "../data/sources/%s.iso" % issue.id
	check_path = "../data/sources/%s.check" % issue.id

	# download missing issues
	if os.path.isfile(issue_path):
		print "\tSource exists"
	else:
		print "\tDownloading source..."
		issue_download(config, issue, issue_path)

	# skip checking if checked
	if os.path.isfile(check_path):
		with open(check_path, "r") as f:
			check_date = f.read()

		print Fore.GREEN + "\tChecked already (%s)" % check_date
		continue

	# check size by config
	if not os.path.isfile(issue_path):
		print Fore.RED + "\tCan not check size"
		continue
	else:
		print "\tChecking size..."

		while True:
			issue_size = os.path.getsize(issue_path)

			if issue_size == issue.origin.size:
				print "\tSize OK (%s)" % issue_size
				break
			else:
				print "\tSize error (%s != %s)" % (issue_size, issue.origin.size)
				print "\tDownloading source..."
				issue_download(config, issue, issue_path)

	# check md5 by config
	if not os.path.isfile(issue_path):
		print Fore.RED + "\tCan not check MD5 signature"
		continue
	else:
		print "\tChecking MD5 signature..."

		issue_md5 = issue_get_md5(config, issue, issue_path)

		if issue_md5 == issue.origin.md5:
			print "\tMD5 signature OK (%s)" % issue_md5
		else:
			print Fore.RED + "\tMD5 signature error (%s != %s)" % (issue_md5, issue.origin.md5)
			continue

	# write check file
	with open(check_path, "w") as f:
		print "\tWriting check file..."
		f.write(datetime.datetime.utcnow().replace(microsecond=0).isoformat())

	# issue done
	if not os.path.isfile(issue_path):
		print Fore.RED + "\tChecking error"
		continue
	else:
		print Fore.GREEN + "\tChecking OK"
