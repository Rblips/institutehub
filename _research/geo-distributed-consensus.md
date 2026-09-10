---
title: "Fault-Tolerant Consensus for Geo-Distributed Hybrid Clouds"
slug: "geo-distributed-consensus"
area: "Distributed Systems"
department: "Computer Science and Engineering"
principal_investigator: "Dr. Aravind Nair"
team:
  - "Dr. Karthik Venkatesh"
  - "Rahul Sharma (Ph.D. Candidate)"
  - "Ananya V (Research Fellow)"
funding_agency: "National Science & Technology Board & CloudTech Labs"
duration: "2023 - 2026"
status: "Active"
lab: "Distributed & Networked Systems Lab"
description: "Developing adaptive, low-latency Byzantine and Crash Fault-Tolerant consensus protocols optimized for cross-continent data replication and WAN latency jitter."
technologies:
  - "Raft & Paxos Variants"
  - "Rust"
  - "eBPF Network Instrumentation"
  - "gRPC / Protobuf"
publications:
  - "Adaptive Consensus in Geo-Distributed Byzantine Fault-Tolerant Networks (IEEE TPDS 2024)"
  - "Low-Latency Quorum Systems for Edge-to-Cloud Workloads (ACM TOCS 2023)"
---

Large-scale enterprise workloads and multinational financial infrastructure increasingly span across multiple geographic cloud regions and edge clusters. Traditional consensus protocols (such as standard Raft or Multi-Paxos) suffer drastic throughput collapses when wide-area network (WAN) links experience asymmetric latency, packet drops, or transient partition anomalies.

The **Geo-Distributed Consensus Project** investigates novel topology-aware quorum formations, speculative execution paths, and hardware-accelerated state-machine replication. Our research prototypes demonstrate up to a 64% reduction in tail commit latencies across trans-Atlantic and trans-Pacific benchmarks while maintaining strictly serializable correctness guarantees.
