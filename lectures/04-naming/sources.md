# Sources and asset provenance

Accessed 2026-11-09. Quotes were checked verbatim on the page.

## References

1. RFC 1034, "Domain Names: Concepts and Facilities", P. Mockapetris, November 1987. https://www.rfc-editor.org/rfc/rfc1034.html — "The domain name space is a tree structure."; "RESOLVERS are programs that extract information from name servers in response to client requests."; "NAME SERVERS are server programs which hold information about the domain tree's structure and set information."; "The TTL describes how long a RR can be cached before it should be discarded."
2. RFC 2308, "Negative Caching of DNS Queries (DNS NCACHE)", M. Andrews, March 1998. https://www.rfc-editor.org/rfc/rfc2308.html — "A negative answer that resulted from a name error (NXDOMAIN) should be cached" (§5); TTL "taken from the minimum of the SOA.MINIMUM field and SOA's TTL" (§5).
3. RFC 2782, "A DNS RR for specifying the location of services (DNS SRV)", February 2000. https://www.rfc-editor.org/rfc/rfc2782.html — format `_Service._Proto.Name TTL Class SRV Priority Weight Port Target`; port, priority, weight.
4. Docker, "Networking in Compose". https://docs.docker.com/compose/how-tos/networking/ — "Compose creates a network named `<project-name>_default` and attaches all services to it."; "Each service registers its name with an internal DNS server,"; "The `web` service can connect to the database at `postgres://db:5432`."
5. Docker, "Manage swarm service networks". https://docs.docker.com/engine/swarm/networking/ — VIP assigned when a service attached to a network publishes ports; DNS round-robin via `--endpoint-mode dnsrr`.
6. Kubernetes, "Service". https://kubernetes.io/docs/concepts/services-networking/service/ — "Pods are ephemeral resources (you should not expect that an individual Pod is reliable and durable)."; a Deployment "can create and destroy Pods dynamically"; clients should not "need to keep track of the set of backends themselves"; "Kubernetes updates the EndpointSlices for a Service whenever the set of Pods in a Service changes."
7. gRPC, "Custom Name Resolution". https://grpc.io/docs/guides/custom-name-resolution/ — "by default, DNS name resolution is used"; example target `dns:///grpc.io:50051`.
8. C. Richardson, microservices.io, "Pattern: Client-side service discovery" and "Pattern: Server-side service discovery". https://microservices.io/patterns/client-side-discovery.html, https://microservices.io/patterns/server-side-discovery.html — client queries a registry; server-side: client calls "a router (a.k.a load balancer) that runs at a well known location".
9. C. Richardson, microservices.io, "Pattern: Self Registration" and "Pattern: 3rd Party Registration". https://microservices.io/patterns/self-registration.html, https://microservices.io/patterns/3rd-party-registration.html — "A service instance is responsible for registering itself with the service registry."; "periodically renew its registration so that the registry knows it is still alive"; "The registrar can perform health checks on a service instance".
11. Docker, "Swarm mode key concepts". https://docs.docker.com/engine/swarm/key-concepts/ — verified in Lecture 02 (2026-10-27): "if a worker node becomes unavailable, Docker schedules that node's tasks on other nodes". Manager/worker and task roles are described there; the diagrams' addresses are illustrative.
10. etcd, "etcd API", Lease API, v3.6. https://etcd.io/docs/v3.6/learning/api/ — "The cluster grants leases with a time-to-live."; "A lease expires if the etcd cluster does not receive a keepAlive within a given TTL period."; "When a lease expires or is revoked, all keys attached to that lease will be deleted."; "Leases are refreshed using a bi-directional stream created with the `LeaseKeepAlive` API call."

12. AWS, "Using time to live (TTL) in DynamoDB". https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html — accessed 2026-11-10: "TTL allows you to define a per-item expiration timestamp that indicates when an item is no longer needed."; "DynamoDB automatically deletes expired items within a few days of their expiration time"; "Use filter expressions to remove expired items from Scan and Query results."
13. AWS Labs, "Amazon DynamoDB Lock Client" (README). https://github.com/awslabs/amazon-dynamodb-lock-client — accessed 2026-11-10: example withLeaseDuration(10 s) and withHeartbeatPeriod(3 s), "If I die, my lock will expire in 10 seconds."; another client can acquire a lock that "is stale (has passed the lease duration)". No default lease or heartbeat values are stated; 10 s / 3 s are the README's example values. Heartbeat: a background thread "continually updates the record version number on your locks"; expiry: a waiting client "checks the RecordVersionNumber of the lock (which is a GUID) and starts a timer" and expires it if it "still has the same GUID after the lease duration"; "The lock client never stores absolute times in DynamoDB".

14. Docker, "What is Docker?". https://docs.docker.com/get-started/docker-overview/ — accessed 2026-11-10: "An image is a read-only template with instructions for creating a Docker container."; "A container is a runnable instance of an image."; "A Docker registry stores Docker images."; Docker Hub is a public registry; pull/run pull images from the configured registry, push pushes to it. Swarm key concepts (11): "you specify which container image to use" when creating a service. (Chapter numbering: Docker overview is [12], DynamoDB TTL [13], Lock Client [14].)

## Not verified / not used

- etcd flat, lexically sorted key space and prefix range semantics (data model and API pages) were available only as model summaries, not verbatim text; the chapter states them modestly ("dogovor o prefiksima").

- Consul service-discovery page returned 404; Consul is not cited.
- Kubernetes Service DNS name format (`my-svc.my-namespace.svc...`) was available only as a summary; not used.
- `etcdctl lease grant / put --lease / lease keep-alive / get --prefix` commands follow the etcd documentation's usage but were not executed (etcd not installed). The lease ID is illustrative.
- Docker was not running; Compose and Swarm behaviour is documented, not demonstrated.

## Assets

- `assets/draw_diagrams.py` generates nine original diagrams (`code-image-container`, `swarm-overview`, `swarm-reschedule` and `etcd-keys` added 2026-11-10): `name-address`, `dns-tree` (names and steps illustrative), `ttl-stale`, `discovery-modes` (patterns as named by Richardson [8]), `lease-timeline`.
- `assets/dns-ttl.js` and `assets/lease-registry.js`: original self-contained simulators (no libraries, no network); models documented in their header comments.
- `lecture.css`, `lecture.hr.css` copied from Lecture 03.

## Legacy material

`references/legacy/RS-01-Intro.pdf` pp. 30–33 (distribution transparency, location and migration transparency; caching as mechanism vs policy) reviewed; used only as motivation for "name hides location" and the TTL policy discussion.
