Puppet Configuration
====================

TODO (short introduction)

CREAM service parameters
------------------------

These are the basic configuration parameters related to the CREAM
service:

-  ``creamce::batch_system`` (string): The installed batch system,
   *mandatory*, one of "pbs", "slurm", "condor", "lsf"

-  ``creamce::host`` (string): The fully qualified Computing Element
   host name, default the host name

-  ``creamce::port`` (integer): The tomcat listen port, default 8443

-  ``creamce::site::name`` (string): The human-readable name of the
   site, default the host name

-  ``creamce::site::email`` (string): The main email contact for the
   site. The syntax is a coma separated list of email addresses, default
   undefined

-  ``creamce::sandbox_path`` (string): The directory where the sandbox
   files are staged on the CREAM CE node, default "/var/cream\_sandbox"

-  ``creamce::delegation::purge_rate`` (integer): Specifies in minutes
   how often the delegation purger has to run, default 10 minutes

-  ``creamce::lease::time`` (integer): The maximum allowed lease time in
   second. If a client specifies a lease time too big, this value is
   used instead, default 36000 seconds.

-  ``creamce::lease::rate`` (integer): Specifies in minutes how often
   the job purger has to run, default 30 minutes

The following parameters enable and configure the internal monitoring
system. Whenever a resource metric exceeds the related resource limit
the CREAM CE suspends the job submission.

-  ``creamce::enable_limiter`` (boolean): In order to disable the
   limiter, it is needed to set this parameter value to false and
   restart the service, default true

-  ``creamce::limit::load1`` (integer): Limiter threshold for the load
   average (1 minute), default 40

-  ``creamce::limit::load5`` (integer): Limiter threshold for the load
   average (5 minute), default 40

-  ``creamce::limit::load15`` (integer): Limiter threshold for the load
   average (15 minute), default 20

-  ``creamce::limit::memusage`` (integer): Limiter threshold for the
   memory usage, default 95 (percentage)

-  ``creamce::limit::swapusage`` (integer): Limiter threshold for the
   swap usage, default 95 (percentage)

-  ``creamce::limit::fdnum`` (integer): Limiter threshold for the number
   of file descriptors, default 500

-  ``creamce::limit::diskusage`` (integer): Limiter threshold for the
   disk usage, default 95 (percentage)

-  ``creamce::limit::ftpconn`` (integer): Limiter threshold for the
   number of concurrent ftp connections, default 30

-  ``creamce::limit::fdtomcat`` (integer): Limiter threshold for the
   number of file descriptors, default 800

-  ``creamce::limit::activejobs`` (integer): Limiter threshold for the
   number of active jobs, default -1 (unlimited)

-  ``creamce::limit::pendjobs`` (integer): Limiter threshold for the
   number of pending jobs, default -1 (unlimited)

The following parameters configure the internal job purger mechanism,
all the values are expressed in number of days

-  ``creamce::job::purge_rate`` (integer): Specifies in minutes how
   often the job purger has to run, default 300 minutes.

-  ``creamce::purge::aborted`` (integer): Specifies how often the job
   purger deletes the aborted jobs, default 10 days

-  ``creamce::purge::cancel`` (integer): Specifies how often the job
   purger deletes the cancelled jobs, default 10 days

-  ``creamce::purge::done`` (integer): Specifies how often the job
   purger deletes the executed jobs, default 10 days

-  ``creamce::purge::failed`` (integer): Specifies how often the job
   purger deletes the failed jobs, default 10 days

-  ``creamce::purge::register`` (integer): Specifies how often the job
   purger deletes the registered jobs, default 2 days

The following parameters configure the job wrapper:

-  ``creamce::jw::proxy_retry_wait`` (integer): The minimum time
   interval expressed in seconds, between the first attempt and the
   second one for retrieving the user delegation proxy, default 60

-  ``creamce::jw::isb::retry_count`` (integer): The maximum number of
   ISB file transfers that should be tried, default 2

-  ``creamce::jw::isb::retry_wait`` (integer): If during a input sandbox
   file transfer occurs a failure, the JW retries the operation after a
   while. The sleep time between the first attempt and the second one is
   the “initial wait time” (i.e. the wait time between the first attempt
   and the second one) expressed in seconds. In every next attempt the
   sleep time is doubled. Default 60 seconds.

-  ``creamce::jw::osb::retry_count`` (integer): The maximum number of
   ISB file transfers that should be tried, default 2

