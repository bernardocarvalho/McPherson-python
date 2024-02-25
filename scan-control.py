#!/usr/bin/env python3
"""
"""
import argparse
from mcpherson import mcpherson


parser = argparse.ArgumentParser(description='McPherson Scan controller')

# Switch
parser.add_argument('--Reset', action='store_true',
                    help='Reset Controller')
parser.add_argument('--Home', action='store_true',
                    help='Find Home Position ')
parser.add_argument('--steps', type=int,
                    help='Move n motor steps')

args = parser.parse_args()

mcp = mcpherson(serial_port='/dev/ttys001')

#if args.steps:
#    mcp.scanSteps(
if args.steps is not None:
    print(args.steps)
    mcp.scanSteps(args.steps)
#else:
#    print('no steps')

if args.Home:
    print('Go Home')
    mcp.findHome()

if args.Reset:
    print('Reset')
    mcp.reset()

mcp.close()

# vim: sta:et:sw=4:ts=4:sts=4
