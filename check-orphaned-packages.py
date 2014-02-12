#!/usr/bin/env python
import portage
import re
# For python2.6 compatibility
try:
	from urllib.request import urlopen
except:
	from urllib2 import urlopen

# Compatibility with bs3 users
try:
	from bs4 import BeautifulSoup
except:
	from BeautifulSoup import BeautifulSoup

# Make a list of orphaned packages by parsing xml with BeautifulSoup
url = 'http://www.gentoo.org/proj/en/qa/treecleaners/maintainer-needed.xml'

orphan_page = urlopen(url)
soup = BeautifulSoup(orphan_page)
orphan_page.close()
table = soup.find('table', 'ntable')
# compatibility for bs3 users
try:
	orphan_links = table.find_all('a', href=re.compile('https?://packages.gentoo.org'))
except:
	orphan_links = table.findAll('a', href=re.compile('https?://packages.gentoo.org'))
orphans = set([a.text for a in orphan_links])

# Build a list of packages that are installed
vartree = portage.db[portage.root]['vartree']
installed = set(vartree.dbapi.cp_all())

# Print list of all orphans that are installed
packages = sorted(orphans.intersection(installed))

# Python 2.6 requires the '0' in between curly braces to work
if packages:
    print("The following {0} installed package(s) need a maintainer".format(len(packages)))
    for package in packages:
        print("-{0}".format(str(package)))
    exit(1)
else:
    print("All installed packages have a maintainer :)")
    exit(0)
