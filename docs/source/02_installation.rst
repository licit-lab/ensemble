.. highlight:: shell

============
Installation
============


Stable release
--------------

To install Ensemble Truck Platooning, run this command in your terminal:

.. code-block:: console

    $ pip install -e .

This is the preferred method to install Ensemble Truck Platooning, as it will always install the most recent stable release.

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for Ensemble Truck Platooning can be downloaded from the `Gitlab repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git@ci.tno.nl:paco.hamers-tno/ensemble_drivermodel.git

Or download the `tarball`_:

.. code-block:: console

    $ curl -OJL https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel/-/archive/master/ensemble_drivermodel-master.tar.gz

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install -e .   

You can run as well 

.. code-block:: console

    $ make develop       


.. _Gitlab repo: https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel
.. _tarball: https://ci.tno.nl/gitlab/paco.hamers-tno/ensemble_drivermodel/-/archive/master/ensemble_drivermodel-master.tar.gz
