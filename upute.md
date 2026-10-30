# Distributed Systems – Lecture & Slide Generation Instructions

Create university-level teaching material for the 12-week **Distributed Systems (Raspodijeljeni sustavi)** course.

## Course philosophy

Use **Martin Kleppmann's Cambridge Distributed Systems lectures/notes as the main theoretical reference and conceptual backbone**, supplemented with authoritative sources where necessary.

The course should combine:

- rigorous distributed-systems fundamentals;
- understanding *why* distributed systems are difficult;
- practical patterns used in contemporary software systems;
- cloud-native implementations and real-world architectures.

Do not turn the course into an AWS/Kubernetes tutorial. Technologies should illustrate distributed-systems concepts rather than replace them.

Target audience: computer science / informatics students who already know programming, databases, HTTP and basic software architecture.

## 12-week structure

1. **Introduction to Distributed Systems**
   - Definition and characteristics
   - Why distribute a system?
   - Scalability, availability and performance
   - Concurrency and partial failures
   - Client-server, P2P and distributed architectures
   - Real-world examples

2. **Communication in Distributed Systems**
   - Network communication from the application perspective
   - Request/response
   - Serialization
   - RPC and gRPC
   - REST
   - WebSockets
   - Synchronous vs asynchronous communication
   - Timeouts, retries and idempotency

3. **Failures and System Models**
   - Partial failure
   - Network failures
   - Crash-stop and crash-recovery
   - Byzantine failures
   - Synchronous, asynchronous and partially synchronous models
   - Two Generals Problem
   - Failure detection
   - Fault tolerance

4. **Time, Clocks and Ordering**
   - Physical clocks and clock drift
   - NTP and clock synchronization
   - Problems with timestamps
   - Causality
   - Happens-before relation
   - Lamport clocks
   - Vector clocks
   - Concurrent events

5. **Messaging and Event-Driven Systems**
   - Message queues
   - Publish/subscribe
   - Event-driven architecture
   - RabbitMQ and Redis as examples
   - Delivery semantics
   - Acknowledgements
   - Message ordering
   - Backpressure
   - Dead-letter queues
   - Idempotent consumers

6. **Replication and Consistency**
   - Reasons for replication
   - Leader/follower replication
   - Multi-leader approaches
   - Synchronous vs asynchronous replication
   - Quorums
   - Consistency models
   - Linearizability
   - Eventual consistency
   - Session guarantees
   - CAP theorem and its common misconceptions

7. **Consensus and Coordination**
   - Consensus problem
   - Leader election
   - Replicated state machines
   - Quorums and majority
   - Raft in detail
   - Terms, elections, logs and commits
   - Network partitions and split brain
   - Paxos overview
   - ZooKeeper/Consul as practical examples

8. **Distributed Transactions**
   - ACID in distributed environments
   - Distributed transaction problem
   - Two-Phase Commit
   - Coordinator failure and blocking
   - Three-Phase Commit briefly
   - Distributed locks
   - Saga pattern
   - Compensating transactions
   - Transactional outbox
   - Idempotency

9. **Distributed Data and Storage**
   - Partitioning/sharding
   - Replication combined with partitioning
   - Consistent hashing
   - Dynamo-style systems
   - Distributed caching
   - Redis
   - Distributed SQL and NoSQL
   - Google Spanner case study

10. **Microservices and Distributed Architecture**
   - Monolith vs distributed architecture
   - Microservices
   - Service boundaries
   - Service discovery
   - API gateways
   - Load balancing
   - Circuit breakers
   - Retries and exponential backoff
   - Bulkheads
   - Distributed tracing
   - Observability

11. **Cloud-Native Distributed Systems**
   - Containers as deployment units
   - Kubernetes/ECS/EKS concepts
   - Scheduling
   - Service discovery
   - Health checks
   - Load balancing
   - Autoscaling
   - Stateless services
   - Serverless/Lambda
   - Queues and event buses
   - Workflow orchestration / Step Functions

