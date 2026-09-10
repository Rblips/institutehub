---
title: "Predictive Cold-Start Mitigation for Serverless Functions via eBPF Tracing"
slug: "predictive-serverless-cold-start"
authors:
  - "Dr. Karthik Venkatesh"
  - "Dr. Aravind Nair"
  - "Harish Rao"
venue: "ACM European Conference on Computer Systems (EuroSys 2024)"
volume: "19"
issue: "EuroSys"
pages: "240-255"
year: 2023
doi: "10.1145/3627703.3629571"
research_area: "Distributed Systems"
bibtex: |
  @inproceedings{venkatesh2024serverless,
    author={Venkatesh, Karthik and Nair, Aravind and Rao, Harish},
    booktitle={Proceedings of the 19th European Conference on Computer Systems (EuroSys 2024)}, 
    title={Predictive Cold-Start Mitigation for Serverless Functions via eBPF Tracing}, 
    year={2024},
    pages={240-255}
  }
---

### Abstract

Function-as-a-Service (FaaS) platforms suffer substantial cold-start penalties when instantiating new isolated execution containers. We design FastFork, an in-kernel eBPF tracking system that monitors container memory access patterns during initialization and pre-warms snapshot states 85ms before peak invocation arrivals, cutting cold-start delays by 78%.
