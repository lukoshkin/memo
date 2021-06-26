#!/usr/bin/env python3

import sys
import argparse

from memorize import PatientLearner

parser = argparse.ArgumentParser()
parser.add_argument(
        '-t', '--expire-time',
        help='notification duration', default=10)
parser.add_argument(
        '-d', '--period',
        help='delay between showing notifications', default=30)
parser.add_argument(
        '--editable',
        help='edit word-translation pairs', action='store_true')

parser.add_argument('dict', help='dictionary')
args = parser.parse_args()

infile = sys.argv[1]
just_notify = not args.editable

trainer = PatientLearner(infile, args.expire_time, just_notify)
trainer.train(args.period)

