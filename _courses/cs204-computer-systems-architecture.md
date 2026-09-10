---
title: "Computer Systems Architecture & Pipelining"
code: "CS-204"
credits: 4
department: "Computer Science and Engineering"
semester: "Spring"
level: "Undergraduate (Core)"
faculty: "Dr. Rajesh Sen"
prerequisites: "CS-102: Data Structures & Algorithmic Analysis"
lecture_hours: 3
lab_hours: 2
description: "Microarchitectural design of modern RISC processors, pipelining, dynamic branch prediction, out-of-order superscalar execution, memory hierarchy, caches, and cache coherence."
topics:
  - module: "Module 1"
    title: "Instruction Set Architectures & RISC-V"
    description: "Assembly programming, register conventions, addressing modes, ABI."
  - module: "Module 2"
    title: "Pipelined Datapath & Hazard Resolution"
    description: "Structural, data, and control hazards, forwarding paths, branch prediction."
  - module: "Module 3"
    title: "Cache Hierarchies & Coherence"
    description: "Direct-mapped and set-associative caches, write policies, MESI coherence."
  - module: "Module 4"
    title: "Superscalar & Speculative Execution"
    description: "Tomasulo's algorithm, reorder buffers, memory disambiguation."
textbooks:
  - "Patterson, D. A., & Hennessy, J. L. (2020). Computer Organization and Design RISC-V Edition. Morgan Kaufmann."
---

Students develop a cycle-accurate 5-stage RISC-V processor in Verilog/SystemVerilog and measure instructions per cycle (IPC) on FPGA testbenches.