-  ``creamce::jw::osb::retry_wait`` (integer): If during a output
   sandbox file transfer occurs a failure, the JW retries the operation
   after a while. The sleep time between the first attempt and the
   second one is the “initial wait time” (i.e. the wait time between the
   first attempt and the second one) expressed in seconds. In every next
   attempt the sleep time is doubled. Default 300 seconds.

CREAM Database
--------------

The following parameters configure the CREAM back-end:

-  ``creamce::mysql::root_password`` (string): root password for the
   database administrator, *mandatory*

-  ``creamce::creamdb::password`` (string): The database user password
   for the main operator, *mandatory*

-  ``creamce::creamdb::minpriv_password`` (string): The database user
   password for the monitor agent, *mandatory*

-  ``creamce::mysql::max_active`` (integer): The maximum number of
   active database connections that can be allocated from this pool at
   the same time, or negative for no limit, default 200

-  ``creamce::mysql::min_idle`` (integer): The minimum number of
   connections that can remain idle in the pool, without extra ones
   being created, or zero to create none, default 30

-  ``creamce::mysql::max_wait`` (integer): The maximum number of
   milliseconds that the pool will wait for a connection to be returned
   before throwing an exception, or -1 to wait indefinitely, default
   10000

-  ``creamce::mysql::override_options`` (hash): see the override option
   defined in https://forge.puppet.com/puppetlabs/mysql,default

   ::

       {'mysqld' => {'bind-address' => '0.0.0.0', 'max_connections' => "450" }}

-  ``creamce::creamdb::name`` (string): The database name for the CREAM
   service, default "creamdb"

-  ``creamce::creamdb::user`` (string): The database user name with user
   acting as main operator, default "cream"

-  ``creamce::creamdb::host`` (string): The fully qualified host name
   for any CE databases, default the host name

-  ``creamce::creamdb::port`` (integer): The mysql listen port for any
   CE databases, default 3306

-  ``creamce::creamdb::minpriv_user`` (string): The database user name
   with user acting as monitor agent, default "minprivuser"

-  ``creamce::delegationdb::name`` (string): The database name for the
   Delegation Service, default "delegationcreamdb"

BLAH
----

These are the basic configuration parameters for BLAH:

-  ``blah::config_file`` (string): The path of the main BLAH
   configuration file, default "/etc/blah.config"

-  ``blah::logrotate::interval`` (integer): The interval in days for log
   rotation, default 365 days

-  ``blah::logrotate::size`` (string): The size of a log file in MB,
   default "10M"

-  ``blah::use_blparser`` (boolean): If true it enables the BLParser
   service otherwise BUpdater/BNotifier is used, default false

-  ``creamce::blah_timeout`` (integer): Represents the maximum time
   interval in seconds accepted by CREAM for the execution of commands
   by BLAH, default 300 seconds

-  ``creamce::job::prefix`` (string): The prefix to be used for the BLAH
   job id, default "cream\_"

-  ``blah::shared_directories`` (list): A list of of paths that are
   shared among batch system head and worker nodes; the empty list is
   the default value

The following parameters configure BLAH if BNotifier/BUpdater are
enabled:

-  ``blah::bupdater::loop_interval`` (integer): The interval in seconds
   between two BUpdater sessions, default 30 seconds.

-  ``blah::bupdater::notify_port`` (integer): The service port for the
   BNotifier, default 56554

-  ``blah::bupdater::logrotate::interval`` (integer): The interval in
   days for log rotation, default 50

-  ``blah::bupdater::logrotate::size`` (string): The size of a log file
   in MB, default "10M"

The following parameters configure BLAH if the BLParser is enabled:

-  ``blah::blp::host`` (string): The host name for the primary BLParser,
   *mandatory* if BLParser is used, default undefined

-  ``blah::blp::port`` (integer): The service port for the primary
   BLParser, default 33333

-  ``blah::blp::num`` (integer): The number of BLParser enabled
   instances, default 1

-  ``blah::blp::host1`` (string): The host name for the secondary
   BLParser, default undefined

-  ``blah::blp::port1`` (integer): The service port for the secondary
   BLParser, default 33334

-  ``creamce::listener_port`` (integer): The port used by CREAM to
   receive notifications about job status changes sent by the
   BLParser/JobWrapper, default 49152

-  ``creamce::blp::retry_delay`` (integer): The time interval in seconds
   between two attempts to contact the BLAH parser, default 60 seconds

