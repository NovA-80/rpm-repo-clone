RPM Repositories Cloning tool
=============================

Python command line tool to clone repositories in RPM-MD format with optionally selecting needed architectures. Tested on OpenSUSE-Leap repositories.

Inspired by [rrclone](https://github.com/eleksir/rrclone) Perl tool.

## Getting Started

Use
```
$ ./rpm-repo-clone.py  --arch x86_64 --arch noarch  http://source/repo/   path/to/destination/folder/
```
to clone repo from the Web keeping only 'x86_64' & 'noarch' package architectures.

Or to copy repo files from a local directory (e.g. on usb-stick) use
```
$ ./rpm-repo-clone.py   local/path/to/source/repo/   path/to/dest/folder/
```


## Requirements
- Python 3.6+
- `Requests` python module

## Usage

You need a correct path to RPM-MD repository. For example, take it from a `.repo`-file (located in '/etc/yum.repos.d' (RedHat) or '/etc/zypp/repos.d' (SUSE) dirs) as a string after "baseurl=". To check that URL is correct you can try to download repository xml metadata. Put your string into browser address bar and append "/repodata/repomd.xml" (no quotes) and if you see xml text then the URL is correct.

By default, the `rpm-repo-clone` downloads packages for all architectures available. If only several are required (e.g. 'x86_64' and 'noarch'), provide one or many `--arch <name>` options in the command line.

### Auxiliary `rpm-repo-clean` tool

This deletes files not listed in the repository metadata. It can help to clean-up a local repository storage created by direct packages downloading from the Web (e.g. by mirroring repo site contents via `wget`).

Note, `rpm-repo-clean` cleans only subdirectories, any top level objects remains unchanged.
