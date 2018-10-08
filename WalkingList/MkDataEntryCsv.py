#!/usr/bin/python3

import csv
import datetime
import os
import psycopg2
import sys

from collections import namedtuple

if len(sys.argv) > 1:
  canvasdate = sys.argv[1]
else:
  canvasdate = datetime.datetime.now().strftime('%Y-%m-%d')

canvasid = None
if len(sys.argv) > 2:
  canvasid = sys.argv[2]

queryfile = os.path.join(os.path.dirname(__file__), 'WalkingList.sql')
if len(sys.argv) > 3:
  queryfile = sys.argv[3]

def namedtuplefetchall(cursor):
  "Return all rows from a cursor as a namedtuple"
  desc = cursor.description
  nt_result = namedtuple('Result', [col[0] for col in desc])
  return [nt_result(*row) for row in cursor.fetchall()]

conn = psycopg2.connect('dbname=postgres user=postgres host=postgres password=%s' % os.environ['POSTGRES_ENV_POSTGRES_PASSWORD'])

cur = conn.cursor()

with open(queryfile, 'r') as qrfl:
  query = qrfl.read()

cur.execute(query)

csvwriter = None

for row in namedtuplefetchall(cur):
  if not csvwriter:
    # I'm going to print out only a subset of the fields from the query.
    # The purpose of this csv file is to be hand-edited to include a
    # friend-or-foe determination and other notes.  Some of these fields are
    # here for the data enterer to read.  Some fields are intended to be filled
    # out by the data enterer.  The fields the computer will care about are:
    # voterid, contacted, nosolicitors, fof, notes.
    # The reason I'm making a query for more fields than I need is that the
    # query is in a separate file, shared with the process that makes the
    # walking sheets.
    # fieldnames = [col[0] for col in cur.description]
    fieldnames = ['turf', 'canvasdate', 'voterid', 'address', 'apt', 'firstname', 'lastname', 'contacted', 'flierdrop', 'nosolicitors', 'fof', 'notes']
    csvwriter = csv.DictWriter(sys.stdout, fieldnames)
    csvwriter.writeheader()

  if canvasid and row.canvasid and int(row.canvasid) != int(canvasid):
    continue
  
  csvwriter.writerow({
    'turf':    'Turf %2d' % row.turfid,
    'voterid': row.voterid,
    'canvasdate': canvasdate,
    'voterid': row.voterid,
    'address': row.address,
    'apt': row.apt,
    'firstname': row.firstname,
    'lastname': row.lastname,
    'contacted': 0,
    'flierdrop': 1,
    'nosolicitors': 0,
    'fof': 3,
    'notes': '',
  })
