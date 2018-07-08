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

\\newcommand{\\ckbx}{\\framebox[1.2em]{\\parbox[c][0.5em][t]{1em}{ }}\\,}
\\newcommand{\\ckbxck}{\\framebox[1.2em]{\\parbox[c][0.5em][t]{1em}{X}}\\,}

\\begin{document}
""")

lastaddr = None
lastapt = None
print('\\vbox{')
for row in namedtuplefetchall(cur):
  if row.address != lastaddr:
    print('}')

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
    print('\\makebox[40ex][l]{\\makebox[4ex][r]{ }%s} \\ckbx Flier Drop' % escapelatex(row.apt))

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
  print('\\hspace{4ex}Notes: \\vspace{2em}')
  print()

  lastaddr = row.address
  lastapt = row.apt

print('}')
print('\\end{document}')
