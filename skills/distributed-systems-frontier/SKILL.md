---
name: distributed-systems-frontier
description: "Distributed systems primitives: consensus (Raft, Paxos, EPaxos, Multi-Paxos), CRDT (G-Counter, OR-Set, RGA, Yjs, Automerge), vector clocks, HLC, CALM theorem, saga, eventual consistency, causal consistency, Jepsen testing. Triggers on Raft, Paxos, consensus, CRDT, Yjs, Automerge, vector clock, HLC, distributed consistency, Jepsen."
category: architecture
tags: [raft, paxos, crdt, consensus, distributed, yjs, automerge, jepsen]
---

# Distributed Systems Frontier

## Consensus algorithms

| Algorithm | Use | Complexity |
|-----------|-----|------------|
| **Raft** | Leader-based log replication | Understandable, default choice |
| **Multi-Paxos** | Classic leader-based | Harder to implement |
| **EPaxos** | Leaderless, low-latency WAN | Complex; few production uses |
| **PBFT / Tendermint** | Byzantine fault tolerance | Blockchains |
| **ViewStamped Replication** | Pre-Paxos equivalent | Academic mostly |
| **Zab** | ZooKeeper's broadcast | Specialized |

### Raft in 30s
- Elect a leader (randomized timeout)
- Leader replicates log entries to followers (majority ack)
- Committed entries applied to state machine
- New election on leader failure
- Popular libs: **etcd/raft** (Go), **hashicorp/raft** (Go), **tikv/raft-rs** (Rust), **openraft** (Rust), **async-raft** (Rust)

### When consensus
Use when you need: single source of truth, linearizable reads/writes, leader election, config management. Systems: etcd, Consul, ZooKeeper, CockroachDB, TiKV, Nomad.

## CRDTs (Conflict-free Replicated Data Types)

Data structures that merge concurrent updates deterministically — no coordination needed. Trade strong consistency for availability + eventual consistency (CAP: AP).

### Types

| CRDT | What | Use |
|------|------|-----|
| **G-Counter** | Grow-only counter | Analytics, likes |
| **PN-Counter** | +/- counter | Inventory |
| **G-Set** / **OR-Set** | Add-only / add+remove set | Tags, members |
| **LWW-Register** | Last-write-wins | Single-value config |
| **RGA / Treedoc** | Ordered list | Collaborative text |
| **Yjs / Automerge** | Document CRDTs | Collaborative editors, local-first apps |

### Yjs example (collaborative edits)
```javascript
import * as Y from 'yjs';
import { WebsocketProvider } from 'y-websocket';

const doc = new Y.Doc();
const provider = new WebsocketProvider('wss://...', 'room-1', doc);
const ytext = doc.getText('content');
ytext.insert(0, 'Hello ');
// Changes propagate to all connected peers, merge automatically
```

Backends: y-websocket, y-webrtc, y-indexeddb (offline), Liveblocks, Partykit.

### Automerge (Rust/JS)
```javascript
import * as Automerge from '@automerge/automerge';
let doc = Automerge.change(Automerge.init(), d => { d.tasks = []; });
doc = Automerge.change(doc, d => d.tasks.push({ text: 'foo', done: false }));
// Binary sync protocol between peers
```

## Clocks

| Clock | Detects |
|-------|---------|
| **Lamport timestamps** | Partial causal order |
| **Vector clocks** | Full causal order per-node |
| **Version vectors** | Per-key causality |
| **HLC (Hybrid Logical Clock)** | Causal + wall-clock proximity (CockroachDB, MongoDB) |
| **TrueTime** (Google Spanner) | Bounded clock uncertainty |

## Consistency models (strong → weak)

1. **Linearizable** — real-time ordered, single global timeline
2. **Sequential** — some total order, not necessarily real-time
3. **Causal** — respects happens-before
4. **Eventual** — converges if no new writes
5. **PRAM** / **Read-your-writes** / **Monotonic reads** — session guarantees

CAP: pick 2 of {Consistent, Available, Partition-tolerant} under partition. PACELC extends: Else (no partition) pick {Latency, Consistency}.

## CALM theorem
Monotonic programs (where additions don't invalidate prior conclusions) can run consistently without coordination. Use as design principle for CRDT-friendly architectures.

## Saga pattern

Long-running transactions via compensating actions instead of 2PC.
- **Choreography**: each service reacts to events, no central orchestrator
- **Orchestration**: central saga orchestrator (Temporal, Cadence, AWS Step Functions)

## Jepsen testing

Aphyr's framework for testing distributed DB correctness under network partitions, clock skew, pauses. Essential for claims of linearizability.

```clojure
;; Jepsen test: fault injection + linearizability checker (Knossos)
```

Run before claiming CP properties. Many DBs have been caught violating claims (MongoDB, CockroachDB, Redis, FaunaDB) via Jepsen.

## Production-ready libs

| Need | Lib |
|------|-----|
| Raft consensus (Go) | hashicorp/raft, etcd/raft |
| Raft (Rust) | openraft, tikv/raft-rs |
| CRDT docs (JS) | Yjs, Automerge |
| CRDT sync protocol | matrix (Olm/Megolm), Replicache, Partykit |
| Workflow orchestration | Temporal, Cadence, Dapr, Restate |
| Consensus-backed KV | etcd, TiKV, Consul |
| Distributed transactions | Spanner, CockroachDB, FoundationDB, YugabyteDB |

## Common pitfalls

- Trying to achieve linearizability across WAN → high tail latency; use causal consistency where possible
- Implementing your own Raft → use proven library; edge cases abound
- Two-phase commit under partition → blocks forever; use saga or try/compensate
- Relying on wall-clock time for ordering → use HLC or vector clocks
- CRDTs for data with hard constraints (e.g., unique usernames) → CRDTs can't enforce uniqueness
- Overestimating leader-based speed → leaderless (EPaxos) or CRDTs lower tail latency
- Testing only happy path → Jepsen for production systems

## References
- Ongaro & Ousterhout — Raft (USENIX 2014)
- Lamport — Paxos Made Simple (2001)
- Shapiro et al. — CRDTs comprehensive survey (2011)
- Kleppmann — *Designing Data-Intensive Applications*
- Kleppmann — Local-First Software (2019)
- jepsen.io analyses
- aphyr.com (Kyle Kingsbury)

## Related
- `event-sourcing-architect` (existing) — natural fit with CRDTs
- `saga-orchestration` (existing) — distributed transaction pattern
- `temporal-python-pro` (existing) — workflow orchestration