-  ``creamce::blp::retry_count`` (integer): Represents the number of
   attempts to contact the BLAH parser (if it is not reachable) before
   giving up. If -1 is specified, CREAM will never give up , default 100

CREAM information system
------------------------

The following parameters configure the Resource BDII:

-  ``bdii::params::user`` (string): The local user running the BDII
   service, default "ldap"

-  ``bdii::params::group`` (string): The local group running the BDII
   service, default "ldap"

-  ``bdii::params::port`` (integer): The BDII service port, default 2170

-  ``creamce::use_locallogger`` (boolean): True if the local logger
   service must be installed and configured, default is false

-  ``creamce::info::capability`` (list): The list of capability for a
   CREAM site; it's a list of string, in general with format
   "name=value", default empty list

-  ``creamce::vo_software_dir`` (string): The base directory for
   installation of the software used by Virtual Organizations

-  ``creamce::workarea::shared`` (boolean): True if the working area is
   shared across different Execution Environment instances, typically
   via an NFS mount; this attribute applies to single-slot jobs, default
   false

-  ``creamce::workarea::guaranteed`` (boolean): True if the job is
   guaranteed the full extent of the WorkingAreaTotal; this attribute
   applies to single-slot jobs, default false

-  ``creamce::workarea::total`` (integer): Total size in GB of the
   working area available to all single-slot jobs, default 0

-  ``creamce::workarea::free`` (integer): The amount of free space in GB
   currently available in the working area to all single-slot jobs,
   default 0 GB

-  ``creamce::workarea::lifetime`` (integer): The minimum guaranteed
   lifetime in seconds of the files created by single-slot jobs in the
   working area, default 0 seconds

-  ``creamce::workarea::mslot_total`` (integer): The total size in GB of
   the working area available to all the multi-slot Grid jobs shared
   across all the Execution Environments, default 0GB

-  ``creamce::workarea::mslot_free`` (integer): The amount of free space
   in GB currently available in the working area to all multi-slot jobs
   shared across all the Execution Environments, default 0 GB

-  ``creamce::workarea::mslot_lifetime`` (integer): The minimum
   guaranteed lifetime in seconds of the files created by multi-slot
   jobs in the working area, default 0 seconds

Hardware table
~~~~~~~~~~~~~~

The hardware table contains any information about the resources of the
site; the parameter to be used is ``creamce::hardware_table``. The
hardware table is a hash table with the following structure:

-  the key of an entry in the table is the ID assigned to the
   homogeneous sub-cluster of machines (see GLUE2 execution
   environment).

-  the value of an entry in the table is a hash containing the
   definitions for the homogeneous sub-cluster, the supported mandatory
   keys are:

   -  ``ce_cpu_model`` (string): The name of the physical CPU model, as
      defined by the vendor, for example "XEON"

   -  ``ce_cpu_speed`` (integer): The nominal clock speed of the
      physical CPU, expressed in MHz

   -  ``ce_cpu_vendor`` (string): The name of the physical CPU vendor,
      for example "Intel"

   -  ``ce_cpu_version`` (string): The specific version of the Physical
      CPU model as defined by the vendor

   -  ``ce_physcpu`` (integer): The number of physical CPUs (sockets) in
      a work node of the sub-cluster

   -  ``ce_logcpu`` (integer): The number of logical CPUs (cores) in a
      worker node of the sub-cluster

   -  ``ce_minphysmem`` (integer): The total amount of physical RAM in a
      worker node of the sub-cluster, expressed in MB

   -  ``ce_os_family`` (string): The general family of the Operating
      System installed in a worker node ("linux", "macosx", "solaris",
      "windows")

   -  ``ce_os_name`` (string): The specific name Operating System
      installed in a worker node, for example "RedHat"

   -  ``ce_os_arch`` (string): The platform type of worker node, for
      example "x86\_64"

   -  ``ce_os_release`` (string): The version of the Operating System
      installed in a worker node, as defined by the vendor, for example
      "7.0.1406"

   -  ``nodes`` (list): The list of the name of the worker nodes of the
      sub-cluster

   the supported optional keys are:

   -  ``ce_minvirtmem`` (integer): The total amount of virtual memory
      (RAM and swap space) in a worker node of the sub-cluster,
      expressed in MB

   -  ``ce_outboundip`` (boolean): True if a worker node has out-bound
      connectivity, false otherwise, default true

   -  ``ce_inboundip`` (boolean): True if a worker node has in-bound
      connectivity, false otherwise default false

   -  ``ce_runtimeenv`` (list): The list of tags associated to the
      software packages installed in the worker node, the definitions
      for a tag is listed in the software table, default empty list

   -  ``ce_benchmarks`` (hash): The hash table containing the values of
      the standard benchmarks ("specfp2000", "specint2000",
      "hep-spec06"); each key of the table corresponds to the benchmark
      name, default empty hash

   -  ``subcluster_tmpdir`` (string): The path of a temporary directory
      shared across worker nodes (see GLUE 1.3)

   -  ``subcluster_wntmdir`` (string): The path of a temporary directory
      local to each worker node (see GLUE 1.3)

