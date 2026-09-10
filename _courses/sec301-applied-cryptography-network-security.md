---
title: "Applied Cryptography, TLS & Zero-Trust Network Defense"
code: "SEC-301"
credits: 4
department: "Computer Science and Engineering"
semester: "Spring"
level: "Undergraduate (Elective)"
faculty: "Dr. Suresh Iyer"
prerequisites: "CS-305: Computer Networks & Internet Protocol Engineering"
lecture_hours: 3
lab_hours: 2
description: "Mathematical and practical foundations of modern cryptography: symmetric block ciphers (AES-GCM), asymmetric cryptography (RSA, ECC), digital signatures, TLS 1.3 protocol dissection, PKI, and Post-Quantum Cryptography (ML-KEM/Kyber)."
topics:
  - module: "Module 1"
    title: "Symmetric Encryption & Authenticated Modes"
    description: "AES, ChaCha20-Poly1305, Galois Counter Mode (GCM), cryptanalysis fundamentals."
  - module: "Module 2"
    title: "Public-Key Cryptography & Key Exchange"
    description: "Diffie-Hellman, ECDH, Ed25519 signatures, lattice-based post-quantum primitives."
  - module: "Module 3"
    title: "TLS 1.3 Protocol & Key Schedule"
    description: "0-RTT session resumption, certificate verification, OCSP stapling, forward secrecy."
  - module: "Module 4"
    title: "Zero Trust Architecture & Enterprise Hardening"
    description: "Mutual TLS (mTLS), identity-aware proxies, credential vaulting, OpenSSL CLI."
textbooks:
  - "Katz, J., & Lindell, Y. (2020). Introduction to Modern Cryptography (3rd ed.). CRC Press."
---

Students implement cryptographic hash algorithms, dissect raw TLS 1.3 packets, and configure hardened Nginx reverse proxies with SSL/TLS cipher suites.
