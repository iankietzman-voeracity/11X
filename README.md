# About This Repo and Document
This is the top-level README for a sandbox application to complement the job application process for a Senior Full Stack Software Engineer position at 10x Genomics.

The purpose of this application is to dust off some molecular genetics skills and demonstrate some headstart on the domain knowledge required, wire something "interesting" and full-stack together to demonstrate technical skill, and provide something halfway digestible for discussion. This is by no means a perfect application and represents perhaps 30 hours of work, including domain knowledge uptake. There is no claim to being production ready, and theoretical proposed next steps will be outlined here and in the README files for the individual services. 

# Application Description and Philosophy
11X is a full stack application where one can generate mock FASTQ data, parse and analyze and that, and interact with that data in a web application. 

Architecture choices have been guided by trying to adhere to technologies outlined in the position description here: [https://careers.10xgenomics.com/careers/job/171824516809](https://careers.10xgenomics.com/careers/job/171824516809)

# Services Architecture Diagram

# Services Stack Details
- Web App - React with Vite and SWC, Shadcn + TailwindCSS, Vitest + React Testing Library
- Gateway - Python with Flask, Levenshtein C extension module
- Mendel - Go with native HTTP Multiplexer, Levenshtein module

Each service has its own README with applicable information and instructions

# Screenshots

# Demo 

# Proposed High Level Next Steps
- Finish Dockerizing and composing services
- Add Github Actions for linting, testing, building, deployment
- Identify further abstraction candidates
- Concurrentify (is that a word?) and parallelize computationally heavy operations and move from Gateway to Mendel
- Lots of error handling
- Algorithmic improvements and benchmarking
- Memory store to eliminate processing the same underlying data upon every request
- Change Gateway-Mendel communication protocol to gRPC
- Change file reads/writes to streams
- Additional front front end features and data visualization