Software table
~~~~~~~~~~~~~~

The software table is a hash with the following structure:

-  the key of an entry in the table is the tag assigned to the software
   installed on the machines (see GLUE2 application environment); tags
   are used as a reference (``ce_runtimeenv``) in the hardware table.

-  the value of an entry in the table is a hash containing the
   definitions for the software installed on the machines, the supported
   keys are:

   -  ``name`` (string): The name of the software installed, for example
      the package name, *mandatory*

   -  ``version`` (string): The version of the software installed,
      *mandatory*

   -  ``license`` (string): The license of the software installed,
      default unpublished

   -  ``description`` (string): The description of the software
      installed, default unpublished

Queues table
~~~~~~~~~~~~

The queue table contains definitions for local user groups; the
parameter to be declared is ``creamce::queues``. The queues table is a
hash with the following structure:

-  the key of an entry in the table is the name of the batch system
   queue/partition.

-  the value of an entry in the table is a hash table containing the
   definitions for the related queue/partition, the supported keys for
   definitions are:

   -  ``groups`` (list): The list of local groups which are allowed to
      operate the queue/partition, each group *MUST BE* defined in the
      VO table.

Storage table
~~~~~~~~~~~~~

The storage table contains any information about the set of storage
elements bound to this site. The parameter to be declared is
creamce::se\_table
, the default value is an empty hash. The storage element table is a
hash with the following structure:
``creamce::queues``. The queues table is a hash with the following
structure:

-  the key of an entry in the table is the name of the storage element
   host.

-  the value of an entry in the table is a hash table containing the
   definitions for the related storage element, the supported keys for
   definitions are:

   -  ``type`` (string): The name of the application which is installed
      in the storage element ("Storm", "DCache", etc.)

   -  ``mount_dir`` (string): The local path within the Computing
      Service which makes it possible to access files in the associated
      Storage Service (this is typically an NFS mount point)

   -  ``export_dir`` (string): The remote path in the Storage Service
      which is associated to the local path in the Computing Service
      (this is typically an NFS exported directory).

   -  ``default`` (boolean): True if the current storage element must be
      considered the primary SE, default false. Just one item in the
      storage element table can be marked as primary.

Example
~~~~~~~

::

    ---
    creamce::queues :
        long :  { groups : [ dteam, dteamprod ] }
        short : { groups : [ dteamsgm ] }

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

CREAM security and accounting
-----------------------------

The following parameters configure the security layer and the pool
account system:

-  ``creamce::host_certificate`` (string): The complete path of the
   installed host certificate, default /etc/grid-security/hostcert.pem

-  ``creamce::host_private_key`` (string): The complete path of the
   installed host key, default /etc/grid-security/hostkey.pem

-  ``creamce::voms_dir`` (string): The location for the deployment of VO
   description files (LSC), default /etc/grid-security/vomsdir

-  ``creamce::gridmap_dir`` (string): The location for the pool account
   files, default /etc/grid-security/gridmapdir

-  ``creamce::gridmap_file`` (string): The location of the pool account
   description file, default /etc/grid-security/grid-mapfile

-  ``creamce::gridmap_extras`` (list): The list of custom entry for the
   pool account description file, default empty list

-  ``creamce::gridmap_cron_sched`` (string): The cron time parameters
   for the pool account cleaner, default "5 \* \* \* \*"

-  ``creamce::groupmap_file`` (string): The path of the groupmap file,
   default /etc/grid-security/groupmapfile

-  ``creamce::crl_update_time`` (integer): The CRL refresh time in
   seconds, default 3600 seconds

-  ``creamce::ban_list_file`` (string): The path of the ban list file,
   if gJAF/LCMAPS is used, default /etc/lcas/ban\_users.db

