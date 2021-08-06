Economics behavioural experiments using oTree
=============================================

About
-----

This repository contains assorted "Economics Experiments" created at the
`James Hutton Institute <https://hutton.ac.uk>`__. They run within the
`oTree <https://www.otree.org/>`__, an open-source platform for web-based
interactive tasks.

Our initial work was funded by the `Macaulay Development Trust
<https://www.macaulaydevelopmenttrust.org/>`__ under project
MDT-INTR-EXP-MET.

Currently these examples were created and revised within the `oTree Studio
<https://www.otreehub.com/studio/>`__ interactive environment, and then
exported to record the changes under git version control. You can download
(export) an experiment as a compressed tar-ball with the extension
``.otreezip``, but you cannot upload (import) back into oTree Studio.

We unzip these files to track changes to the internal files including
``.html`` templates and ``.py`` Python code. See ``CONTRIBUTING.rst`` for more
details.


Installation
------------

You can install run an oTree server locally, or hosted in the cloud. It is
written in Python, and so `oTree is distributed on PyPI
<https://pypi.org/project/otree/>`__, from where it can be install with:

.. code:: console

   $ pip install otree

Then change directory to one of our examples, and run either a development
server (with additional debugging information via ``otree devserver``), or
a production server (with ``otree prodserver``).

Or, to run on the cloud, the example directory must be re-compressed (via
``otree zip``) and can then be uploaded to `oTree Hub
<https://www.otreehub.com/my_projects/>`__ for deployment on Heroku (which
you must pay for).
