CREAM monitoring
================

The CREAM CE site is monitored with the Nagios framework and a set of
specific probes. The service can be tested with job submission through
WMS or with direct submittion (i.e. using CREAM CLI). The probes
developed for the CREAM service must be installed on a User Interface
because they use the cream-cli commands to monitor the CREAM ce.

Requirements
------------

The required packages for the CREAM CE probes are:

-  python (version 2.4 or greater)

-  python-ldap

-  python-suds (version 0.3.5 or greater)

-  openssl (version 0.9.8e-12 or greater)

-  nagios-submit-conf (version 0.2 or greater)

-  python-GridMon (version 1.1.10)

About the last two rpms they can be install using the EGI
`repository <http://repository.egi.eu/sw/production/sam/1/repofiles/sam.repo>`__
