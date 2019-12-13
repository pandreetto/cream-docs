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

-  python (version 2.7 or greater)

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

-  ``cream_allowedSubmission.py`` - check if the submission to the selected CREAM CE is allowed

-  ``cream_jobSubmit.py`` - submit a job directly to the selected CREAM CE

-  ``cream_jobOutput.py`` - submit a job directly to the selected CREAM CE and retrieve the output-sandbox

-  ``WN-softver probe`` - check middleware version on WN (via cream_jobOutput.py)

-  ``WN-csh probe`` - check if WN has csh (via cream_jobOutput.py)

All of them have been implemented in python and are based on the `cream-cli <User_Guide.html#cream-command-line-interface-guide>`__\ commands. They share the same logic structure and provide useful information about their version, usage (i.e. help) including the options list and their meaning, according to the guide `Probes Development <https://tomtools.cern.ch/confluence/display/SAMDOC/Probes+Development>`__.
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
    cream_serviceInfo v.1.1


The interaction with the CREAM CE requires the use of a valid VOMS proxy expressed by the ``X509_USER_PROXY`` env variable or through the ``--proxy`` option. All metrics check the existence of the proxy file and calculate the time left. In case of error, the related error message will be thrown:

::

    $ ./cream_serviceInfo.py --hostname cream-41.pd.infn.it --port 8443 --proxy /tmp/x509up_u0 --verbose
    Proxy file not found or not readable

The verbose mode (``--verbose``) could be enabled to each metric. It provides several details about the probe execution itself by highlighting the internal commands:

::

    $ ./cream_serviceInfo.py --hostname prod-ce-01.pd.infn.it --port 8443 -x /tmp/x509up_u733 --verbose
    executing command: /usr/bin/voms-proxy-info -timeleft
    invoking service info
    executing command: /usr/bin/glite-ce-service-info prod-ce-01.pd.infn.it:8443
    CREAM serviceInfo OK: Service Version    = [1.16.4 - EMI version: 3.15.0-1.el6]


In case of mistakes on the selected options or on their values, the probe tries to explain what is wrong. For example the cream\_serviceInfo doesn't support the ``--queue`` option:

::

    $ ./cream_serviceInfo.py --hostname prod-ce-01.pd.infn.it --port 8443 --queue creamtest1 -x  /tmp/x509up_u733 --verbose
    Usage: cream_serviceInfo.py [options]

    cream_serviceInfo.py: error: no such option: --queue


In case of the errors in interacting with the CREAM CE, useful details will be provided about the failure:

::

    $ ./cream_allowedSubmission.py --url https://prod-ce-01.pd.infn.it:8443 -x /tmp/x509up_u733
    command '/usr/bin/glite-ce-allowed-submission cream-43.pd.infn.it:8443' failed: return_code=1
    details: ['2019-12-13 15:59:57,085 FATAL - Received NULL fault; the error is due to another cause: FaultString=[connection error] - FaultCode=[SOAP-ENV:Client] - FaultSubCode=[SOAP-ENV:Client] - FaultDetail=[Connection refused]\n']


Sources are available in `github <https://github.com/italiangrid/cream-nagios/tree/master/src>`__


cream\_serviceInfo.py
~~~~~~~~~~~~~~~~~~~~~

The serviceInfo.py retrieves information about the status of the CREAM CE. The help shows how the probe must be invoked:

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

In order to get information about the CREAM service on the host https://prod-ce-01.pd.infn.it:8443, use the following command:

::

    $ ./cream_serviceInfo.py --url https://prod-ce-01.pd.infn.it:8443 -x /tmp/x509up_u733
    CREAM serviceInfo OK: Service Version = [1.16.4 - EMI version: 3.15.0-1.el6]

or similary:

::

    $ ./cream_serviceInfo.py --hostname prod-ce-01.pd.infn.it --port 8443 -x /tmp/x509up_u733
    CREAM serviceInfo OK: Service Version = [1.16.4 - EMI version: 3.15.0-1.el6]


