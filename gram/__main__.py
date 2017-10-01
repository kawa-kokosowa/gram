"""gram: GitHub Repo Account Manager

Usage:
    gram register -u <username> -k <public-key> -n <full-name> -e <email>
    gram list
    gram assign <username>

Options:
    -h --help       Show this screen.
    --version       Show version.
    -u              GitHub username to create or assign to a repo.
    -k              Key associated with the GitHub username.
    -n              Full author's name for commits.
    -e              Author email for commits.

"""

import sys

from docopt import docopt

from . import __version__
from . import gram


def entrypoint():
    """The Python "entrypoint" (main) of this CLI script.

    """

    arguments = docopt(__doc__, version='gram ' + __version__)
    if arguments['register']:
        try:
            username = arguments['<username>']
            public_key = arguments['<public-key>']
            full_name = arguments['<full-name>']
            email = arguments['<email>']
        except KeyError:
            print(
                "When defining a new account you must use define username,"
                " public-key, full-name, and email."
                " See --help for more details."
            )
            sys.exit(1)
        else:
            gram.new_user(username, public_key, full_name, email)
            sys.exit(0)
    elif arguments['list']:
        gram.list_users()
    elif arguments['assign']:
        try:
            username = arguments['<username>']
        except KeyError:
            print(
                "When assigning a username to a repo you must specify "
                "username registered with gram."
            )
            sys.exit(1)
        else:
            gram.set_repo_user(username)
    elif arguments['--version']:
        print(__version__)
