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

Example
-------

This section illustrate an example of installation of a CREAM site by
means of a standalone execution of puppet. In the following examples the
FQDN of the CREAM site is myhost.mydomain.

The required steps are:

-  Installation of the packages for puppet:

   ::

       yum -y install puppet

-  Installation of the CREAM CE module for puppet:

   ::

       puppet module install infnpd-creamce

-  Creation of the required directories:

   ::

       mkdir -p /etc/puppet/manifests /var/lib/hiera/node /etc/grid-security

-  Creation of the file ``/etc/puppet/manifests/site.pp`` with the
   following definition

   ::

       node 'myhost.mydomain' {
         require creamce
       }

-  Creation of the file ``/etc/hiera.yaml`` with the following
   definitions:

   ::

       ---
       :backends:
         - yaml
       :hierarchy:
         - "node/%{fqdn}"
       :yaml:
         :datadir: /var/lib/hiera

-  Creation of the symbolic link

   ::

       ln -s /etc/hiera.yaml /etc/puppet/hiera.yaml

-  Creation of the CREAM CE description file
   ``/var/lib/hiera/node/myhost.mydomain.yaml``, an example of minimal
   configuration is:

   ::

       ---
       creamce::mysql::root_password :      mysqlp@$$w0rd
       creamce::creamdb::password :         creamp@$$w0rd
       creamce::creamdb::minpriv_password : minp@$$w0rd
       apel::db::pass :                     apelp@$$w0rd
       creamce::batch_system :              pbs
       creamce::use_argus :                 false
       creamce::default_pool_size :         10

       gridftp::params::certificate :       "/etc/grid-security/hostcert.pem"
       gridftp::params::key :               "/etc/grid-security/hostkey.pem"
       gridftp::params::port :              2811

       creamce::queues :
           long :  { groups : [ dteam, dteamprod ] }
           short : { groups : [ dteamsgm ] }

       creamce::vo_table :
           dteam : { 
               vo_app_dir : /afs/dteam, 
               vo_default_se : storage.pd.infn.it,
               servers : [
                             {
                                 server : voms.hellasgrid.gr,
                                 port : 15004,
                                 dn : /C=GR/O=HellasGrid/OU=hellasgrid.gr/CN=voms.hellasgrid.gr,
                                 ca_dn : "/C=GR/O=HellasGrid/OU=Certification Authorities/CN=HellasGrid CA 2016"
                             },
                             {
                                 server : voms2.hellasgrid.gr,
                                 port : 15004,
                                 dn : /C=GR/O=HellasGrid/OU=hellasgrid.gr/CN=voms2.hellasgrid.gr,
                                 ca_dn : "/C=GR/O=HellasGrid/OU=Certification Authorities/CN=HellasGrid CA 2016"
                             }
               ],
               groups : {
                   dteam : { fqan : [ "/dteam" ], gid : 9000 },
                   
                   dteamsgm : { fqan : [ "/dteam/sgm/ROLE=developer" ], gid : 9001, pub_admin : true },
                   
                   dteamprod : { fqan : [ "/dteam/prod/ROLE=developer" ], gid : 9002 }
               },
               users : {
                   dteamusr : { first_uid : 6000, fqan : [ "/dteam" ],
                                name_pattern : "%<prefix>s%03<index>d" },
                   
                   dteamsgmusr : { first_uid : 6100, fqan : [ "/dteam/sgm/ROLE=developer", "/dteam" ], 
                                   pool_size : 5, name_pattern : "%<prefix>s%02<index>d" },
                   
                   dteamprodusr : { first_uid : 6200, fqan : [ "/dteam/prod/ROLE=developer", "/dteam" ], 
                                    pool_size : 5, name_pattern : "%<prefix>s%02<index>d" }
               }
           }

       creamce::hardware_table :
           subcluster001 : {
               ce_cpu_model : XEON,
               ce_cpu_speed : 2500,
               ce_cpu_vendor : Intel,
               ce_cpu_version : 5.1,
               ce_physcpu : 2,
               ce_logcpu : 2,
               ce_minphysmem : 2048,
               ce_minvirtmem : 4096,
               ce_os_family : "linux",
               ce_os_name : "CentOS",
               ce_os_arch : "x86_64",
               ce_os_release : "7.0.1406",
               ce_outboundip : true,
               ce_inboundip : false,
               ce_runtimeenv : [ "tomcat_6_0", "mysql_5_1" ],
               subcluster_tmpdir : /var/tmp/subcluster001,
               subcluster_wntmdir : /var/glite/subcluster001,
               ce_benchmarks : { specfp2000 : 420, specint2000 : 380, hep-spec06 : 780 },
               nodes : [ "node-01.mydomain", "node-02.mydomain", "node-03.mydomain" ]
               # Experimental support to GPUs
               accelerators : {
                   acc_device_001 : {
                       type : GPU,
                       log_acc : 4,
                       phys_acc : 2,
                       vendor : NVidia,
                       model : "Tesla k80",
                       version : 4.0,
                       clock_speed : 3000,
                       memory : 4000 
                   }
               }
           }

       creamce::software_table :
           tomcat_6_0 : {
               name : "tomcat",
               version : "6.0.24",
               license : "ASL 2.0",
               description : "Tomcat is the servlet container" 
           }
           mysql_5_1 : {
               name : "mysql",
               version : "5.1.73",
               license : "GPLv2 with exceptions",
               description : "MySQL is a multi-user, multi-threaded SQL database server" 
           }

       creamce::vo_software_dir : /afs

       creamce::se_table :
           storage.pd.infn.it : { mount_dir : "/data/mount", export_dir : "/storage/export",
                                  type : Storm, default : true }
           cloud.pd.infn.it : { mount_dir : "/data/mount", export_dir : "/storage/export",
                                type : Dcache }

   The permissions of the file
   ``/var/lib/hiera/node/myhost.mydomain.yaml`` must be set to ``600``.

-  Deployment of the host private key in
   ``/etc/grid-security/hostkey.pem``

-  Deployment of the host certificate in
   ``/etc/grid-security/hostcert.pem``

-  Execution of puppet

   ::

       puppet apply /etc/puppet/manifests/site.pp
