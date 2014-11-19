# LocalMH

LocalMH is an infrastructure for local (in a working tree) management of the content in http://MathHub.info.

The infrastructure consists of set of resources (Makefiles, LaTeX Packages, LaTeXML, sTeX) and a management tool lmh.

## Installation

There are several ways to install lmh. The easiest way is:

```bash
pip install lmh
lmh core --install
```

Note that the pip baased installation might require python development tools to be installed
(package python-dev on Ubuntu / Debian).

This will clone lmh from https://github.com/KWARC/localmh. To manually install lmh, simply installed the dependencies and then clone lmh to a directory of your choice. Then add the subdirectory bin to your $PATH.

Once lmh is installed, you will have to run

```bash
lmh setup --install
```

for lmh to install and configure run-time dependencies correctly.

### Upgrade

To upgrade only lmh itself run:

```bash
lmh selfupdate
```

Note that this will not automatically update dependencies. To update dependencies, run:

```bash
pip install --upgrade lmh
```

### Dependencies

Currently only *nix-based systems are supported.

#### Installer dependencies

The installer requires the following programs installed to function properly. Whenever possible the installer will warn if these are missing:

* pip
* git

#### Runtime dependencies

In addition to the installer dependencies the following are required for lmh to run properly:

* svn
* pdflatex, preferably TexLive 2013 or newer
* perl with cpanminus installed
* libxml2
* libxslt

### System-specific instructions

#### Ubuntu / Debian

On newer Ubuntu / Debian systems, all required packages may be installed with the following command:

```bash
sudo apt-get install python python-pip python-dev subversion git texlive cpanminus libxml2-dev libxslt-dev libgdbm-dev
```

Then you can install lmh normally using:

```bash
pip install lmh # May require sudo
lmh core --install
lmh setup --install
```

#### Mac
On Mac OS X you may use [Homebrew](http://brew.sh/) to install some of the required dependencies:

```bash
brew install python cpanminus libxml2 libxslt subversion git
```

If lmh setup fails for LibXML, you might have to:

```bash
brew link libxslt
brew link libxml
```

and re-run:

```
lmh setup --reinstall
```


and then

Furthermore, you will have to install MacTex from ()




## Help

Basic Instructions on how to use lmh can be found at [http://mathhub.info/help/offline-authoring](http://mathhub.info/help/offline-authoring).

## Directory Structure

Resources/directory structure:

* MathHub:		stored offline content from MathHub.info
* bin:			main scripts, auto-added to $PATH via the pip package
* docs:			Documentation, autogenerated
* lmh:			main source directory for lmh
* ext:			external Software
* sty:			LaTeX packages used in MathHub.info
* logs:			crash reports that will help developers improve lmh.
* styles:		for the notation definitions MMT uses for generating XHTML from OMDoc
* pip-package:	A pip package which serves as an installer for lmh

## License

GPL, version 3.0

For the full license text, please see [gpl-3.0.txt](gpl-3.0.txt).
