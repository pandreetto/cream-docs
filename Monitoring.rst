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

CREAM-CE direct job submission metrics and WN probes
----------------------------------------------------

The following metrics are a restructured version of the existing
`ones <https://wiki.italiangrid.it/twiki/bin/view/CREAM/DjsCreamProbe>`__
and provide a better approach for probing a CREAM CE and its WNs:

-  ``cream_serviceInfo.py`` - get CREAM CE service info

-  ``cream_allowedSubmission.py`` - check if the submission to the
   selected CREAM CE is allowed

-  ``cream_jobSubmit.py`` - submit a job directly to the selected CREAM
   CE

-  ``cream_jobCancel.py`` - cancel an active job.

-  ``cream_jobPurge.py`` - purge a terminted job.

-  ``WN-softver probe`` - check middleware version on WN (via
   cream\_jobSubmit.py)

-  ``WN-csh probe`` - check if WN has csh (via cream\_jobSubmit.py)

All of them have been implemented in python and are based on the
`cream-cli <User_Guide.html#cream-command-line-interface-guide>`__\ commands.
They share the same logic structure and provide useful information about
their version, usage (i.e. help) including the options list and their
meaning, according to the guide `Probes
Development <https://tomtools.cern.ch/confluence/display/SAMDOC/Probes+Development>`__.
For example:

