import json
import urllib
import urllib2
import base64
import webbrowser
import pyperclip

def parse_potential_engineers(results_filename):
	"""Goes through potential engineers one by one"""

	json_data = open(results_filename)
	results = json.load(json_data)
	json_data.close()

	for email in results:
 		if results[email] == None:
 			continue

 		print email
 		print results[email]

 		webbrowser.open(results[email]['github']) # open GitHub page in a new browser window
 		pyperclip.copy(email) # copy email address to clipboard
 		sys.stdin.readline()

def call_sourcingio(email):
	"""Calls Sourcing.io with an email
	Returns a user's title and relevant URLs, if any exist.
	Otherwise returns None """
	try:
		url = 'https://api.sourcing.io/v1/people/email/{0}'

		# TODO insert your API key here
		key = ''

		request = urllib2.Request(url.format(email))
		request.add_header('Authorization', 'Bearer {0}'.format(key))
		response_object = urllib2.urlopen(request)
		response = json.loads(response_object.read())
	except urllib2.HTTPError, err:
	   	if err.code == 404:
	   		return None
	   	else:
	  		raise err
	return {
		'headline': response['headline'], \
		'linkedin': 'https://www.linkedin.com/{0}'.format(response['linkedin']), \
		'github': 'https://github.com/{0}'.format(response['github']), \
		'twitter': 'https://twitter.com/{0}'.format(response['twitter']), \
		'url': response['url'] 
		}

def call_github(email):
	"""Calls GitHub with an email
	Returns a user's GitHub URL, if one exists.
	Otherwise returns None """
	url = 'https://api.github.com/search/users'
	values = {'q' : '{0} in:email type:user repos:>0'.format(email) }

	# TODO insert your credentials here or read them from a config file or whatever
	# First param is username, 2nd param is passwd
	# You can also do this without credentials, but then you'll be limited to 5 requests per minute
	auth_info = '{0}:{1}'.format('','')

	basic = base64.b64encode(auth_info)
	headers = { 'Authorization' : 'Basic ' + basic }
	params = urllib.urlencode(values)
	req = urllib2.Request('{0}?{1}'.format(url,params), headers=headers)
	response = json.loads(urllib2.urlopen(req).read())

	if response and response['total_count'] == 1:
		return response['items'][0]['html_url'] 
	else:
		return None	