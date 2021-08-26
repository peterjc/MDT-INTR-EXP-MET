.. image:: https://github.com/peterjc/MDT-INTR-EXP-MET/actions/workflows/github-actions.yml/badge.svg
   :alt: GitHub Actions Continous Integration Status
   :target: https://github.com/peterjc/MDT-INTR-EXP-MET/actions/workflows/github-actions.yml
.. image:: https://img.shields.io/github/license/peterjc/MDT-INTR-EXP-MET.svg
   :alt: MIT License
   :target: https://github.com/peterjc/thapbi-pict/blob/master/LICENSE.rst

Economics behavioural experiment using oTree
============================================

About
-----

The repository https://github.com/peterjc/MDT-INTR-EXP-MET contains an
"Economics Experiment" including a single-player risk assessment lottery game
based on Holt and Laury (2002), and a multi-player cooperative game.

It was created at the `James Hutton Institute <https://hutton.ac.uk>`__, and
runs within `oTree <https://www.otree.org/>`__, an open-source platform for
web-based interactive tasks. There is a `live demo on oTree Hub
<https://www.otreehub.com/projects/mdt-intr-exp-met/>`__.

Our initial work was funded by the `Macaulay Development Trust
<https://www.macaulaydevelopmenttrust.org/>`__ under project "Introducing
experimental methods for the study of resource and land-related decisions in
rural Scotland" (MDT project INTR-EXP-MET). The experimental team consists of
Simone Piras and Laure Kuhfuss (protocols), and Peter Cock (implementation).

This example was created and revised within the `oTree Studio
<https://www.otreehub.com/studio/>`__ interactive environment, and then
exported and unzipped to record the changes under git version control. See
``CONTRIBUTING.rst`` for more details.


Installation
------------

You can install run an oTree server locally, or hosted in the cloud. It is
written in Python, and so `oTree is distributed on PyPI
<https://pypi.org/project/otree/>`__. It can be installed along with the
other dependencies using:

.. code:: console

   $ pip install -r requirements.txt

Then change directory to a copy of this repository, and run a development
server (with additional debugging information via ``otree devserver``), or a
production server (with ``otree prodserver``).

Or, to run on the cloud, the example directory must be re-compressed (which
can be done with the ``otree zip`` command), and then uploaded to `oTree Hub
<https://www.otreehub.com/my_projects/>`__ for deployment on Heroku.


Usage
-----

Once the oTree server is running, the "Demo" page offers some pre-configured
examples with small number of players for testing purposes. The "Sessions"
page should be used to create real sessions, and allows access to the number
of players, participation fee, points to currency rate, and custom parameters.

The volunteering dilemma game includes multiple framings (called treatments in
the oTree documentation) which change the text but not the game rules and
payoffs. This is controlled with a custom integer session parameter "framing".
The default configuration offers multiple suggested sessions:

* ``farmer_framing`` using ``framing=0`` (for all participants)
* ``community_centre_framing`` using ``framing=1`` (for all participants)

We run parallel sessions for each framing, giving control over which session,
and thus which framing, each participant is assigned to.