-  ``creamce::ban_list`` (list): The list of banned users, each item is
   a Distinguished Name in old openssl format. If not defined the list
   is not managed by puppet.

-  ``creamce::use_argus`` (boolean): True if Argus authorization
   framework must be used, false if gJAF must be used, default true

-  ``creamce::argus::service`` (string): The argus PEPd service host
   name, ``mandatory`` if ``creamce::use_argus`` is set to true

-  ``creamce::argus::port`` (integer): The Argus PEPd service port,
   default 8154

-  ``creamce::argus::timeout`` (integer): The connection timeout in
   seconds for the connection to the Argus PEPd server, default 30
   seconds

-  ``creamce::argus::resourceid`` (string): The ID of the CREAM service
   to be registered in Argus, default
   ``https://{ce_host}:{ce_port}/cream``

-  ``creamce::admin::list`` (list): The list of service administators
   Distinguished Name, default empty list

-  ``creamce::admin::list_file`` (string): The path of the file
   containing the service administrators list, default
   /etc/grid-security/admin-list

-  ``creamce::default_pool_size`` (integer): The default number of users
   in a pool account, used if ``pool_size`` is not define for a VO
   group, default 100

VO table
~~~~~~~~

The VO table contains any information related to pool accounts, groups
and VO data. The parameter to be declared is ``creamce::vo_table``, the
default value is an empty hash. The VO table is a hash, the key of an
entry in the table is the name or ID of the virtual organization, the
corresponding value is a hash table containing the definitions for the
virtual organization,the supported keys for definitions are:

-  ``servers`` (list): The list of configuration details for the VOMS
   servers. Each item in the list is a hash; the parameter and any
   supported keys of a contained hash are ``mandatory``. The supported
   keys are:

   -  ``server`` (string): The VOMS server FQDN

   -  ``port`` (integer): The VOMS server port

   -  ``dn`` (string): The distinguished name of the VOMS server, as
      declared in the VOMS service certificate

   -  ``ca_dn`` (string): The distinguished name of the issuer of the
      VOMS service certificate

-  ``groups`` (hash): The list of local groups and associated FQANs, the
   parameter is ``mandatory``, each key of the hash is the group name,
   each value is a hash with the following keys:

   -  ``gid`` (string): The unix group id, ``mandatory``

   -  ``fqan`` (list): The list of VOMS Fully Qualified Attribute Name,
      ``mandatory``

   -  ``pub_admin`` (boolean): True if the group is the defined
      administrator group, default false, just one administrator group
      is supported

-  ``users`` (hash): The description of pool accounts or a static users,
   the parameter is ``mandatory``, each key of the hash is the pool
   account prefix or the user name for a static user, each value is a
   hash with the following keys:

   -  ``name_pattern`` (list): The pattern used to create the user name
      of the pool account, the variables used for the substitutions are
      ``prefix``, the pool account prefix, and ``index``, a consecutive
      index described below; the expression is explained in the ruby
      `guide <https://ruby-doc.org/core-2.2.0/Kernel.html#method-i-sprintf>`__,
      default value is

      ::

          %<prefix>s%03<index>d

   -  ``fqan`` (list): The list of VOMS Fully Qualified Attribute Name
      associated with the user of the pool account. The first element of
      the list is considered the primary FQAN and it is used to
      calculate the primary group of the user; the other FQANs are used
      to calculate the secondary groups. The mapping between FQANs and
      groups refers to the ``groups`` hash for the given VO. For further
      details about the mapping algorithm refer to the authorization
      `guide <https://twiki.cern.ch/twiki/bin/view/EGEE/AuthZOH#Account_and_Group_Mapping>`__.
      The parameter is ``mandatory``

   -  ``accounts`` (list): The list of SLURM accounts associated with
      this set of users, the parameter is ``mandatory`` if
      ``slurm::config_accounting`` is set to true

   A pool account can be defined in two different ways. If the user IDs
   are consecutive the parameters required are:

   -  ``first_uid`` (integer): The initial number for the unix user id
      of the pool account, the other ids are obtained incrementally with
      step equals to 1

   -  ``pool_size`` (integer): The number of user in the current pool
      account, the default value is global definition contained into
      ``creamce::default_pool_size``. If the value for the pool size is
      equal to zero the current definition must be considered for a
      static user.

   If the user IDs are not consecutive their values must be specified
   with the parameter:

   -  ``uid_list`` (list): The list of user ID; the pool account size is
      equal to the number of elements of the list.

   In any case the user name is created using the pattern specified by
   the parameter ``name_pattern`` where the index ranges from 1 to the
   pool account size (included). It is possible to shift the range of
   the indexes using the parameter ``creamce::username_offset``.

