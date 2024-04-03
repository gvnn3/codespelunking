# Code Spelunking Scripts
Scripts for working with large source trees.

These scripts can quickly give an overview of a source tree as well as
build indices for large code bases, those of a million lines or more,
which is often untenable within typical IDEs.  In order to use the
scripts here you'll need to install:

[CSCOPE](https://cscope.sourceforge.net)

[GNU Global](https://www.gnu.org/software/global/)

[Doxygen](https://www.doxygen.nl)

as well as Python, version 3 or greater.

# Example Usage

Consider a really large source tree such as the FreeBSD operating system.  In the root of the source tree run the script in
the following way:

```
> cd /usr/src/
> what.py 
Type		Number		Lines
PHP include 		 458 		 94763
C 		 20094 		 12623630
C or C++ Header Files 		 18259 		 5051571
Shell Script 		 5455 		 694420
M4 		 542 		 165868
AWK 		 105 		 16690
C++ 		 5695 		 4215423
HTML 		 311 		 109670
Automake 		 233 		 19053
Python 		 248 		 64194
Emacs Lisp 		 4 		 1053
XML 		 35 		 5073
TCL 		 2 		 500
Makefile 		 636 		 55948
Objective C 		 139 		 19354
Java 		 15 		 4235

			Files	Lines
Identified Code		 52231 	 23141445

Unknown			 48113 	 14244133

Total			 100344 	 37385578
```

For working with such code bases we have the `code_spelunk.py` script
which will generate indices for both the CSCSOPE and Global tools
which can be accessed from Emacs, vi, nvi, vim and other text editors.
When spelunking an OS kernel, which has its own, internal, header
files include the `-k` flag:

```
> code_spelunk.py -c -k
```

User space programs, such as nginx, apache, etc. do not require the
`-k` flag.


