Economics behavioural experiment using oTree
============================================

About
-----

The repository https://github.com/peterjc/MDT-INTR-EXP-MET contains an
"Economics Experiment" including a single-player risk assessment lottery game,
and a multi-player cooperative game.

It was created at the `James Hutton Institute <https://hutton.ac.uk>`__, and
runs within `oTree <https://www.otree.org/>`__, an open-source platform for
web-based interactive tasks.

Our initial work was funded by the `Macaulay Development Trust
<https://www.macaulaydevelopmenttrust.org/>`__ under project
MDT-INTR-EXP-MET.

This example was created and revised within the `oTree Studio
<https://www.otreehub.com/studio/>`__ interactive environment, and then
exported and unzipped to record the changes under git version control. See
``CONTRIBUTING.rst`` for more details.


Installation
------------

You can install run an oTree server locally, or hosted in the cloud. It is
written in Python, and so `oTree is distributed on PyPI
<https://pypi.org/project/otree/>`__, from where it can be installed with:

.. code:: console

   $ pip install otree

Then change directory to a copy of this repository, and run a development
server (with additional debugging information via ``otree devserver``), or a
production server (with ``otree prodserver``).

Or, to run on the cloud, the example directory must be re-compressed (via
the ``otree zip`` command) and then uploaded to `oTree Hub
<https://www.otreehub.com/my_projects/>`__ for deployment on Heroku (a paid
service).
