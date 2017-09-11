CREAM installation
==================

Requirements
------------

The requirements for a basic installation of a CREAM site are:

-  A system based on Cent OS version 7 or compatibile distribution.

-  The UMD4 extension as described in the UMD
   `guide <http://repository.egi.eu/category/umd_releases/distribution/umd-4/>`__

Installation
------------

The basic installation of a CREAM site consists on the following
mandatory packages:

-  canl-java-tomcat
-  cleanup-grid-accounts
-  bdii
-  dynsched-generic
-  glite-ce-cream
-  glite-info-provider-service
-  globus-gridftp-server-progs
-  globus-proxy-utils
-  glue-schema
-  kill-stale-ftp
-  lcg-expiregridmapdir
-  mariadb
-  sudo

If the authorization framework used is based on glexec the following
packages are mandatory:

-  glexec

-  lcas-lcmaps-gt4-interface

-  lcas-plugins-basic

-  lcas-plugins-check-executable

-  lcas-plugins-voms

-  lcmaps-plugins-basic

-  lcmaps-plugins-verify-proxy

-  lcmaps-plugins-voms

if the authorization framework used is based on Argus the following
package is mandatory:

-  argus-gsi-pep-callout

The following packages are optional:

-  apel-parsers : if the support for APEL accounting is enabled

-  glite-lb-logger : if the support for the Logging and Bookkeping is
   enabled

-  info-dynamic-scheduler-lsf : if the batch system used is LSF

-  info-dynamic-scheduler-lsf-btools : if the batch system used is LSF

-  info-dynamic-scheduler-slurm : if the batch system used is SLURM

-  lcg-info-dynamic-scheduler-condor : if the batch system used is
   HTCondor

-  lcg-info-dynamic-scheduler-pbs : if the batch system used is TORQUE

The standard procedure for the installation and configuration of a CREAM
site makes use of the puppet framework. The puppet module checks for the
presence of the packages described above, and in case they're not
available on the system it installs them.
