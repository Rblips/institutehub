---
title: "Hardware-Assisted Kernel Compartmentalization for Monolithic UNIX Systems"
slug: "hardware-assisted-kernel-compartmentalization"
authors:
  - "Dr. Rajesh Sen"
  - "Dr. Suresh Iyer"
  - "Gaurav Malhotra"
venue: "USENIX Security Symposium 2024"
volume: "33"
issue: "Security'24"
pages: "310-327"
year: 2024
doi: "10.5555/usenixsec24.sen"
research_area: "Operating Systems"
bibtex: |
  @inproceedings{sen2024kernel,
    author={Sen, Rajesh and Iyer, Suresh and Malhotra, Gaurav},
    booktitle={33rd USENIX Security Symposium (USENIX Security 24)}, 
    title={Hardware-Assisted Kernel Compartmentalization for Monolithic UNIX Systems}, 
    year={2024},
    pages={310-327}
  }
---

### Abstract

We design and evaluate K-Guard, a compiler pass and Linux kernel extension that splits device drivers and unverified network stacks into isolated privilege domains utilizing ARM Memory Tagging Extension (MTE) and Intel MPK. K-Guard prevents privilege escalation across 94% of historical CVE exploits with less than 2.8% benchmark CPU overhead.
