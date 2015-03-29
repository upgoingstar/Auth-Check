import requests
import re
from bs4 import BeautifulSoup
import optparse
parser = optparse.OptionParser()
parser.add_option('-f', '--file', action="store", dest="Filename", help="File storing the list of URLs to be checked", default="spam")
parser.add_option('-t', '--target', action="store", dest="target", help="Which site do those URLs in -f switch belong to? Use this option for relative paths. Leave blank for Absolute paths. Ex. http://example.com", default="spam")
parser.add_option('-o', '--output-file', action="store", dest="output", help="Which site do those URLs in -f switch belong to? Use this option for relative paths. Leave blank for Absolute paths.", default="C:\\auth-report.csv")
parser.add_option('-s', '--search', action="store", dest="search", help="Define any search pattern, string / regex to be highlighted in the response pages.", default="spam")

print '--------------------------------------------------------------------------\n[+] Test Started..\n--------------------------------------------------------------------------\n'
options, args = parser.parse_args()
file = options.Filename
def dowork(pass_target,pass_file):
	fopen = open(pass_file, 'r')
	counter = 0
	outputfile = options.output
	fwrite = open(outputfile, 'w')
	for x in fopen.readlines():
		counter = counter + 1
		if (x.find('http://') == 0) or (x.find('https://') == 0) or (pass_target == 'no_site'):
			url = x.strip('\n')
		else:
			url = pass_target + x.strip('\n')
		try:
			req = requests.get(url)
			if (options.search == 'spam'):
				search_check = 'No Pattern Defined'
			else:
				search_check = req.text.find(options.search)
				res = re.search(options.search,req.text,re.I)
				if res:
					search_check = "Yes"
				else:
					search_check = "No"
			success = 'true'
		except Exception as e:
			print e
			success = 'false'
		if (success == 'false'):
			print (	'[-] ' + url.strip('\n') + ',' + ',' + '\n')
			fwrite.write('[-],' + str(counter) +',' + url.strip('\n') + 'No Result' + ',' + '\n')
		else:
			if (req.status_code == 200):
				print ('[+] ' + url.strip('\n') + ',' + str(req.status_code) + ',' + 'search_check' + '\n')
				fwrite.write('[+],' + str(counter) + ',' + url.strip('\n') + ',' + str(req.status_code) + ',' + 'search_check' + '\n')
			else:
				print ('[-] ' + url.strip('\n') + ',' + str(req.status_code) + ',' + 'search_check' + '\n')
				fwrite.write('[-],' + str(counter) +',' + url.strip('\n') + ',' + str(req.status_code) + ',' + 'search_check' + '\n')

	print '\n-----------------------------------------------\n[+] Test Completed for ' + str(counter) + ' urls. \n[+] Please find results in: ' + outputfile 

if (options.target != 'spam'):
	target = options.target
	ifhttp = target.find('http://')
	ifhttps = target.find('https://')
	if (ifhttp == 0) or (ifhttps == 0):
		dowork(target,file)
	else:
		print 'Please enter target as http://example.com'
else: 
	dowork('no_site',file)
