# gram: GitHub Repo Account Manager

Easily use different GitHub accounts (with different public keys) on different
local repositories.

## Installing

Only works in Python 3 and with SSH (not HTTPS).

`pip install .` or `pip install gram`!

## How to Use

Create a GitHub account:
Register a GitHub account with gram

```
gram register -u lily-mayfield -k ~/.ssh/some-key.pub -n "Lily Mayfield" -e lily.mayfield@gmail.com
```

List accounts:

```
gram list
```

While in a repository root:

```
gram assign lily-mayfield
```
