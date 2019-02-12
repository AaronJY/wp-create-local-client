from argparse import ArgumentParser
import urllib.request
import json

DOWNLOAD_ENDPOINT = "wp-json/pipdig-create-local/v1/download"
REQ_USERAGENT = 'Magic-Browser'

def get_download_url(site_url = "", dump_id = ""):
	return site_url + "/" + DOWNLOAD_ENDPOINT + "?dump_id=" + dump_id

def req(url):
	return urllib.request.Request(url, headers={'User-Agent' : REQ_USERAGENT})

parser = ArgumentParser()
parser.add_argument("siteurl", help="WordPress site URL (ex: https://my-site.com")
parser.add_argument("dumpid", help="Your dump ID")
parser.add_argument("--p", "--path", dest="outputpath", default="dump.zip", help="The destination you wish to save the downloaded dump file to")

args = parser.parse_args()

print("Getting dump download url...")

download_url = get_download_url(args.siteurl, args.dumpid)
download_req = req(download_url)

try:
	with urllib.request.urlopen(download_req) as resp:
		dl_resp_json = resp.read()
except urllib.error.HTTPError as e:
	if e.code == 404:
		print('Dump could not be found with given id {}'.format(args.dumpid))
		quit()
	else:
		print('HTTPError: {}'.format(e.code))
except urllib.error.URLError as e:
	print('URLError: {}'.format(e.reason))
	quit()

resp_data = json.loads(dl_resp_json)

if not "success" in resp_data:
	print("Something went wrong while obtaining the download URL")
	print(resp_data["message"])
	quit()

print("Downloading...")
direct_download_url = resp_data["data"]["url"]
direct_download_req = req(direct_download_url)
with urllib.request.urlopen(direct_download_req) as direct_dl_resp:
	dl_zip_data = direct_dl_resp.read()

with open(args.outputpath, 'wb') as fhandler:
	fhandler.write(dl_zip_data)

print("Done! Your dump has been saved to '" + args.outputpath + "'")