12. **Designing Reliable Distributed Systems**
   - Integrating concepts from the course
   - Availability and resilience
   - Redundancy
   - Graceful degradation
   - Failure isolation
   - Observability
   - Chaos/failure testing
   - Security considerations
   - Architecture trade-offs
   - Complete distributed-system design case study

## For each week, produce two artifacts

### 1. Lecture script

Write a complete lecturer's script suitable for approximately **90–120 minutes of teaching**.

The script should:

- establish 3–6 explicit learning outcomes;
- introduce concepts progressively;
- explain the reasoning behind algorithms rather than merely describing them;
- use concrete examples before or alongside formal definitions;
- include diagrams that should be shown;
- contain examples of failures and counterexamples;
- explicitly identify common misconceptions;
- connect new concepts to previous weeks;
- contain occasional questions that can be asked to students;
- include real-world examples from well-known distributed systems;
- distinguish fundamental principles from implementation-specific details.

For algorithms such as Lamport clocks, vector clocks, 2PC and Raft, walk through at least one concrete execution step-by-step.

When discussing trade-offs, avoid statements such as "X is better." Explain **under which assumptions X is preferable and what is sacrificed**.

### 2. Slides

Generate slides corresponding directly to the lecture script.

Aim for approximately **30–40 substantive slides per lecture**, adjusting when the subject requires it.

Prefer:

- diagrams;
- timelines;
- message-sequence diagrams;
- architecture diagrams;
- state machines;
- comparison tables;
- short examples;
- progressive/reveal-style explanations.

Avoid slides containing paragraphs copied from the script.

A typical slide should communicate **one main idea**.

For important algorithms, use several slides showing successive states rather than compressing the entire algorithm onto one slide.

Every diagram must have a teaching purpose and must be technically correct.

## Theory vs practice

Clearly distinguish:

**Fundamental concepts:** failure models, causality, ordering, replication, consistency, consensus, transactions, partitions.

**Patterns:** retries, idempotency, Saga, transactional outbox, circuit breaker, event-driven architecture.

**Implementations/products:** Raft implementations, RabbitMQ, Redis, ZooKeeper, Consul, Kubernetes, AWS services.

Students should understand the concept independently of the particular technology.

For example, do not teach "SQS" as a concept. Teach message queues and delivery semantics, then use SQS/RabbitMQ as implementations demonstrating those properties.

## Technical depth

Assume technically capable students.

Do not spend time explaining basic HTTP, JSON, SQL, Docker commands, etc., unless necessary for understanding a distributed-systems issue.

Prefer questions such as:

> What happens if this node crashes at this exact point?

> What can another node actually know?

> Can these two events be ordered?

> What happens during a network partition?

> Can retrying this request corrupt state?

> Which guarantee are we sacrificing?

Failure scenarios should appear throughout the course.

## Sources and correctness

Prioritize:

1. Martin Kleppmann's Distributed Systems course/notes.
2. *Designing Data-Intensive Applications* where appropriate.
3. Original or authoritative papers for important algorithms.
4. Official technical documentation for implementation-specific claims.

Do not invent guarantees provided by technologies.

Distinguish explicitly between:

- mathematically/theoretically guaranteed behavior;
- behavior guaranteed by a particular implementation;
- typical engineering practice.

Cite important claims and provide references at the end of each lecture.

## Continuity

Treat the 12 lectures as **one course rather than twelve independent presentations**.

Reuse terminology consistently.

Refer back to earlier concepts where appropriate.

Build conceptual dependencies deliberately:

**communication → failures → time/ordering → messaging → replication → consensus → transactions → distributed data → architecture → cloud → complete system design**

By Week 12, students should be able to analyze a distributed architecture by asking:

- What can fail?
- What assumptions does the system make?
- What happens during a partition?
- What ordering guarantees exist?
- Where is state stored?
- How is state replicated?
- What consistency guarantees exist?
- What operations require consensus?
- What happens when messages are duplicated?
- What happens when a component is unavailable?
- How does the system recover?
- Which trade-offs were deliberately chosen?
