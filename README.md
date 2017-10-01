# gram: GitHub Repo Account Manager

Easily use different GitHub accounts (with different public keys) on different
local repositories.

## Installing

Only works in Python 3 and with SSH (not HTTPS).

`pip install .` or `pip install gram`!

## How to Use

Create a new GitHub account:

```
gram register --username slimemaid --key-file ~/.ssh/some-key.pub
```

List accounts:

```
gram list
```

While in a repository root:

```
gram assign slimemaid
```
