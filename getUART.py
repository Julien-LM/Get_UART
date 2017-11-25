#!/usr/bin/env python

import sys


class Main:
    def __init__(self):
        print sys.argv

    def main(self, argv):
        print argv[1]


if __name__ == "__main__":
    Main().main(sys.argv)