cream\_allowedSubmission.py
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a simple metric which checks if the submission to the selected CREAM CE is allowed. Its usage is analogous to the above metric:

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

    $ ./cream_allowedSubmission.py --hostname prod-ce-01.pd.infn.it --port 8443 -x /tmp/x509up_u733
    CREAM allowedSubmission OK: the job submission is ENABLED
    
    $ ./cream_allowedSubmission.py --url https://prod-ce-01.pd.infn.it:8443 -x /tmp/x509up_u733
    CREAM allowedSubmission OK: the job submission is ENABLED

The verbose mode highlights the internal commands:

::

    $ ./cream_allowedSubmission.py --url https://prod-ce-01.pd.infn.it:8443 -x /tmp/x509up_u733 --verbose
    executing command: /usr/bin/voms-proxy-info -timeleft
    invoking allowedSubmission
    executing command: /usr/bin/glite-ce-allowed-submission prod-ce-01.pd.infn.it:8443
    CREAM allowedSubmission OK: the job submission is ENABLED


cream\_jobSubmit.py
~~~~~~~~~~~~~~~~~~~

This metric submits a job directly to the selected CREAM CE and waits until the job termination by providing the final status. Finally the job is purged. This probe does not test the output-sandbox retrieval.

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

The ``--url`` (``-u``) directive must be used to target the probe to a specific CREAM CE identified by its identifier (i.e. CREAM CE ID). Alternatively is it possible to specify the CREAM CE identifier by using the ``--hostname`` , ``--port``, ``--lrms`` and ``--queue`` options which are mutually exclusive with respect to the ``--url`` option.
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

    $ ./cream_jobSubmit.py --url https://prod-ce-01.pd.infn.it:8443/cream-lsf-grid -x /tmp/x509up_u733 --jdl ./hostname.jdl 
    CREAM JobSubmit OK [DONE-OK]

Notice: the use of the ``--url`` option is equivalent to specify both the options: ``--hostname``, ``--port`` ``--lrms`` and --queue:

::

    $ ./cream_jobSubmit.py --hostname prod-ce-01.pd.infn.it --port 8443 --lrms lsf --queue grid -x /tmp/x509up_u733 --jdl ./hostname.jdl 
    CREAM JobSubmit OK [DONE-OK]


If the verbose mode is enabled, the output of the above command should be like this:

::

    $ ./cream_jobSubmit.py --hostname prod-ce-01.pd.infn.it --port 8443 --lrms lsf --queue grid -x /tmp/x509up_u733 --jdl ./hostname.jdl --verbose
    executing command: /usr/bin/voms-proxy-info -timeleft
    executing command: /usr/bin/glite-ce-job-submit -d -a -r prod-ce-01.pd.infn.it:8443/cream-lsf-grid ./hostname.jdl
    ['2019-12-13 13:54:33,247 DEBUG - Using certificate proxy file [/tmp/x509up_u733]\n', '2019-12-13 13:54:33,279 DEBUG - VO from certificate=[enmr.eu]\n', '2019-12-13 13:54:33,279 WARN - No configuration file suitable for loading. Using built-in configuration\n', '2019-12-13 13:54:33,279 DEBUG - Logfile is [/tmp/glite_cream_cli_logs/glite-ce-job-submit_CREAM_zangrand_20191213-135433.log]\n', '2019-12-13 13:54:33,282 INFO - certUtil::generateUniqueID() - Generated DelegationID: [12815a52a76431b1712199d87ae5896fd6718b3a]\n', '2019-12-13 13:54:36,175 DEBUG - Registering to [https://prod-ce-01.pd.infn.it:8443/ce-cream/services/CREAM2] JDL=[ StdOutput = "std.out"; BatchSystem = "lsf"; QueueName = "grid"; Executable = "/bin/hostname"; Type = "Job"; Arguments = "-s"; JobType = "Normal"; OutputSandboxBaseDestUri = "gsiftp://localhost"; OutputSandbox = { "std.out","std.err" }; StdError = "std.err" ] - JDL File=[./hostname.jdl]\n', '2019-12-13 13:54:36,634 DEBUG - Will invoke JobStart for JobID [CREAM067861520]\n', 'https://prod-ce-01.pd.infn.it:8443/CREAM067861520\n']
    job id: https://prod-ce-01.pd.infn.it:8443/CREAM067861520
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://prod-ce-01.pd.infn.it:8443/CREAM067861520
    ['\n', '******  JobID=[https://prod-ce-01.pd.infn.it:8443/CREAM067861520]\n', '\tStatus        = [DONE-OK]\n', '\tExitCode      = [0]\n', '\n', '\n']
    exitCode=	ExitCode      = [0]

    job status: DONE-OK
    invoking jobPurge
    executing command: /usr/bin/glite-ce-job-purge --noint https://prod-ce-01.pd.infn.it:8443/CREAM067861520
    CREAM JobSubmit OK [DONE-OK]


