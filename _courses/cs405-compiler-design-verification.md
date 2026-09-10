---
title: "Compiler Design, Code Optimization & Verification"
code: "CS-405"
credits: 4
department: "Computer Science and Engineering"
semester: "Spring"
level: "Undergraduate (Elective) / Graduate"
faculty: "Dr. Tanya Choudhury"
prerequisites: "CS-308: Principles of Programming Languages"
lecture_hours: 3
lab_hours: 2
description: "Front-end and back-end compiler pipeline construction: lexical analysis (Lex/Flex), parsing (LL/LR/LALR), intermediate representations (SSA form), dataflow analysis, LLVM optimization passes, and code generation."
topics:
  - module: "Module 1"
    title: "Lexing, Parsing & Abstract Syntax"
    description: "Finite automata, context-free grammars, recursive descent, shift-reduce parsing."
  - module: "Module 2"
    title: "Static Single Assignment (SSA) & IR"
    description: "Dominator trees, phi-functions, control flow graphs, LLVM IR syntax."
  - module: "Module 3"
    title: "Dataflow Analysis & Optimizations"
    description: "Liveness analysis, constant propagation, dead code elimination, loop unrolling."
  - module: "Module 4"
    title: "Instruction Selection & Register Allocation"
    description: "Tree-matching, Chaitin's graph coloring register allocation, RISC-V target code."
textbooks:
  - "Aho, A. V., Lam, M. S., Sethi, R., & Ullman, J. D. (2006). Compilers: Principles, Techniques, and Tools (2nd ed.). Pearson."
---

Students build an optimizing C-subset to LLVM compiler targeting RISC-V in Rust/C++.
