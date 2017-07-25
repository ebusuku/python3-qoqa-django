#!/usr/bin/python3

import argparse

from qoqa import qoqa


def main():
    """
    Main Entry point for qoqa
    """
    parser = argparse.ArgumentParser(description="Qoqa is an application to"
                                     "create a new django project and to"
                                     "build the django project")
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--new', help='Create new django project')
    group.add_argument('--prepare', help='perform project checks')
    group.add_argument('--release', help='build .deb file of project')
    args = parser.parse_args()

    if args.new:
        print("Starting new django project")
        qoqa.new(args.new)
    elif args.prepare:
        qoqa.prepare()
    elif args.release:
        qoqa.release()


if __name__ == '__main__':
    main()
