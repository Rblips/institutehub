---
title: "Advanced Distributed Systems & Consensus Protocols"
code: "CS-401"
credits: 4
department: "Computer Science and Engineering"
semester: "Autumn"
level: "Undergraduate (Advanced) / Graduate"
faculty: "Dr. Aravind Nair"
prerequisites: "CS-201: Operating Systems Principles"
lecture_hours: 3
lab_hours: 2
description: "Theoretical and algorithmic foundations of distributed computing: clock synchronization, vector clocks, snapshot algorithms, FLP impossibility, Paxos, Raft, Byzantine consensus, and distributed transactions."
topics:
  - module: "Module 1"
    title: "Time, Clocks & Ordering"
    description: "Lamport timestamps, vector clocks, consistent global snapshots, Chandy-Lamport."
  - module: "Module 2"
    title: "Fault Tolerance & Consensus"
    description: "Crash vs Byzantine failure models, FLP impossibility theorem, Multi-Paxos, Raft."
  - module: "Module 3"
    title: "Distributed Storage & Transactions"
    description: "CAP theorem, PACELC, Two-Phase Commit (2PC), Google Spanner, TrueTime."
  - module: "Module 4"
    title: "Peer-to-Peer & Decentralized Ledgers"
    description: "Distributed hash tables (Chord/Kademlia), proof-of-work/stake consensus."
textbooks:
  - "van Steen, M., & Tanenbaum, A. S. (2023). Distributed Systems (4th ed.). Pearson."
  - "Kleppmann, M. (2017). Designing Data-Intensive Applications. O'Reilly."
---

Students build a replicated key-value storage engine in Rust/Go that passes strict network partition chaos testing.
