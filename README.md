bootstrap-upgrade
=================

This little script will do its best to update your bootstrap 2.x files to bootstrap 3.x files. There are no guarantees, of course, and you are likely to have to do some hand editing afterwards!

This work is based on the excellent work done by iatek in [bootstrap-3-upgrade](https://github.com/iatek/bootstrap-3-upgrade) 

The script was written to address two primary drawbacks of online conversion tools:
 - they can usually only process one file at a time (this script will iterate through directories); and
 - they can have a tendency to screw up formatting (especially where you're using html with a separate templating language interspersed, for example).

Requirements
============
Getting up and running is very simple.

You'll just need python installed and the pyquery and django utils module. Python comes pre-installed on OS X and most Linux distributions, so in most cases there's nothing to do, but see the python website if you're unsure.

To install the modules, you can type:

```sh
# pip install pyquery
# pip install django
```

(If you don't want to install the whole set of django modules, you can use ``` pip install django-utils ``` instead).

A note to users of OS X: If you get complaints and errors about 'clang', [there is a simple fix here.](http://jaranto.blogspot.co.uk/2012/08/os-x-unable-to-execute-clang-no-such.html)

Running the script
============

Download the script to your computer (or clone this repo) and type:

```sh
$ python upgrade.py /Path/to/file/or/directory
```
The script will iterate recursively through each file in the directory and subdirectories and attempt to upgrade them. Take care that each file in these subdirectories is an html/template file. The upgrade script currently opens every file it comes across (see todos)

Todos
=====
 - implement a filter so that only files with a given file extension are modified. For example, by specifying an extension of .html or .twig, and so on. 

Feedback
========

Feedback/bug reports/pull requests very welcome!

Have fun!
