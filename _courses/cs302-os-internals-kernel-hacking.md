---
title: "Linux Operating Systems Internals & Kernel Engineering"
code: "CS-302"
credits: 4
department: "Computer Science and Engineering"
semester: "Autumn"
level: "Undergraduate (Elective) / Graduate"
faculty: "Dr. Rajesh Sen"
prerequisites: "CS-201: Operating Systems Principles"
lecture_hours: 3
lab_hours: 2
description: "In-depth study of the Linux kernel source code, custom loadable kernel modules (LKMs), process scheduler implementation (CFS), VFS layer, eBPF telemetry, and kernel memory allocators (SLUB/buddy)."
topics:
  - module: "Module 1"
    title: "Kernel Architecture & Boot Sequence"
    description: "Kernel compilation, early init, page table initialization, system call dispatcher."
  - module: "Module 2"
    title: "Process Management & CFS Scheduling"
    description: "task_struct, Completely Fair Scheduler, red-black runqueues, priority inversion."
  - module: "Module 3"
    title: "Virtual File System (VFS) & Device Drivers"
    description: "Inodes, dentries, superblocks, character/block driver registration, DMA."
  - module: "Module 4"
    title: "eBPF Subsystem & Kernel Tracing"
    description: "eBPF verifier, maps, kprobes, tracepoints, and XDP fast packet filtering."
textbooks:
  - "Love, R. (2010). Linux Kernel Development (3rd ed.). Addison-Wesley."
  - "Gregg, B. (2019). BPF Performance Tools. Addison-Wesley."
---

Students write real loadable kernel modules, patch the Linux kernel scheduler, and deploy custom eBPF performance profilers on real Linux servers.
