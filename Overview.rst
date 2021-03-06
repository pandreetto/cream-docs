CREAM Functional Description
============================

The CREAM (Computing Resource Execution And Management) Service is a
simple, lightweight service that implements all the operations at the
Computing Element (CE) level; its well-defined WebService-based
interface and its implementation as an extension of the Java-Axis
servlet (running inside the Apache Tomcat container) provide
interoperability with clients written in any programming language and
running on any computer platform.

The CREAM interface is well-defined using the Web Service Description
Language (WSDL); anyone can generate his/her CREAM client by simply
filling in the stub code generated by WSDL parser (gSOAP for C/C++, Axis
for Java, Perl module for perl).

CREAM functionality:

-  Job Submission

   -  Possibility of direct staging of input sandbox files

   -  gLite JDL compliance (with CREAM-specific extensions)

   -  Support for batch and parallel jobs

-  Manual and automatic proxy delegation

-  Job Cancellation

-  Job Info with configurable level of verbosity and filtering based on
   submission time and/or job status

-  Job List

-  Job Suspension and Resume

-  Job output retrieval

-  Job Purge for terminated jobs

-  Possibility (for admin) to disable new submissions

-  Self limiting CREAM behavior: CREAM is able to protect itself if the
   load, memory usage, etc. is too high. This happens disabling new job
   submissions, while the other commands are still allowed

-  ARGUS or gJAF based authorization

-  Possibility to forward requirements to the batch system

-  Integration with APEL accounting systems

CREAM can be used

-  by the Workload Management System (WMS), via the ICE (Interface to
   CREAM Environment) service

-  by a generic client, e.g. an end-user willing to directly submit jobs
   to a CREAM CE. A C++ command line interface (CLI) is available

CREAM service accesses and operates local resource management systems.
The current version of the application supports the following management
systems:

-  TORQUE

-  LSF

-  SLURM

-  HTCondor

-  Grid Engine (partially)

Authentication in CREAM is managed via the trustmanager. The Trust
Manager is the component responsible for carrying out authentication
operations. It is an implementation of the J2EE security specifications.
Authentication is based on PKI. Each user (and Grid service) wishing to
access CREAM is required to present an X.509 format certificate. These
certificates are issued by trusted entities, the Certificate Authorities
(CA). The role of a CA is to guarantee the identity of a user. This is
achieved by issuing an electronic document (the certificate) that
contains the information about the user and is digitally signed by the
CA with its private key. An authentication manager, such as the Trust
Manager, can verify the user identity by decrypting the hash of the
certificate with the CA public key. This ensures that the certificate
was issued by that specific CA. The Trust Manager can then access the
user data contained in the certificate and verify the user identity.

Authorization in the CREAM CE can be implemented in two different ways
(the choice is done at configuration time):

-  Authorization with ARGUS

-  Authorization with gJAF

Argus is a system meant to render consistent authorization decisions for
distributed services (e.g. compute elements, portals). In order to
achieve this consistency a number of points must be addressed. First, it
must be possible to author and maintain consistent authorization
policies. This is handled by the Policy Administration Point (PAP)
component in the service. Second, authored policies must be evaluated in
a consistent manner, a task performed by the Policy Decision Point
(PDP). Finally, the data provided for evaluation against policies must
be consistent (in form and definition) and this is done by the Policy
Enforcement Point (PEP). Argus is also responsible to manage the Grid
user - local user mapping.

gJAF (Grid Java Authorization Framework) provides a way to invoke a
chain of policy engines and get a decision result about the
authorization of a user. The policy engines are divided in two types,
depending on their functionality. They can be plugged into the framework
in order to form a chain of policy engines as selected by the
administrator in order to let him set up a complete authorization
system. A policy engine may be either a PIP or a PDP. PIP collect and
verify assertions and capabilities associated with the user, checking
her role, group and VO attributes. PDP may use the information retrieved
by a PIP to decide whether the user is allowed to perform the requested
action, whether further evaluation is needed, or whether the evaluation
should be interrupted and the user access denied.

In CREAM CE VO based authorization is supported. In this scenario,
implemented via the VOMS PDP, the administrator can specify
authorization policies based on the VO the jobs' owners belong to (or on
particular VO attributes). When gJAF is used as authorization mechanism,
the Grid user - local user mapping is managed via glexec, For what
concerns authorization on job operations, by default each user can
manage (e.g. cancel, suspend, etc.) only her own jobs. However, the
CREAM administrator can define specific super-users who are empowered to
manage also jobs submitted by other users.
