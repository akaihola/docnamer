==========================================================
 docnamer – automatic content-based bulk document renamer
==========================================================

This software is meant for automatically giving sensible human-readable names to
different document files, e.g. those downloaded from on-line services.

The initial version only supports PDF receipts from the K-Ruoka on-line grocery
delivery service in Finland. Support for additional document types is planned.


Quickstart
==========

Install Python 3.x and pdfgrep_.

On the command line, go into a directory with files you want to rename. Run the script
e.g. with this command line::

    python3 ~/docnamer/rename_documents.py

You can also point the script to a directory to process. For example, in the project
directory you could start it like::

    python3 rename_documents.py ~/Dropbox/receipts/

You may see output like::

    Renaming 'k-ruoka-kuitti-8082221.pdf' to '2023-01-09 k-ruoka-kuitti-8082221.pdf'
    Renaming 'k-ruoka-kuitti-8113828.pdf' to '2023-01-16 k-ruoka-kuitti-8113828.pdf'
    2 PDF files renamed.
    19 PDF file names already have the correct date.    

On NixOS, you can simply run ``nix-shell`` in the root directory of this project to
both install dependencies and run the script in an isolated environment

.. _pdfgrep: https://pdfgrep.org/


How does it work?
=================

The script uses pdfgrep_ to go through all PDF files in the current directory (or the
directory specified on the command line). It looks for a single occurrence of a date (in
D.M.YYYY format) at the beginning of a line, and prepends it in the ISO format
(YYYY-MM-DD) to the file name. All files whose name doesn't yet conform to this naming
scheme are then renamed. Finally, a summary of the number of files processed and skipped
is shown.

The matching algorithm is suitable for K-Ruoka receipts, and may be modified in the
future to work with other kinds of documents.