::

    $ ./cream_serviceInfo.py 
    Usage: cream_serviceInfo.py [options]

    cream_serviceInfo.py: error: Specify either option -u URL or option -H HOSTNAME (and -p PORT) or read the help (-h)

    $ ./cream_serviceInfo.py --help
    Usage: cream_serviceInfo.py [options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -H HOSTNAME, --hostname=HOSTNAME
                            The hostname of the CREAM service.
      -p PORT, --port=PORT  The port of the service. [default: none]
      -x PROXY, --proxy=PROXY
                            The proxy path
      -t TIMEOUT, --timeout=TIMEOUT
                            Probe execution time limit. [default:
                            120 sec]
      -v, --verbose         verbose mode [default: False]
      -u URL, --url=URL     The status endpoint URL of the service. Example:
                            https://<host>[:<port>]

    $ ./cream_serviceInfo.py --version
    cream_serviceInfo v.1.0

The interaction with the CREAM CE requires the use of a valid VOMS proxy
expressed by the ``X509_USER_PROXY`` env variable or through the
``--proxy`` option. All metrics check the existence of the proxy file
and calculate the time left. In case of error, the related error message
will be thrown:

::

    $ ./cream_serviceInfo.py --hostname cream-41.pd.infn.it --port 8443 --proxy /tmp/x509up_u0 --verbose
    Proxy file not found or not readable

The verbose mode (``--verbose``) could be enabled to each metric. It
provides several details about the probe execution itself by
highlighting the internal commands:

::

    $ ./cream_serviceInfo.py --hostname cream-41.pd.infn.it --port 8443 -x /tmp/dteam.proxy --verbose
    executing command: /usr/bin/voms-proxy-info -timeleft
    invoking service info
    executing command: /usr/bin/glite-ce-service-info cream-41.pd.infn.it:8443
    OK: Service Version    = [1.16.1 - EMI version: 3.5.1-1.el6]

In case of mistakes on the selected options or on their values, the
probe tries to explain what is wrong. For example the cream\_serviceInfo
doesn't support the ``--queue`` option:

::

    $ ./cream_serviceInfo.py --hostname cream-41.pd.infn.it --port 8443 --queue creamtest1 -x /tmp/dteam.proxy --verbose
    Usage: cream_serviceInfo.py [options]

    cream_serviceInfo.py: error: no such option: --queue

In case of the errors in interacting with the CREAM CE, useful details
will be provided about the failure:

::

    $ ./cream_allowedSubmission.py --url https://cream-43.pd.infn.it:8443 -x /tmp/dteam.proxy
    command '/usr/bin/glite-ce-allowed-submission cream-43.pd.infn.it:8443' failed: return_code=1
    details: ['2014-01-16 15:59:57,085 FATAL - Received NULL fault; the error is due to another cause: FaultString=[connection error] - FaultCode=[SOAP-ENV:Client] - FaultSubCode=[SOAP-ENV:Client] - FaultDetail=[Connection refused]\n']

Sources are available in
`github <https://github.com/italiangrid/cream-nagios/tree/master/src>`__

cream\_serviceInfo.py
~~~~~~~~~~~~~~~~~~~~~

The serviceInfo.py retrieves information about the status of the CREAM
CE. The help shows how the probe must be invoked:

::

    $ ./cream_serviceInfo.py --help
    Usage: cream_serviceInfo.py [options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -H HOSTNAME, --hostname=HOSTNAME
                            The hostname of the CREAM service.
      -p PORT, --port=PORT  The port of the service. [default: none]
      -x PROXY, --proxy=PROXY
                            The proxy path
      -t TIMEOUT, --timeout=TIMEOUT
                            Probe execution time limit. [default:
                            120 sec]
      -v, --verbose         verbose mode [default: False]
      -u URL, --url=URL     The status endpoint URL of the service. Example:
                            https://<host>[:<port>]

In order to get information about the CREAM service on the host
https://cream-41.pd.infn.it:8443, use the following command:

::

    $ ./cream_serviceInfo.py --url https://cream-41.pd.infn.it:8443 -x /tmp/dteam.proxy
    OK: Service Version    = [1.16.1 - EMI version: 3.5.1-1.el6]

or similary:

::

    $ ./cream_serviceInfo.py --hostname cream-41.pd.infn.it --port 8443 -x /tmp/dteam.proxy
    OK: Service Version    = [1.16.1 - EMI version: 3.5.1-1.el6] 

cream\_allowedSubmission
~~~~~~~~~~~~~~~~~~~~~~~~

This is a simple metric which checks if the submission to the selected
CREAM CE is allowed. Its usage is analogous to the above metric:

::

    $ ./cream_allowedSubmission.py --help
    Usage: cream_allowedSubmission.py [options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -H HOSTNAME, --hostname=HOSTNAME
                            The hostname of the CREAM service.
      -p PORT, --port=PORT  The port of the service. [default: none]
      -x PROXY, --proxy=PROXY
                            The proxy path
      -t TIMEOUT, --timeout=TIMEOUT
                            Probe execution time limit. [default:
                            120 sec]
      -v, --verbose         verbose mode [default: False]
      -u URL, --url=URL     The status endpoint URL of the service. Example:
                            https://<host>[:<port>]

Notice: the use of the ``--url`` option is equivalent to specify both
the options: ``--hostname`` and ``--port``:

::

    $ ./cream_allowedSubmission.py --hostname cream-41.pd.infn.it --port 8443 -x /tmp/dteam.proxy
    OK: ENABLED

    $ ./cream_allowedSubmission.py --url https://cream-41.pd.infn.it:8443 -x /tmp/dteam.proxy
    OK: ENABLED

The verbose mode highlights the internal commands:

::

    $ ./cream_allowedSubmission.py --url https://cream-41.pd.infn.it:8443 -x /tmp/dteam.proxy --verbose
    executing command: /usr/bin/voms-proxy-info -timeleft
    invoking allowedSubmission
    executing command: /usr/bin/glite-ce-allowed-submission cream-41.pd.infn.it:8443
    OK: ENABLED

cream\_jobSubmit.py
~~~~~~~~~~~~~~~~~~~

This metric submits a job directly to the selected CREAM CE and waits
until the job termination by providing the final status. Finally the job
is purged. Moreover the stage-in and stage-out phases are both performed
automatically by the CE. In particular the stage-out needs the
``OutputSandboxBaseDestUri="gsiftp://localhost"`` set in the JDL.

::

    $ ./cream_jobSubmit.py --help
    Usage: cream_jobSubmit.py [options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -H HOSTNAME, --hostname=HOSTNAME
                            The hostname of the CREAM service.
      -p PORT, --port=PORT  The port of the service. [default: none]
      -x PROXY, --proxy=PROXY
                            The proxy path
      -t TIMEOUT, --timeout=TIMEOUT
                            Probe execution time limit. [default:
                            120 sec]
      -v, --verbose         verbose mode [default: False]
      -u URL, --url=URL     The status endpoint URL of the service. Example:
                            https://<host>[:<port>]/cream-<lrms>-<queue>
      -l LRMS, --lrms=LRMS  The LRMS name (e.g.: 'lsf', 'pbs' etc)
      -q QUEUE, --queue=QUEUE
                            The queue name (e.g.: 'creamtest')
      -j JDL, --jdl=JDL     The jdl path
      -d DIR, --dir=DIR     The output sandbox path

The ``--url`` (``-u``) directive must be used to target the probe to a
specific CREAM CE identified by its identifier (i.e. CREAM CE ID).
Alternatively is it possible to specify the CREAM CE identifier by using
the ``--hostname`` , ``--port``, ``--lrms`` and ``--queue`` options
which are mutually exclusive with respect to the ``--url`` option.
Consider the JDL file hostname.jdl with the following content:

::

    $ cat ./hostname.jdl
    [
    Type="Job";
    JobType="Normal";
    Executable = "/bin/hostname";
    Arguments = "-s";
    StdOutput = "std.out";
    StdError = "std.err";
    OutputSandbox = {"std.out","std.err"};
    OutputSandboxBaseDestUri="gsiftp://localhost";
    ]

If verbose mode is disabled, the output should look like this:

::

    $ ./cream_jobSubmit.py --url https://cream-41.pd.infn.it:8443/cream-lsf-creamtest1 -x /tmp/dteam.proxy --jdl ./hostname.jdl 
    DONE-OK: prod-wn-001

Notice: the use of the ``--url`` option is equivalent to specify both
the options: ``--hostname``, ``--port`` ``--lrms`` and --queue:

::

    $ ./cream_jobSubmit.py --hostname cream-41.pd.infn.it --port 8443 --lrms lsf --queue creamtest1 -x /tmp/dteam.proxy --jdl ./hostname.jdl 
    DONE-OK: prod-wn-001

If the verbose mode is enabled, the output of the above command should
be like this:

::

    $ ./cream_jobSubmit.py --hostname cream-41.pd.infn.it --port 8443 --lrms lsf --queue creamtest1 -x /tmp/dteam.proxy --jdl ./hostname.jdl --verbose
    executing command: /usr/bin/voms-proxy-info -timeleft
    executing command: /usr/bin/glite-ce-job-submit -d -a -r cream-41.pd.infn.it:8443/cream-lsf-creamtest1 hostname.jdl
    ['2014-01-31 12:18:12,740 DEBUG - Using certificate proxy file [/tmp/dteam.proxy]\n', '2014-01-31 12:18:12,756 DEBUG - VO from certificate=[dteam]\n', '2014-01-31 12:18:12,756 WARN - No configuration file suitable for loading. Using built-in configuration\n', '2014-01-31 12:18:12,756 DEBUG - Logfile is [/tmp/glite_cream_cli_logs/glite-ce-job-submit_CREAM_root_20140131-121812.log]\n', '2014-01-31 12:18:12,760 INFO - certUtil::generateUniqueID() - Generated DelegationID: [e0b6d023c766400e8b27e51cf5a2b1fa179d78f9]\n', '2014-01-31 12:18:14,606 DEBUG - Registering to [https://cream-41.pd.infn.it:8443/ce-cream/services/CREAM2] JDL=[ StdOutput = "std.out"; BatchSystem = "lsf"; QueueName = "creamtest1"; Executable = "/bin/hostname"; Type = "Job"; Arguments = "-s"; JobType = "Normal"; OutputSandboxBaseDestUri = "gsiftp://localhost"; OutputSandbox = { "std.out","std.err" }; StdError = "std.err" ] - JDL File=[hostname.jdl]\n', '2014-01-31 12:18:14,942 DEBUG - Will invoke JobStart for JobID [CREAM446576112]\n', 'https://cream-41.pd.infn.it:8443/CREAM446576112\n']
    job id: https://cream-41.pd.infn.it:8443/CREAM446576112
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://cream-41.pd.infn.it:8443/CREAM446576112
    ['\n', '******  JobID=[https://cream-41.pd.infn.it:8443/CREAM446576112]\n', '\tStatus        = [DONE-OK]\n', '\tExitCode      = [0]\n', '\n', '\n']
    exitCode=       ExitCode      = [0]

    job status: DONE-OK
    invoking getOutputSandbox
    executing command: /usr/bin/glite-ce-job-output --noint --dir /tmp https://cream-41.pd.infn.it:8443/CREAM446576112
    output sandbox dir: /tmp/cream-41.pd.infn.it_8443_CREAM446576112
    invoking jobPurge
    executing command: /usr/bin/glite-ce-job-purge --noint https://cream-41.pd.infn.it:8443/CREAM446576112
    DONE-OK: prod-wn-001

Notice the
``output sandbox dir: ./cream-41.pd.infn.it_8443_CREAM446576112``. This
is the output sandbox directory containing all the produced files:

::

    $ ls -la ./cream-41.pd.infn.it_8443_CREAM446576112
    total 12
    drwxr-xr-x   2 root root 4096 17 gen 16:20 .
    dr-xr-x---. 23 root root 4096 17 gen 16:20 ..
    -rw-------   1 root root    0 17 gen 16:20 std.err
    -rw-------   1 root root   26 17 gen 16:20 std.out

cream\_jobCancel.py
~~~~~~~~~~~~~~~~~~~

This metric submits a job directly to the selected CREAM CE, waits until
the job gain the REALLY-RUNNING state and then tries to cancel it.
Finally it checks if the job has been correctly canceled.

::

    $ ./cream_jobCancel.py --help
    Usage: cream_jobCancel.py [options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -H HOSTNAME, --hostname=HOSTNAME
                            The hostname of the CREAM service.
      -p PORT, --port=PORT  The port of the service. [default: none]
      -x PROXY, --proxy=PROXY
                            The proxy path
      -t TIMEOUT, --timeout=TIMEOUT
                            Probe execution time limit. [default:
                            120 sec]
      -v, --verbose         verbose mode [default: False]
      -u URL, --url=URL     The status endpoint URL of the service. Example:
                            https://<host>[:<port>]/cream-<lrms>-<queue>
      -l LRMS, --lrms=LRMS  The LRMS name (e.g.: 'lsf', 'pbs' etc)
      -q QUEUE, --queue=QUEUE
                            The queue name (e.g.: 'creamtest')
      -j JDL, --jdl=JDL     The jdl path

The job must be enough long in terms of execution time, in order to
allow the probe to check the current job status and invoke the
glite-ce-job-cancel. For example consider the job (i.e. hostnane.jdl) of
the above metric. In this case the probe will fail because the job
already terminated before the execution of the e glite-ce-job-cancel
command:

::

    $ ./cream_jobCancel.py --url https://cream-41.pd.infn.it:8443/cream-lsf-creamtest1 -x /tmp/dteam.proxy --jdl ./hostname.jdl 
    job already terminated

Now consider the following job:

::

    $ cat ./sleep.jdl 
    [
    Type="Job";
    JobType="Normal";
    Executable = "/bin/sleep";
    Arguments = "200";
    StdOutput = "cream.out";
    StdError = "cream.out";
    ]

The output of the probe should be like:

::

    $ ./cream_jobCancel.py --url https://cream-41.pd.infn.it:8443/cream-lsf-creamtest1 -x /tmp/dteam.proxy --jdl ./sleep.jdl 
    OK: job cancelled

or like this with ``--verbose`` option specified:

::

    $ ./cream_jobCancel.py --url https://cream-41.pd.infn.it:8443/cream-lsf-creamtest1 -x /tmp/dteam.proxy --jdl ./sleep.jdl --verbose
    executing command: /usr/bin/voms-proxy-info -timeleft
    executing command: /usr/bin/glite-ce-job-submit -d -a -r cream-41.pd.infn.it:8443/cream-lsf-creamtest1 ./sleep.jdl
    ['2014-01-31 12:30:42,469 DEBUG - Using certificate proxy file [/tmp/dteam.proxy]\n', '2014-01-31 12:30:42,489 DEBUG - VO from certificate=[dteam]\n', '2014-01-31 12:30:42,489 WARN - No configuration file suitable for loading. Using built-in configuration\n', '2014-01-31 12:30:42,489 DEBUG - Logfile is [/tmp/glite_cream_cli_logs/glite-ce-job-submit_CREAM_root_20140131-123042.log]\n', '2014-01-31 12:30:42,493 INFO - certUtil::generateUniqueID() - Generated DelegationID: [59882bed5243b5788a83404ad027cf571319ef79]\n', '2014-01-31 12:30:44,059 DEBUG - Registering to [https://cream-41.pd.infn.it:8443/ce-cream/services/CREAM2] JDL=[ StdOutput = "cream.out"; BatchSystem = "lsf"; QueueName = "creamtest1"; Executable = "/bin/sleep"; Type = "Job"; Arguments = "200"; JobType = "Normal"; StdError = "cream.out" ] - JDL File=[./sleep.jdl]\n', '2014-01-31 12:30:44,368 DEBUG - Will invoke JobStart for JobID [CREAM076606856]\n', 'https://cream-41.pd.infn.it:8443/CREAM076606856\n']
    job id: https://cream-41.pd.infn.it:8443/CREAM076606856
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://cream-41.pd.infn.it:8443/CREAM076606856
    ['\n', '******  JobID=[https://cream-41.pd.infn.it:8443/CREAM076606856]\n', '\tStatus        = [REALLY-RUNNING]\n', '\n', '\n']
    job status: REALLY-RUNNING
    invoking jobCancel
    executing command: /usr/bin/glite-ce-job-cancel --noint https://cream-41.pd.infn.it:8443/CREAM076606856
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://cream-41.pd.infn.it:8443/CREAM076606856
    ['\n', '******  JobID=[https://cream-41.pd.infn.it:8443/CREAM076606856]\n', '\tStatus        = [REALLY-RUNNING]\n', '\n', '\n']
    job status: REALLY-RUNNING
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://cream-41.pd.infn.it:8443/CREAM076606856
    ['\n', '******  JobID=[https://cream-41.pd.infn.it:8443/CREAM076606856]\n', '\tStatus        = [CANCELLED]\n', '\tExitCode      = []\n', '\tDescription   = [Cancelled by user]\n', '\n', '\n']
    exitCode=       ExitCode      = []

    job status: CANCELLED
    invoking jobPurge
    executing command: /usr/bin/glite-ce-job-purge --noint https://cream-41.pd.infn.it:8443/CREAM076606856
    OK: job cancelled

cream\_jobPurge.py
~~~~~~~~~~~~~~~~~~

This metric is analogous of cream\_jobCancel.py. It submits a short job
(e.g. hostname.jdl), waits its termination (e.g DONE-OK) and then it
tries to purge it. Finally, in order to verify the purging operation was
successfully executed, the probe checks the job status by executing the
glite-ce-job-status command which just in this scenario, must fail
because the job doesn't exist anymore.

::

    $ ./cream_jobPurge.py --help
    Usage: cream_jobPurge.py [options]

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -H HOSTNAME, --hostname=HOSTNAME
                            The hostname of the CREAM service.
      -p PORT, --port=PORT  The port of the service. [default: none]
      -x PROXY, --proxy=PROXY
                            The proxy path
      -t TIMEOUT, --timeout=TIMEOUT
                            Probe execution time limit. [default:
                            120 sec]
      -v, --verbose         verbose mode [default: False]
      -u URL, --url=URL     The status endpoint URL of the service. Example:
                            https://<host>[:<port>]/cream-<lrms>-<queue>
      -l LRMS, --lrms=LRMS  The LRMS name (e.g.: 'lsf', 'pbs' etc)
      -q QUEUE, --queue=QUEUE
                            The queue name (e.g.: 'creamtest')
      -j JDL, --jdl=JDL     The jdl path

::

    $ ./cream_jobPurge.py --url https://cream-41.pd.infn.it:8443/cream-lsf-creamtest1 -x /tmp/dteam.proxy --jdl ./hostname.jdl 
    OK: job purged

::

    $ ./cream_jobPurge.py --url https://cream-41.pd.infn.it:8443/cream-lsf-creamtest1 -x /tmp/dteam.proxy --jdl ./hostname.jdl --verbose
    executing command: /usr/bin/voms-proxy-info -timeleft
    executing command: /usr/bin/glite-ce-job-submit -d -a -r cream-41.pd.infn.it:8443/cream-lsf-creamtest1 hostname.jdl
    ['2014-01-31 12:27:50,347 DEBUG - Using certificate proxy file [/tmp/dteam.proxy]\n', '2014-01-31 12:27:50,364 DEBUG - VO from certificate=[dteam]\n', '2014-01-31 12:27:50,364 WARN - No configuration file suitable for loading. Using built-in configuration\n', '2014-01-31 12:27:50,364 DEBUG - Logfile is [/tmp/glite_cream_cli_logs/glite-ce-job-submit_CREAM_root_20140131-122750.log]\n', '2014-01-31 12:27:50,367 INFO - certUtil::generateUniqueID() - Generated DelegationID: [5978b3f267779dbf4d691889ea316a14dafeb4bb]\n', '2014-01-31 12:27:51,780 DEBUG - Registering to [https://cream-41.pd.infn.it:8443/ce-cream/services/CREAM2] JDL=[ StdOutput = "std.out"; BatchSystem = "lsf"; QueueName = "creamtest1"; Executable = "/bin/hostname"; Type = "Job"; Arguments = "-s"; JobType = "Normal"; OutputSandboxBaseDestUri = "gsiftp://localhost"; OutputSandbox = { "std.out","std.err" }; StdError = "std.err" ] - JDL File=[hostname.jdl]\n', '2014-01-31 12:27:52,109 DEBUG - Will invoke JobStart for JobID [CREAM973322659]\n', 'https://cream-41.pd.infn.it:8443/CREAM973322659\n']
    job id: https://cream-41.pd.infn.it:8443/CREAM973322659
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://cream-41.pd.infn.it:8443/CREAM973322659
    ['\n', '******  JobID=[https://cream-41.pd.infn.it:8443/CREAM973322659]\n', '\tStatus        = [DONE-OK]\n', '\tExitCode      = [0]\n', '\n', '\n']
    exitCode=       ExitCode      = [0]

    job status: DONE-OK
    invoking jobPurge
    executing command: /usr/bin/glite-ce-job-purge --noint https://cream-41.pd.infn.it:8443/CREAM973322659
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://cream-41.pd.infn.it:8443/CREAM973322659
    OK: job purged

WN-softver probe
~~~~~~~~~~~~~~~~

This probe checks the middleware version on a WN managed by the
CREAM-CE. It makes use of cream\_jobSubmit.py in the following way:

::

    $ ./cream_jobSubmit.py --url https://cream-41.pd.infn.it:8443/cream-lsf-creamtest1 -x /tmp/dteam.proxy -j ./WN-softver.jdl
    DONE-OK: prod-wn-002 has EMI 1.11.0-1

where

::

    $ cat WN-softver.jdl
    [
    Type="Job";
    JobType="Normal";
    Executable = "WN-softver.sh";
    #Arguments = "a b c";
    StdOutput = "std.out";
    StdError = "std.err";
    InputSandbox = {"WN-softver.sh"};
    OutputSandbox = {"std.out","std.err"};
    OutputSandboxBaseDestUri="gsiftp://localhost";
    ]

and
`WN-softver.sh <https://wiki.italiangrid.it/twiki/pub/CREAM/DjsCreamProbeNew/WN-softver.sh>`__
is attached.

The verbose option enabled gives the following output:

::

    $ ./cream_jobSubmit.py --url https://cream-41.pd.infn.it:8443/cream-lsf-creamtest1 -x /tmp/dteam.proxy -j ./WN-softver.jdl --verbose
    executing command: /usr/bin/voms-proxy-info -timeleft
    executing command: /usr/bin/glite-ce-job-submit -d -a -r cream-41.pd.infn.it:8443/cream-lsf-creamtest1 ./WN-softver.jdl
    ['2014-01-31 13:05:05,802 DEBUG - Using certificate proxy file [/tmp/dteam.proxy]\n', '2014-01-31 13:05:05,823 DEBUG - VO from certificate=[dteam]\n', '2014-01-31 13:05:05,824 WARN - No configuration file suitable for loading. Using built-in configuration\n', '2014-01-31 13:05:05,824 DEBUG - Logfile is [/tmp/glite_cream_cli_logs/glite-ce-job-submit_CREAM_root_20140131-130505.log]\n', '2014-01-31 13:05:05,824 DEBUG - Processing file [WN-softver.sh]...\n', '2014-01-31 13:05:05,824 DEBUG - Adding absolute path [/root/WN-softver.sh]...\n', '2014-01-31 13:05:05,824 DEBUG - Inserting mangled InputSandbox in JDL: [{"/root/WN-softver.sh"}]...\n', '2014-01-31 13:05:05,827 INFO - certUtil::generateUniqueID() - Generated DelegationID: [b18342097b01b309cc9112a683d4c6bd15d35796]\n', '2014-01-31 13:05:07,517 DEBUG - Registering to [https://cream-41.pd.infn.it:8443/ce-cream/services/CREAM2] JDL=[ StdOutput = "std.out"; BatchSystem = "lsf"; QueueName = "creamtest1"; Executable = "WN-softver.sh"; Type = "Job"; JobType = "Normal"; OutputSandboxBaseDestUri = "gsiftp://localhost"; OutputSandbox = { "std.out","std.err" }; InputSandbox = { "/root/WN-softver.sh" }; StdError = "std.err" ] - JDL File=[./WN-softver.jdl]\n', '2014-01-31 13:05:07,870 DEBUG - JobID=[https://cream-41.pd.infn.it:8443/CREAM680089855]\n', '2014-01-31 13:05:07,871 DEBUG - UploadURL=[gsiftp://cream-41.pd.infn.it/var/glite/cream_sandbox/dteam/CN_Marco_Verlato_L_Padova_OU_Personal_Certificate_O_INFN_C_IT_dteam_Role_NULL_Capability_NULL_dteam019/68/CREAM680089855/ISB]\n', '2014-01-31 13:05:07,873 INFO - Sending file [gsiftp://cream-41.pd.infn.it/var/glite/cream_sandbox/dteam/CN_Marco_Verlato_L_Padova_OU_Personal_Certificate_O_INFN_C_IT_dteam_Role_NULL_Capability_NULL_dteam019/68/CREAM680089855/ISB/WN-softver.sh]\n', '2014-01-31 13:05:08,044 DEBUG - Will invoke JobStart for JobID [CREAM680089855]\n', 'https://cream-41.pd.infn.it:8443/CREAM680089855\n']
    job id: https://cream-41.pd.infn.it:8443/CREAM680089855
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://cream-41.pd.infn.it:8443/CREAM680089855
    ['\n', '******  JobID=[https://cream-41.pd.infn.it:8443/CREAM680089855]\n', '\tStatus        = [DONE-OK]\n', '\tExitCode      = [0]\n', '\n', '\n']
    exitCode=       ExitCode      = [0]

    job status: DONE-OK
    invoking getOutputSandbox
    executing command: /usr/bin/glite-ce-job-output --noint https://cream-41.pd.infn.it:8443/CREAM680089855
    output sandbox dir: ./cream-41.pd.infn.it_8443_CREAM680089855
    invoking jobPurge
    executing command: /usr/bin/glite-ce-job-purge --noint https://cream-41.pd.infn.it:8443/CREAM680089855
    DONE-OK: prod-wn-002 has EMI 1.11.0-1

WN-csh probe
~~~~~~~~~~~~

This probe checks that csh is there on a WN managed by the CREAM-CE. It
makes use of cream\_jobSubmit.py in the following way:

::

    $ ./cream_jobSubmit.py --url https://cream-41.pd.infn.it:8443/cream-lsf-creamtest1 -x /tmp/dteam.proxy -j ./WN-csh.jdl
    DONE-OK: prod-wn-002 has csh

where

::

    $ cat WN-csh.jdl
    [
    Type="Job";
    JobType="Normal";
    Executable = "WN-csh.sh";
    #Arguments = "a b c";
    StdOutput = "std.out";
    StdError = "std.err";
    InputSandbox = {"WN-csh.sh"};
    OutputSandbox = {"std.out","std.err"};
    OutputSandboxBaseDestUri="gsiftp://localhost";
    ]

and
`WN-csh.sh <https://wiki.italiangrid.it/twiki/pub/CREAM/DjsCreamProbeNew/WN-csh.sh>`__
is attached.

Deployment example
~~~~~~~~~~~~~~~~~~

In a Nagios server version 3.5.0 testing instance, we deployed the files
needed to execute the probes described above in the following
directories:

::

    $ ls -l /usr/libexec/grid-monitoring/probes/emi.cream/
    total 48
    -rwxr-xr-x 1 root root  1361 Jan 30 16:58 cream_allowedSubmission.py
    -rwxr-xr-x 1 root root  2494 Jan 30 17:00 cream_jobCancel.py
    -rwxr-xr-x 1 root root  2103 Jan 30 17:01 cream_jobPurge.py
    -rwxr-xr-x 1 root root  2972 Jan 31 12:42 cream_jobSubmit.py
    -rwxr-xr-x 1 root root 15527 Jan 30 16:29 cream.py
    -rwxr-xr-x 1 root root  1416 Jan 31 12:42 cream_serviceInfo.py
    -rw-r--r-- 1 root root   213 Jan 29 14:26 hostname.jdl
    -rw-r--r-- 1 root root   129 Jan 30 16:21 sleep.jdl
    drwxr-xr-x 2 root root  4096 Jan 31 11:34 wn

and

::

    $ ls -l /usr/libexec/grid-monitoring/probes/emi.cream/wn
    total 16
    -rw-r--r-- 1 root root  292 Jan 31 11:34 WN-csh.jdl
    -rwxr-xr-x 1 root root  603 Jan 31 11:34 WN-csh.sh
    -rw-r--r-- 1 root root  300 Jan 31 11:34 WN-softver.jdl
    -rwxr-xr-x 1 root root 1144 Jan 31 11:34 WN-softver.sh

and defined the new services adding in the file
``/etc/nagios/objects/services.cfg`` the following lines:

::

    define service{
            use                             local-service
            host_name                       cream-41.pd.infn.it
            service_description             emi.cream.CEDIRECT-AllowedSubmission
            check_command                   ncg_check_native!/usr/libexec/grid-monit
    oring/probes/emi.cream/cream_allowedSubmission.py!60!-x /tmp/dteam.proxy -p 8443
            normal_check_interval           6
            retry_check_interval            3
            max_check_attempts              2
            obsess_over_service             0
    }
    define service{
            use                             local-service
            host_name                       cream-41.pd.infn.it
            service_description             emi.cream.CEDIRECT-JobCancel
            check_command                   ncg_check_native!/usr/libexec/grid-monit
    oring/probes/emi.cream/cream_jobCancel.py!60!-x /tmp/dteam.proxy -p 8443 -l lsf 
    -q creamtest1 -j /usr/libexec/grid-monitoring/probes/emi.cream/sleep.jdl
            normal_check_interval           6
            retry_check_interval            3
            max_check_attempts              2
            obsess_over_service             0
    }
    define service{
            use                             local-service
            host_name                       cream-41.pd.infn.it
            service_description             emi.cream.CEDIRECT-JobPurge
            check_command                   ncg_check_native!/usr/libexec/grid-monit
    oring/probes/emi.cream/cream_jobPurge.py!60!-x /tmp/dteam.proxy -p 8443 -l lsf -
    q creamtest1 -j /usr/libexec/grid-monitoring/probes/emi.cream/hostname.jdl
            normal_check_interval           6
            retry_check_interval            3
            max_check_attempts              2
            obsess_over_service             0
    }

    define service{
            use                             local-service
            host_name                       cream-41.pd.infn.it
            service_description             emi.cream.CEDIRECT-ServiceInfo
            check_command                   ncg_check_native!/usr/libexec/grid-monit
    oring/probes/emi.cream/cream_serviceInfo.py!60!-x /tmp/dteam.proxy -p 8443
            normal_check_interval           6
            retry_check_interval            3
            max_check_attempts              2
            obsess_over_service             0
    }
    define service{
            use                             local-service
            host_name                       cream-41.pd.infn.it
            service_description             emi.cream.CEDIRECT-JobSubmit
            check_command                   ncg_check_native!/usr/libexec/grid-monit
    oring/probes/emi.cream/cream_jobSubmit.py!60!-x /tmp/dteam.proxy -p 8443 -l lsf 
    -q creamtest1 -j /usr/libexec/grid-monitoring/probes/emi.cream/hostname.jdl --di
    r /tmp 
            normal_check_interval           6
            retry_check_interval            3
            max_check_attempts              2
            obsess_over_service             0
    }
    define service{
            use                             local-service
            host_name                       cream-41.pd.infn.it
            service_description             emi.cream.WN-Softver
            check_command                   ncg_check_native!/usr/libexec/grid-monit
    oring/probes/emi.cream/cream_jobSubmit.py!60!-x /tmp/dteam.proxy -p 8443 -l lsf 
    -q creamtest1 -j /usr/libexec/grid-monitoring/probes/emi.cream/wn/WN-softver.jdl
     --dir /tmp
            normal_check_interval           6
            retry_check_interval            3
            max_check_attempts              2
            obsess_over_service             0
    }
    define service{
            use                             local-service
            host_name                       cream-41.pd.infn.it
            service_description             emi.cream.WN-Csh
            check_command                   ncg_check_native!/usr/libexec/grid-monit
    oring/probes/emi.cream/cream_jobSubmit.py!60!-x /tmp/dteam.proxy -p 8443 -l lsf 
    -q creamtest1 -j /usr/libexec/grid-monitoring/probes/emi.cream/wn/WN-csh.jdl --d
    ir /tmp

            normal_check_interval           6
            retry_check_interval            3
            max_check_attempts              2
            obsess_over_service             0
    }

The check\_command ncg\_check\_native was defined in the file
``/etc/nagios/objects/commands.cfg`` as below:

::

    define command{
            command_name                    ncg_check_native
            command_line                    $ARG1$ -H $HOSTNAME$ -t $ARG2$ $ARG3$
    }
