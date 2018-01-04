import argparse
import sys
import json
from lib import myghdata, mydatabase


def process_arguments():

    parser = argparse.ArgumentParser(
        description='Collect various metrics for a GitHub repository'
    )

    parser.add_argument(
        '-c',
        '--config',
        type=argparse.FileType('r'),
        default='myconfig.json',
        dest='config_file',
        help='Path to configuration file'
    )

    parser.add_argument(
        '-r',
        '--repo',
        dest='ghFullRepoName',
        help='Full Name of the repo'
    )

    if len(sys.argv) < 2:   # Here 2 means no argument, 1 argument is the program name itself
        parser.print_help()
        sys.exit(1)

    return parser.parse_args()


def main():
    try:
        args = process_arguments()
        dbConfig = json.load(args.config_file)
        ghFullRepoName = args.ghFullRepoName
        print('\nFull Repo Name is {0}\n'.format(ghFullRepoName))

        repoData = myghdata.getRepoInfo(ghFullRepoName)
        if repoData is not None:
            print('\nWe got Repository Data from GitHub\n')
            mydatabase.insertRepo(dbConfig, repoData)
        else:
            print("GitHub Repository Info API call returned None")
            sys.exit(1)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
