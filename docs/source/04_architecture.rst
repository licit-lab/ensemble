============
Architecture
============

The ENSEMBLE model is a software application containing the specifications from WP2 for deliverables `D2.4.`_.  designed as a Client Line Interface (CLI) application to be executed for a specific scenario and platform. This documentation has as a main objective to provide definitions and a description on the way the design requirements are achieved. 


Working principle
-----------------

This application defines the Multibrand Platoon functionality described by the ENSEMBLE project via a set of specifications that are implemented jointly within a python script exchanging information with a traffic simultor. For the use cases 2 traffic simulators have been selected. 

Traffic simulators
~~~~~~~~~~~~~~~~~~

Platform for simulation of specific traffic scenarios defined for the project. 

**Symuvia**
    Open source traffic simulation platform developed and mantained by the `LICIT team <LICITlink>`_ dedicated to integrate multiple models developed within the traffic flow theory community.

    .. figure:: img/symuvia.png
        :width: 700px
        :align: center
        :alt: alternate text
        :figclass: align-center

        Symuvia simulation example

**Vissim**
    Traffic simulator  developed by `PVT group <Vissimlink>`_ dedicated to model and simulate scenarios for the ENSEMBLE project. The platform serves mainly as an industrial reference for 
    benchmarking the platooning application. 

    .. figure:: img/vissim.png
        :width: 700px
        :align: center
        :alt: alternate text
        :figclass: align-center

        Vissim simulation example


Components & Connections
------------------------

The ENSMBLE application is defined via the following components: 



.. _D2.4.: https://platooningensemble.eu/storage/uploads/documents/2019/02/18/ENSEMBLE-D2.4---Functional-specification-for-white-label-truck_under-approval-by-EC.pdf

.. _LICITlink: https://www.licit.ifsttar.fr/linstitut/cosys/laboratoires/licit-ifsttar/plateformes/symuvia/

.. _Vissimlink: https://www.ptvgroup.com/en/solutions/products/ptv-vissim/