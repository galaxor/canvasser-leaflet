#!/usr/bin/python3

import os
import psycopg2

from collections import namedtuple

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

lastaddr = None
lastapt = None
for row in namedtuplefetchall(cur):
  if row.address != lastaddr:
    print('-------------------------------------------------------------------')
    print('%-30s [ ] Flier Drop' % row.address)
  if row.apt != lastapt and row.apt != None:
    if row.address == lastaddr:
      print()
    print('  %-32s [ ] Flier Drop' % row.apt)

  name = ' '.join([row.firstname, row.lastname])
  person = '%s, %s, %d.' % (name, row.gender, row.age)
  v_may = [' ', 'X'][row.v_may]
  v_nov = [' ', 'X'][row.v_nov]
  v_aug = [' ', 'X'][row.v_aug]
  print('  FOF   %-20s Voted: [%s] May  [%s] Nov  [%s] Aug' % (person, v_may, v_nov, v_aug))
  print(' [   ]   Notes:')
  print()
  print()

  lastaddr = row.address
  lastapt = row.apt