-  ``vo_app_dir`` (\_string\_): The path of a shared directory available
   for application data for the current Virtual Organization, as
   describe by Info.ApplicationDir in GLUE 1.3.

-  ``vo_default_se`` (string): The default Storage Element associated
   with the current Virtual Organization. It must be one of the key of
   the storage element table

Example
~~~~~~~

::

    ---
    creamce::use_argus :                 false
    creamce::default_pool_size :         10
    creamce::username_offset :           1

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
                             name_pattern : "%<prefix>s%03%<index>d" },
                dteamsgmusr : { first_uid : 6100, fqan : [ "/dteam/sgm/ROLE=developer", "/dteam" ],
                                pool_size : 5, name_pattern : "%<prefix>s%02<index>d" },
                dteamprodusr : { fqan : [ "/dteam/prod/ROLE=developer", "/dteam" ],
                                 name_pattern : "%<prefix>s%02<index>d",
                                 uid_list  : [ 6200, 6202, 6204, 6206, 6208 ] }
            }
        }

CREAM with TORQUE
-----------------

The TORQUE cluster must be install before the deployment of CREAM,
there's no support in the CREAM CE puppet module for the deployment of
TORQUE. Nevertheless the module may be used to configure the TORQUE
client on CREAM CE node if and only if the node is different from the
TORQUE server node. The YAML parameter which enables the TORQUE client
configuration is ``torque::config::client``, if it is set to false the
configuration is disabled, the default value is true. The CREAM CE
puppet module can create queues and pool accounts in TORQUE, the YAML
parameter is ``torque::config::pool``, if it is set to false the feature
is disabled, the default value is true.

Other configuration parameters for TORQUE are:

-  ``torque::host`` (string): The TORQUE server host name, default value
   is the host name.

-  ``torque::multiple_staging`` (boolean): The BLAH parameter for
   multiple staging, default false

-  ``torque::tracejob_logs`` (integer): The BLAH parameter for tracejob,
   default 2

-  ``munge::key_path`` (string): The location of the munge key. If
   TORQUE client configuration is enabled the path is used to retrieve
   the manually installed key; ``mandatory`` if
   ``torque::config::client`` is set to true.

CREAM with SLURM
----------------

The SLURM cluster must be install before the deployment of CREAM,
there's no support in the CREAM CE puppet module for the deployment of
SLURM. The module provides an experimental feature for configuring SLURM
users and accounts if the accounting is enabled in SLURM. The YAML
parameter which enables the experimental feature is
``slurm::config_accounting``, the default value is false. If it is set
to true each user of the pool account is replicated in the SLURM
accounting system. The list of SLURM accounts associated to the new user
is specified by the parameter ``accounts`` of the ``users`` definition
of the VO table.

CREAM with HTCondor
-------------------

The HTCondor cluster must be install before the deployment of CREAM,
there's no support in the CREAM CE puppet module for the deployment of
HTCondor.

The features described in this section are subject to frequent changes
and must be considered unstable. Use them at your own risk.

GPU support configuration
~~~~~~~~~~~~~~~~~~~~~~~~~

The GPU support in the information system (BDII) can be enabled with the
configuration parameter ``creamce::info::glue21_draft``\ (boolean), the
default value is false. The GPU resources must be described in the
hardware table, inserting in the related sub-cluster hashes the
following parameter:

-  ``accelerators`` (\_hash\_): The hash table containing the
   definitions for any accelerator device mounted in the sub-cluster.
   Each item in the table is a key-value couple. The key is the
   accelerator ID of the device and the value consists on a hash table
   with the following mandatory definitions:

   -  ``type`` (string): The type of the device (GPU, MIC, FPGA)

   -  ``log_acc`` (integer): The number of logical accelerator unit in
      the sub-cluster

   -  ``phys_acc`` (integer): The number of physical accelerator device
      (cards) in the subcluster

   -  ``vendor`` (string): The vendor ID

   -  ``model`` (string): The model of the device

   -  ``version`` (string): The version of the device

   -  ``clock_speed`` (integer): The clock speed of the device in MHz

   -  ``memory`` (integer): The amount of memory in the device in MByte
