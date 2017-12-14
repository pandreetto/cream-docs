Releases
========

Release 1.16.6
--------------

The changes delivered with this release are:

-  Support for CentOS 7

-  Support for accelerator devices (NVidia GPUs, MIC)

-  Implementation of GLUE 2.1 v.0.4 (Draft)

The list of packages for the CREAM services is the following:

+-------------------------------------+---------------+-----------+
| Package                             | Version       | Arch      |
+=====================================+===============+===========+
| BLAH                                | 1.22.2-1      | x86\_64   |
+-------------------------------------+---------------+-----------+
| BLAH-debuginfo                      | 1.22.2-1      | x86\_64   |
+-------------------------------------+---------------+-----------+
| axis2                               | 1.6.4-2.emi   | noarch    |
+-------------------------------------+---------------+-----------+
| canl-java-tomcat                    | 0.2.1-1       | noarch    |
+-------------------------------------+---------------+-----------+
| condor-classads-blah-patch          | 0.0.1-1       | x86\_64   |
+-------------------------------------+---------------+-----------+
| dynsched-generic                    | 2.5.5-2       | noarch    |
+-------------------------------------+---------------+-----------+
| glite-ce-common-java                | 1.16.5-1      | noarch    |
+-------------------------------------+---------------+-----------+
| glite-ce-common-java-doc            | 1.16.5-1      | noarch    |
+-------------------------------------+---------------+-----------+
| glite-ce-cream                      | 1.16.5-3      | noarch    |
+-------------------------------------+---------------+-----------+
| glite-ce-cream-api-java             | 1.16.6-2      | noarch    |
+-------------------------------------+---------------+-----------+
| glite-ce-cream-core                 | 1.16.5-3      | noarch    |
+-------------------------------------+---------------+-----------+
| glite-ce-cream-utils                | 1.3.6-2       | x86\_64   |
+-------------------------------------+---------------+-----------+
| glite-ce-wsdl                       | 1.15.1-1      | noarch    |
+-------------------------------------+---------------+-----------+
| glite-info-dynamic-ge               | 7.2.0-29.1    | noarch    |
+-------------------------------------+---------------+-----------+
| glite-jdl-api-java                  | 3.3.2-3       | noarch    |
+-------------------------------------+---------------+-----------+
| glite-jdl-api-java-doc              | 3.3.2-3       | noarch    |
+-------------------------------------+---------------+-----------+
| info-dynamic-scheduler-lsf          | 2.3.8-3       | noarch    |
+-------------------------------------+---------------+-----------+
| info-dynamic-scheduler-lsf-btools   | 2.3.8-3       | noarch    |
+-------------------------------------+---------------+-----------+
| info-dynamic-scheduler-slurm        | 1.0.4-1       | noarch    |
+-------------------------------------+---------------+-----------+
| jclassads                           | 2.4.0-3       | noarch    |
+-------------------------------------+---------------+-----------+
| kill-stale-ftp                      | 1.0.1-1       | noarch    |
+-------------------------------------+---------------+-----------+
| lcg-info-dynamic-scheduler-condor   | 1.1-1         | noarch    |
+-------------------------------------+---------------+-----------+
| lcg-info-dynamic-scheduler-pbs      | 2.4.6-1       | noarch    |
+-------------------------------------+---------------+-----------+

The list of packages for the CREAM clients is the following:

+-----------------------------------+------------+-----------+
| Package                           | Version    | Arch      |
+===================================+============+===========+
| glite-ce-cream-cli                | 1.15.4-1   | x86\_64   |
+-----------------------------------+------------+-----------+
| glite-ce-cream-client-api-c       | 1.15.5-1   | x86\_64   |
+-----------------------------------+------------+-----------+
| glite-ce-cream-client-devel       | 1.15.5-1   | x86\_64   |
+-----------------------------------+------------+-----------+
| glite-jdl-api-cpp                 | 3.4.4-1    | x86\_64   |
+-----------------------------------+------------+-----------+
| glite-jdl-api-cpp-devel           | 3.4.4-1    | x86\_64   |
+-----------------------------------+------------+-----------+
| glite-jdl-api-cpp-doc             | 3.4.4-1    | x86\_64   |
+-----------------------------------+------------+-----------+
| glite-wms-utils-classad           | 3.4.3-1    | x86\_64   |
+-----------------------------------+------------+-----------+
| glite-wms-utils-classad-devel     | 3.4.3-1    | x86\_64   |
+-----------------------------------+------------+-----------+
| glite-wms-utils-exception         | 3.4.3-1    | x86\_64   |
+-----------------------------------+------------+-----------+
| glite-wms-utils-exception-devel   | 3.4.3-1    | x86\_64   |
+-----------------------------------+------------+-----------+
| log4cpp                           | 1.0.13-1   | x86\_64   |
+-----------------------------------+------------+-----------+
| log4cpp-devel                     | 1.0.13-1   | x86\_64   |
+-----------------------------------+------------+-----------+

The installation and configuration of the CREAM CE site is certified
with the puppet `module <https://forge.puppet.com/infnpd/creamce>`__
version 0.0.16 or greater.

The supported batch systems are:

+----------------+------------+
| Batch system   | Version    |
+================+============+
| TORQUE         | 4.2.10     |
+----------------+------------+
| SLURM          | 16.05.10   |
+----------------+------------+
| Htcondor       | 8.6.3      |
+----------------+------------+
| LSF            | 7.0        |
+----------------+------------+
| GridEngine     | 6.2        |
+----------------+------------+

The fixed issues are:

-  GGUS-Ticket-ID:
   `#106384 <https://ggus.eu/index.php?mode=ticket_info&ticket_id=106384>`__

-  GGUS-Ticket-ID:
   `#122974 <https://ggus.eu/index.php?mode=ticket_info&ticket_id=122974>`__

-  GGUS-Ticket-ID:
   `#124034 <https://ggus.eu/index.php?mode=ticket_info&ticket_id=124034>`__

-  GGUS-Ticket-ID:
   `#124404 <https://ggus.eu/index.php?mode=ticket_info&ticket_id=124404>`__

-  GGUS-Ticket-ID:
   `#127020 <https://ggus.eu/index.php?mode=ticket_info&ticket_id=127020>`__

The known issues are:

-  The CREAM UI requires classads libraries up to version 8.4.11, it
   does not work with versions 8.6.\*

-  GridEngine is partially supported, the infoprovider does not publish
   informationa about acceleratore devices.

-  The puppet agent may report parsing errors.

-  If HTCondor is the batch system adopted, the HTCondor services on the
   computing element must be restarted after the installation of the
   CREAM service.