cream\_jobOutput.py
~~~~~~~~~~~~~~~~~~~

This metric extends the cream\_jobSubmit.py functionality by retrieving the job's output-sandbox. Both the stage-in and stage-out phases are both performed automatically by the CE. In particular the stage-out needs the ``OutputSandboxBaseDestUri="gsiftp://localhost"`` set in the JDL.  Finally the job is purged.

::

    $ ./cream_jobOutput.py --help
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

The options are the same as cream\_jobSubmit.py except for ``--dir``. Such option allows the user to specify the path where the output-sandbox has to be stored temporarily. The default value is ``/var/lib/argo-monitoring/eu.egi.CREAMCE``.
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

    $ ./cream_jobOutput.py --hostname prod-ce-01.pd.infn.it --port 8443 --lrms lsf --queue grid -x /tmp/x509up_u733 --dir /tmp --jdl ./hostname.jdl
    CREAM JobOutput OK | retrieved outputSandbox: ['std.err', 'std.out']

   **** std.err ****


   **** std.out ****
   prod-wn-038


Notice: the use of the ``--dir`` and the output-sandbox content returned in the output message.

If the verbose mode is enabled, the output of the above command should
be like this:

::

    $ ./cream_jobOutput.py --hostname prod-ce-01.pd.infn.it --port 8443 --lrms lsf --queue grid -x /tmp/x509up_u733 --dir /tmp --jdl ./hostname.jdl --verbose
    executing command: /usr/bin/voms-proxy-info -timeleft
    executing command: /usr/bin/glite-ce-job-submit -d -a -r prod-ce-01.pd.infn.it:8443/cream-lsf-grid ./hostname.jdl
    ['2019-12-13 14:02:55,478 DEBUG - Using certificate proxy file [/tmp/x509up_u733]\n', '2019-12-13 14:02:55,519 DEBUG - VO from certificate=[enmr.eu]\n', '2019-12-13 14:02:55,520 WARN - No configuration file suitable for loading. Using built-in configuration\n', '2019-12-13 14:02:55,520 DEBUG - Logfile is [/tmp/glite_cream_cli_logs/glite-ce-job-submit_CREAM_zangrand_20191213-140255.log]\n', '2019-12-13 14:02:55,523 INFO - certUtil::generateUniqueID() - Generated DelegationID: [b6b895d69f7ef0d438db82930476a2fd149d0501]\n', '2019-12-13 14:02:57,610 DEBUG - Registering to [https://prod-ce-01.pd.infn.it:8443/ce-cream/services/CREAM2] JDL=[ StdOutput = "std.out"; BatchSystem = "lsf"; QueueName = "grid"; Executable = "/bin/hostname"; Type = "Job"; Arguments = "-s"; JobType = "Normal"; OutputSandboxBaseDestUri = "gsiftp://localhost"; OutputSandbox = { "std.out","std.err" }; StdError = "std.err" ] - JDL File=[./hostname.jdl]\n', '2019-12-13 14:02:58,271 DEBUG - Will invoke JobStart for JobID [CREAM160637101]\n', 'https://prod-ce-01.pd.infn.it:8443/CREAM160637101\n']
    job id: https://prod-ce-01.pd.infn.it:8443/CREAM160637101
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://prod-ce-01.pd.infn.it:8443/CREAM160637101
    ['\n', '******  JobID=[https://prod-ce-01.pd.infn.it:8443/CREAM160637101]\n', '\tStatus        = [IDLE]\n', '\n', '\n']
    job status: IDLE
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://prod-ce-01.pd.infn.it:8443/CREAM160637101
    ['\n', '******  JobID=[https://prod-ce-01.pd.infn.it:8443/CREAM160637101]\n', '\tStatus        = [DONE-OK]\n', '\tExitCode      = [0]\n', '\n', '\n']
    exitCode=	ExitCode      = [0]

    job status: DONE-OK
    invoking getOutputSandbox
    executing command: /usr/bin/glite-ce-job-output --noint --dir /tmp https://prod-ce-01.pd.infn.it:8443/CREAM160637101
    output sandbox dir: /tmp/prod-ce-01.pd.infn.it_8443_CREAM160637101
    invoking jobPurge
    executing command: /usr/bin/glite-ce-job-purge --noint https://prod-ce-01.pd.infn.it:8443/CREAM160637101
    CREAM JobOutput OK | retrieved outputSandbox: ['std.err', 'std.out']

    **** std.err ****


    **** std.out ****
    prod-wn-038
    

