"""
Simple interface for managing a bibtex database using ADS 
http://adsabs.harvard.edu

Author: Samuel Skillman <samskillman@gmail.com> 
Affiliation: University of Colorado at Boulder, DOE CSGF
Homepage: https://bitbucket.org/samskillman/pyads
License:
  Copyright (C) 2012 Samuel Skillman.  All Rights Reserved.

  This file is part of pyads.

  yt is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import urllib, urllib2
import string
import pickle, cPickle

match2 = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?bibcode=%s"+\
        "&data_type=BIBTEX&db_key=AST&nocookieset=1"

match = "http://adsabs.harvard.edu/cgi-bin/nph-bib_query?bibcode=%s"+\
        "&data_type=BIBTEX&db_key=AST&nocookieset=1"

absmatch = "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?bibcode=%s"+\
        "&data_type=BIBTEXPLUS&return_fmt=LONG&db_key=AST&nocookieset=1"

pdfmatch = "http://adsabs.harvard.edu/cgi-bin/nph-data_query?bibcode=%s"+\
        "&link_type=ARTICLE&db_key=AST&high="
pdf2match = "http://articles.adsabs.harvard.edu/cgi-bin/nph-iarticle_query?%s"+\
        "&amp;data_type=PDF_HIGH&amp;whole_paper=YES&amp;type=PRINTER&amp;filetype=.pdf"

def searchauthyear(guess):
    return "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key="+\
        "AST&qform=AST&author=%5E"+"%s&start_year=%s&end_year=%s" % (guess[:-4], guess[-4:], guess[-4:])

def searchauth(guess):
    return "http://adsabs.harvard.edu/cgi-bin/nph-abs_connect?db_key=AST"+\
        "&qform=AST&author=%5E"+"%s"%guess

class ADSNotFoundError(Exception):
    """ADS Entry not found"""
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class BibTex(dict):
    data = None
    bibfile = None
    _pdf = None
    def __init__(self, name, bibfile=None):
        self.name = name
        self.bibfile = bibfile
        self.parse()

    def get_data_from_ads(self):
        lines = []
        opener = urllib.FancyURLopener({})
        fixed = match % (self.name.replace("&", "%26"))
        f = opener.open(fixed)
        line = f.readline()
        if 'Retrieved 0 abstracts.' in line: 
            raise ADSNotFoundError(self.name)
        while len(line) == 0 or line[0] != '@':
            line = f.readline()
        lines.append(line)
        for l in f:
            lines.append(l)
            if l.strip() == '}':
                break
        self.data = lines

    def get_data_from_bib(self, bibfile):
        f = open(bibfile,'r')
        lines = []
        line = f.readline()
        while self.name not in line:
            line = f.readline()
        lines.append(line)
        for l in f:
            lines.append(l)
            if l.strip() == '}':
                break
        self.data = lines
        f.close()

    def get_data(self):
        if self.data is None:
            if self.bibfile is None: 
                self.get_data_from_ads()
            else:
                self.get_data_from_bib(self.bibfile)
        return self.data
        
    def get_value(self, line):
        vals = line.partition('=')
        return vals

    def fix_author_string(self, name):
        fix1 =  name.translate(None,"\"'\\{},^.~")
        return fix1

    def build_citekey(self):
        au = self['author'].split()[0].strip('{},"')
        yr = self['year'].split()[0].strip('{},"')
        ti = self['title'].split()[0].strip('{},"')
        self.citekey = au+yr+ti
    
    def parse(self):
        print('Parsing %s: ' % self.name)
        self.get_data()
        data = self.data
        for l in data:
            vals = self.get_value(l)
            if len(vals)<=2: continue
            k = vals[0].strip(); v = vals[2].strip('\n,')
            """
            Join together full string. Not currently used.
            elif len(vals) == 3:
                k = vals[0]; v = vals[2].strip('{},"')
            else:
                try:
                    k = vals[0]; v = " ".join([v.strip('{},"') for v in vals[2:]])
                except:
                    print vals[2:]
            """
            self[k] = v

        self['author'] = self.fix_author_string(self['author'])
        self.build_citekey()
        print(self.citekey)

    def write(self, f):
        for l in self.data:
            f.write(l)
        f.write("\n")

    def open(self):
        if self._pdf is None:
            self.download()
        uname = os.uname()
        if 'Linux' == uname[0]:
            os.system("google-chrome ./%s"%self._pdf)
        elif 'Darwin' == uname[0] :
            os.system("open ./%s"%self._pdf)
        else:
            print "Sorry, I don't know how to open a file."

    def download(self):
        fixed = self.name.replace("&", "%26")
        if not os.path.isdir('pdfs'):
            os.system('mkdir pdfs')
        self._pdf = ("pdfs/%s.pdf"%self.name).replace("&","\&")
        options = [pdfmatch % fixed, pdf2match % fixed]
        try:
            options += ['http://arxiv.org/pdf/%s'%self['eprint']]
        except:
            pass
        for url in options:
            try:
                u = urllib2.urlopen(url)
                localFile = open(self._pdf, 'w')
                localFile.write(u.read())
                localFile.close()
            except:
                print 'Failed to download from %s' % url

class ADSLibrary(dict):
    data = {}
    citekeys = {}
    def __init__(self, name):
        self.name = name 
        self.load()

    def add_entry(self, name):
        names = [v.name for v in self.data.values()]
        if name in names: return
        try:
            b = BibTex(name)
            self.citekeys[b.citekey] = b
            self.data[name] = b 
        except ADSNotFoundError as e:
            print 'ADS Entry not found:', e.value

    def add_bibtex(self, b):
        self.citekeys[b.citekey] = b
        self.data[b.name] = b 

    def get_cite(self, citekey):
        try: b = self.data[citekey]
        except KeyError:
            b = self.citekeys[citekey]
        print b.citekey, "\cite{%s}"%b.name
        return b
        
    def write_bib(self, fname=None):
        if fname is None:
            fname = self.name + '.bib'
        f = file(fname,'w')
        for k in sorted(self.data.keys()):
            self.data[k].write(f)
        f.close()

    def suggest_ads(self, guess):
        if any(c in string.digits for c in guess):
            print 'Search url in ads:\n' + \
                searchauthyear(guess) 
        else:
            print 'Search url in ads:\n' + \
                searchauth(guess) 

    def find(self, guess):
        good_keys = [k for k in self.data.keys() if guess in k] + \
                    [k for k in self.citekeys.keys() if guess in k]
        b = None
        if len(good_keys) == 0:
            print 'Key %s not found.' % guess 
            self.suggest_ads(guess)

        elif len(good_keys) == 1:
            b = self.get_cite(good_keys[0])
            self.suggest_ads(guess)
        else:
            print 'Multiple matches for %s found:' % guess
            b = []
            for k in good_keys:
                b.append(self.get_cite(k))
            self.suggest_ads(guess)
        return b
    
    def save(self):
        out = open("%s.pkl"%self.name, "wb")
        cPickle.dump(self.data, out, -1)
        out.close()

    def load(self):
        try:
            infile = open("%s.pkl"%self.name, "rb")
            self.data = cPickle.load(infile)
            infile.close()
            for k, v in self.data.iteritems():
                self.citekeys[v.citekey] = v
        except:
            print 'Could not find saved library. Creating new.'

    def import_bib(self, bibfile):
        bf = open(bibfile,'r')
        for l in bf.readlines():
            if l[0] == '@':
                try:
                    a = l.split('{')[1].split(',')[0]
                    b = BibTex(a, bibfile=bibfile)
                    self.add_bibtex(b)
                except ADSNotFoundError as e:
                    print 'ADS Entry not found:', e.value
        bf.close()

if __name__ == '__main__':
    lib = ADSLibrary('test')
    for t in ["2011ApJ...735...96S", "2008ApJ...689.1063S"]:
        lib.add_entry(t)
    lib.write_bib()
    lib.save()
    lib.find('Skillman')
    lib.find('Skillman2011')
    lib.find('Dinosaur')
    lib.find('2008ApJ...689.1063S')
    
    # lib.import_bib('library.bib')
    # lib.save()
    
