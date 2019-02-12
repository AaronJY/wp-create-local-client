from argparse import ArgumentParser
import distutils.util
import urllib.request
import json

DUMP_ENDPOINT = "wp-json/pipdig-create-local/v1/dump"
REQ_USERAGENT = 'Magic-Browser'

def get_dump_url(site_url = "", api_pass = "", artifacts = [], sql_dump = False):
	return site_url + "/" + DUMP_ENDPOINT + "?api_password=" + api_pass + "&artifacts=" + ','.join(artifacts) + '&sql_dump=' + ('1' if sql_dump == True else '0')

def req(url):
	return urllib.request.Request(url, headers={'User-Agent' : REQ_USERAGENT})

parser = ArgumentParser()
parser.add_argument('siteurl', help='WordPress site URL (ex: https://my-site.com')
parser.add_argument('apipassword', help='Your API password (can be found in the plugin settings page through your WP dash')
parser.add_argument('-a', '--artifacts', default='', dest="artifacts", help='A comma-separated list of the artifacts you want to dump. Possible artifacts: plugins, themes, languages, uploads')
parser.add_argument('-s', '--sqldump', default=False, dest="sqldump", help='Boolean value indicating whether you want to include a dump of the WP database')

args = parser.parse_args()

print("Creating dump...")


dump_url = get_dump_url(args.siteurl, args.apipassword, args.artifacts.split(','), distutils.util.strtobool(args.sqldump))

try:
	with urllib.request.urlopen(req(dump_url)) as resp:
		resp_json = resp.read()
except urllib.error.HTTPError as e:
	if e.code == 401:
		print('Unauthorized. Please check your API password and try again')
		quit()
	else:
		print('HTTPError: {}'.format(e.code))
except urllib.error.URLError as e:
	print('URLError: {}'.format(e.reason))
	quit()

json_data = json.loads(resp_json)

if not 'success' in json_data:
	print('Something went wrong: ' + json_data['message'])
	quit()

print('Successfully created dump with id: ' + json_data['data']['dump_id'])