WN-softver probe
~~~~~~~~~~~~~~~~

This probe checks the middleware version on a WN managed by the CREAM-CE. It makes use of cream\_jobOutput.py in the following way:

::

    $ ./cream_jobOutput.py --url https://prod-ce-01.pd.infn.it:8443/cream-lsf-grid -x /tmp/x509up_u733 --dir /tmp -j ./WN-softver.jdl
    CREAM JobOutput OK | retrieved outputSandbox: ['std.err', 'std.out']

    **** std.err ****


    **** std.out ****
    prod-wn-014 has EMI 3.15.0-1.el6


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

    $ ./cream_jobOutput.py --url https://prod-ce-01.pd.infn.it:8443/cream-lsf-grid -x /tmp/x509up_u733 --dir /tmp -j ./WN-softver.jdl --verbose
    executing command: /usr/bin/voms-proxy-info -timeleft
    executing command: /usr/bin/glite-ce-job-submit -d -a -r prod-ce-01.pd.infn.it:8443/cream-lsf-grid ./WN-softver.jdl
    ['2019-12-13 14:06:25,768 DEBUG - Using certificate proxy file [/tmp/x509up_u733]\n', '2019-12-13 14:06:25,804 DEBUG - VO from certificate=[enmr.eu]\n', '2019-12-13 14:06:25,805 WARN - No configuration file suitable for loading. Using built-in configuration\n', '2019-12-13 14:06:25,805 DEBUG - Logfile is [/tmp/glite_cream_cli_logs/glite-ce-job-submit_CREAM_zangrand_20191213-140625.log]\n', '2019-12-13 14:06:25,805 DEBUG - Processing file [/users/cms/zangrand/cream-nagios-master/src/WN-softver.sh]...\n', '2019-12-13 14:06:25,805 DEBUG - Inserting mangled InputSandbox in JDL: [{"/users/cms/zangrand/cream-nagios-master/src/WN-softver.sh"}]...\n', '2019-12-13 14:06:25,806 INFO - certUtil::generateUniqueID() - Generated DelegationID: [7f0ac5ec8a7deefa01f207c0b341fce1568f5282]\n', '2019-12-13 14:06:27,612 DEBUG - Registering to [https://prod-ce-01.pd.infn.it:8443/ce-cream/services/CREAM2] JDL=[ StdOutput = "std.out"; BatchSystem = "lsf"; QueueName = "grid"; Executable = "WN-softver.sh"; Type = "Job"; JobType = "Normal"; OutputSandboxBaseDestUri = "gsiftp://localhost"; OutputSandbox = { "std.out","std.err" }; InputSandbox = { "/users/cms/zangrand/cream-nagios-master/src/WN-softver.sh" }; StdError = "std.err" ] - JDL File=[./WN-softver.jdl]\n', '2019-12-13 14:06:28,228 DEBUG - JobID=[https://prod-ce-01.pd.infn.it:8443/CREAM608273414]\n', '2019-12-13 14:06:28,228 DEBUG - UploadURL=[gsiftp://prod-ce-01.pd.infn.it/var/cream_sandbox/enmr/CN_Marco_Verlato_verlato_infn_it_O_Istituto_Nazionale_di_Fisica_Nucleare_C_IT_DC_tcs_DC_terena_DC_org_enmr_eu_Role_NULL_Capability_NULL_enmr018/60/CREAM608273414/ISB]\n', '2019-12-13 14:06:28,230 INFO - Sending file [gsiftp://prod-ce-01.pd.infn.it/var/cream_sandbox/enmr/CN_Marco_Verlato_verlato_infn_it_O_Istituto_Nazionale_di_Fisica_Nucleare_C_IT_DC_tcs_DC_terena_DC_org_enmr_eu_Role_NULL_Capability_NULL_enmr018/60/CREAM608273414/ISB/WN-softver.sh]\n', '2019-12-13 14:06:28,482 DEBUG - Will invoke JobStart for JobID [CREAM608273414]\n', 'https://prod-ce-01.pd.infn.it:8443/CREAM608273414\n']
    job id: https://prod-ce-01.pd.infn.it:8443/CREAM608273414
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://prod-ce-01.pd.infn.it:8443/CREAM608273414
    ['\n', '******  JobID=[https://prod-ce-01.pd.infn.it:8443/CREAM608273414]\n', '\tStatus        = [REALLY-RUNNING]\n', '\n', '\n']
    job status: REALLY-RUNNING
    invoking jobStatus
    executing command: /usr/bin/glite-ce-job-status https://prod-ce-01.pd.infn.it:8443/CREAM608273414
    ['\n', '******  JobID=[https://prod-ce-01.pd.infn.it:8443/CREAM608273414]\n', '\tStatus        = [DONE-OK]\n', '\tExitCode      = [0]\n', '\n', '\n']
    exitCode=	ExitCode      = [0]

    job status: DONE-OK
    invoking getOutputSandbox
    executing command: /usr/bin/glite-ce-job-output --noint --dir /tmp https://prod-ce-01.pd.infn.it:8443/CREAM608273414
    output sandbox dir: /tmp/prod-ce-01.pd.infn.it_8443_CREAM608273414
    invoking jobPurge
    executing command: /usr/bin/glite-ce-job-purge --noint https://prod-ce-01.pd.infn.it:8443/CREAM608273414
    CREAM JobOutput OK | retrieved outputSandbox: ['std.err', 'std.out']

    **** std.err ****


    **** std.out ****
    prod-wn-014 has EMI 3.15.0-1.el6
  

WN-csh probe
~~~~~~~~~~~~

This probe checks that csh is there on a WN managed by the CREAM-CE. It makes use of cream\_jobOutput.py in the following way:

::

    $ ./cream_jobOutput.py --url https://prod-ce-01.pd.infn.it:8443/cream-lsf-grid -x /tmp/x509up_u733 --dir /tmp -j ./WN-csh.jdl
    CREAM JobOutput OK | retrieved outputSandbox: ['std.err', 'std.out']

    **** std.err ****


    **** std.out ****
    prod-wn-016 has csh


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
    -rwxr-xr-x 1 root root  2972 Jan 31 12:42 cream_jobOutput.py
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
    oring/probes/emi.cream/cream_jobOutput.py!60!-x /tmp/dteam.proxy -p 8443 -l lsf 
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
    oring/probes/emi.cream/cream_jobOutput.py!60!-x /tmp/dteam.proxy -p 8443 -l lsf 
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
