---
title: "P4-Driven Dynamic Routing and Congestion Control in High-Throughput Datacenter Fabrics"
slug: "p4-datacenter-congestion-control"
authors:
  - "Dr. Vikram Singh"
  - "Dr. Alok Mukherjee"
  - "Nitin Bhat"
venue: "ACM SIGCOMM 2024"
volume: "54"
issue: "4"
pages: "118-132"
year: 2024
doi: "10.1145/3651890.3672230"
research_area: "Computer Networks"
bibtex: |
  @inproceedings{singh2024p4datacenter,
    author={Singh, Vikram and Mukherjee, Alok and Bhat, Nitin},
    booktitle={ACM SIGCOMM 2024 Conference}, 
    title={P4-Driven Dynamic Routing and Congestion Control in High-Throughput Datacenter Fabrics}, 
    year={2024},
    pages={118-132}
  }
---

### Abstract

Modern high-bandwidth RDMA networks suffer severe throughput degradation under incast traffic bursts. We present FastFlow-P4, an in-band telemetry control loop that monitors egress queue depth directly within programmable switch pipelines and injects explicit flow-pacing headers back to senders within 4 microseconds, cutting incast drop rates to near zero.
