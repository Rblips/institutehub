---
title: "eBPF-Driven Runtime Kernel Compartmentalization & Threat Defense"
slug: "ebpf-kernel-security"
area: "Operating Systems"
department: "Computer Science and Engineering"
principal_investigator: "Dr. Rajesh Sen"
team:
  - "Dr. Suresh Iyer"
  - "Gaurav Malhotra (Postdoc Fellow)"
  - "Divya S (Systems Engineer)"
funding_agency: "Cyber Defense Innovation Agency & Linux Systems Foundation"
duration: "2023 - 2026"
status: "Active"
lab: "Systems Architecture and Resilience (SAR) Lab"
description: "Hardening monolithic Linux kernels against privilege escalation and zero-day memory exploits using in-kernel extended Berkeley Packet Filter (eBPF) telemetry and memory safety boundaries."
technologies:
  - "Linux Kernel (C & Rust)"
  - "Extended BPF (eBPF)"
  - "Hardware-Enforced Memory Tagging (ARM MTE / Intel CET)"
  - "QEMU Virtualization"
publications:
  - "Hardware-Assisted Kernel Compartmentalization for Monolithic UNIX Systems (USENIX Security 2024)"
  - "Zero-Cost Memory Boundary Enforcement in Linux eBPF Subsystems (ACM ASPLOS 2022)"
---

Modern server operating systems run monolithic kernels where a single kernel-space flaw or vulnerable loadable module can compromise the entire computing perimeter. 

The **Runtime Kernel Compartmentalization Project** uses safe eBPF bytecode programs combined with modern CPU hardware memory tagging to enforce dynamic privilege boundaries between device drivers, network protocol stacks, and file systems. When an anomalous control-flow hijacking or use-after-free attempt occurs, the subsystem is isolated in microsecond intervals without crashing the host OS.
