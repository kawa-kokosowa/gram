import os
import sys
import configparser

GRAM_ACCOUNTS_INI = os.path.join(os.path.expanduser('~'), '.gram.ini')
SSH_CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.ssh', 'config')
SSH_CONFIG_HOST_TEMPLATE = '''
Host github-%s
    User git
    IdentitiesOnly yes
    Hostname github.com
    PreferredAuthentications publickey
    IdentityFile %s

'''
GIT_CONFIG = os.path.join('.git', 'config')


def new_ssh_config_host(username: str, public_key: str) -> None:
    """Add a new SSH config host, defining its username and key file.

    """

    try:
        with open(SSH_CONFIG_PATH) as f:
            ssh_config_contents = f.read()
        if 'Host github-%s' % username in ssh_config_contents:
            print("ERROR: SSH config host for %s already exists." % username)
            sys.exit(1)
    except FileNotFoundError:
        pass

    try:
        with open(SSH_CONFIG_PATH, 'a') as f:
            f.write(SSH_CONFIG_HOST_TEMPLATE % (username, public_key))
    except (OSError, IOError) as e:
        print('ERROR: cannot update %s (%s)' % (SSH_CONFIG_PATH, e))
        sys.exit(1)


def new_user(username: str, public_key: str, full_name: str, email: str) -> None:
    """Add a GitHub user to the gram ini.

    The format for a user entry looks like this:

      [lily-mayfield]
      public_key = ~/.ssh/somekey
      full_name = Lily Mayfield
      email = lily.m.mayfield@gmail.com

    Raises:
        SystemExit: Exits with error code 1 if INI cannot
            be read from, or if it cannot be written to.

    """

    # Read in the config
    parser = configparser.ConfigParser()
    parser.read(GRAM_ACCOUNTS_INI)

    # If user already in config, error-out, otherwise add the
    # user to the abstract...
    if username in parser:
        print(
            'Error: User %s (%s) already exists.'
            % (username, public_key)
        )
        sys.exit(1)
    else:
        parser.add_section(username)
        parser.set(username, 'public_key', public_key)
        parser[username]['public_key'] = public_key
        parser[username]['full_name'] = full_name
        parser[username]['email'] = email

    # Write out the changed config (user added!)
    try:
        with open(GRAM_ACCOUNTS_INI, 'w') as config_file:
            parser.write(config_file)
    except (OSError, IOError) as e:
        print('ERROR: cannot access %s (%s)' % (GRAM_ACCOUNTS_INI, e))
        sys.exit(1)  # Error 13: Permission Denied

    # Finally add an SSH host config for this user
    new_ssh_config_host(username, public_key)


def list_users() -> None:
    """Print all the users (and their keys)."""

    # Read in the config
    parser = configparser.ConfigParser()
    parser.read(GRAM_ACCOUNTS_INI)

    for section in parser.sections():
        username = section
        user_info = parser[section]
        print(
            '{username} ({full_name}) <{email}>; {public_key}'.format(
                username=username,
                full_name=user_info['full_name'],
                email=user_info['email'],
                public_key=user_info['public_key'],
            )
        )


def set_repo_user(username) -> None:
    """Set the local GitHub repo's account by modifying the
    host in .git/config.

    """

    # Check if in gram ini
    parser = configparser.ConfigParser()
    parser.read(GRAM_ACCOUNTS_INI)
    if username not in parser:
        print("This username is not registered with gram.")
        sys.exit(1)
    name = parser[username]['full_name']
    email = parser[username]['email']

    # Read in the config
    parser = configparser.ConfigParser()
    parser.read(GIT_CONFIG)

    # Use a custom host that corresponds with the
    # host specified in SSH config. It may look like this:
    # url = git@github.com:lily-mayfield/gram.git
    # Simply replace what's between @ and :.
    old_url = parser['remote "origin"']['url']
    new_url = (
        old_url[:old_url.index('@') + 1]
        + "github-" + username +
        old_url[old_url.index(':'):]
    )
    parser.set('remote "origin"', 'url', new_url)

    # Set user info too
    try:
        parser.add_section('user')
    except configparser.DuplicateSectionError as e:
        pass
    parser.set('user', 'name', name)
    parser.set('user', 'email', email)

    # Write out!
    try:
        with open(GIT_CONFIG, 'w') as config_file:
            parser.write(config_file)
    except (OSError, IOError) as e:
        print('ERROR: cannot access %s (%s)' % (GIT_CONFIG, e))
        sys.exit(1)
