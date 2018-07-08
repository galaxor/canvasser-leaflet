#!/usr/bin/python3

import os
import psycopg2

from collections import namedtuple

def escapelatex(txt):
  escaped = txt.translate(str.maketrans({'\\':  '\\\\',
                                              '{': '\\{',
                                              '}': '\\}',
                                              '%': '%%',
                                              '#': '\\#',
                                            }))
  return escaped

def namedtuplefetchall(cursor):
  "Return all rows from a cursor as a namedtuple"
  desc = cursor.description
  nt_result = namedtuple('Result', [col[0] for col in desc])
  return [nt_result(*row) for row in cursor.fetchall()]

conn = psycopg2.connect('dbname=postgres user=postgres host=postgres password=%s' % os.environ['POSTGRES_ENV_POSTGRES_PASSWORD'])

cur = conn.cursor()

with open(os.path.join(os.path.dirname(__file__), 'WalkingList.sql'), 'r') as qrfl:
  query = qrfl.read()

cur.execute(query)

print("""
\\documentclass{article}

\\usepackage{fancyhdr}
\\pagestyle{fancy}

\\newcommand{\\ckbx}{\\framebox[1.2em]{\\parbox[c][0.5em][t]{1em}{ }}\\,}
\\newcommand{\\ckbxck}{\\framebox[1.2em]{\\parbox[c][0.5em][t]{1em}{X}}\\,}

\\begin{document}

\\fancyfoot[C]{}
\\fancyfoot[L]{FoF: 1=Will Campaign Against,  2=Will Vote Against,  3=Flippable,  4=Will Vote For,  5=Will Campaign For}

""")

lastturf = None
lastaddr = None
lastapt = None
laststreet = None
lastside = None
print('\\vbox{')
for row in namedtuplefetchall(cur):
  print('\\fancyhead[L]{TURF %d}' % row.turfid)
  print('\\fancyhead[C]{%s}' % row.prop_street)
  if row.prop_street_num % 2 == 0:
    print('\\fancyhead[R]{Even}')
  else:
    print('\\fancyhead[R]{Odd}')

  if row.address != lastaddr:
    print('}')
    if not (lastturf == None and lastaddr == None and lastapt == None and lastside == None)\
        and (row.turfid != lastturf\
          or row.prop_street != laststreet\
          or row.prop_street_num % 2 != lastside):
      print()
      print('\\newpage')

    print('\\vbox{')
    print('\\hrule')
    print('\\noindent')
    print('\\makebox[40ex][l]{\\bf %s} \\ckbx Flier Drop' % escapelatex(row.address))
  if row.apt != lastapt and row.apt != None:
    if row.address == lastaddr:
      print()
    print()
    print('\\noindent\\hspace*{4ex}\\hrulefill')
    print()
    print('\\noindent')
    print('\\makebox[40ex][l]{\\makebox[4ex][r]{ }\\bf %s} \\ckbx Flier Drop' % escapelatex(row.apt))

  print()
  print('\\noindent')

  name = ' '.join([row.firstname, row.lastname])
  person = escapelatex('%s, %s, %d.' % (name, row.gender, row.age))
  v_may = ['\\ckbx', '\\ckbxck'][row.v_may]
  v_nov = ['\\ckbx', '\\ckbxck'][row.v_nov]
  v_aug = ['\\ckbx', '\\ckbxck'][row.v_aug]

  print('\\makebox[40ex][l]{\\makebox[4ex][r]{ }%s} Voted: %s May\\quad %s Nov\\quad %s Aug' % (person, v_may, v_aug, v_nov))

  print()
  print('\\noindent')
  print('\\hspace{4ex}Friend or Foe of Shauna: \\framebox{1} \\framebox{2} \\framebox{3} \\framebox{4} \\framebox{5}')
  print()

  print('\\noindent')
  print('\\hspace{4ex}Friend or Foe of Ryan: \\framebox{1} \\framebox{2} \\framebox{3} \\framebox{4} \\framebox{5}')
  print()

  print()
  print('\\noindent')
  print('\\hspace{4ex}Notes: \\vspace{3em}')
  print()

  lastturf = row.turfid
  lastaddr = row.address
  laststreet = row.prop_street
  lastside = row.prop_street_num % 2
  lastapt = row.apt

print('}')
print('\\end{document}')
