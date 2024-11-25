# About This Repo and Document
This is the top-level README for a sandbox application to complement the job application process for a Senior Full Stack Software Engineer position at 10x Genomics.

I haved name this project 11x as a cheeky homage to Christopher Guest's Nigel Tufnel from This is Spinal Tap, as 'turn it up to eleven' is a common refrain of mine and it seems appropriate here.

![11](https://github.com/user-attachments/assets/4114c07e-8dec-4a7e-8c7e-1cc7c291bfb7)

The purpose of this application is to dust off some molecular genetics skills and demonstrate some headstart on the domain knowledge required, wire something "interesting" and full-stack together to demonstrate technical skill, and provide something halfway digestible for discussion. This is by no means a perfect application and represents perhaps 30 hours of work, including domain knowledge uptake. There is no claim to being production ready, and theoretical proposed next steps will be outlined here and in the README files for the individual services. 

# Application Description and Philosophy
11X is a full stack application where one can generate mock FASTQ data, parse and analyze and that, and interact with that data in a web application. 

Architecture choices have been guided by trying to adhere to technologies outlined in the position description here: [https://careers.10xgenomics.com/careers/job/171824516809](https://careers.10xgenomics.com/careers/job/171824516809)

# Services Architecture Diagram
![Screenshot from 2024-11-25 11-33-21](https://github.com/user-attachments/assets/61b11317-e2ab-45cb-8e54-de1d5c1a7901)

# Services Stack Details
- Web App - React with Vite and SWC, Shadcn + TailwindCSS, Vitest + React Testing Library
- Gateway - Python with Flask, Levenshtein C extension module
- Mendel - Go with native HTTP Multiplexer, Levenshtein module

Each service has its own README with applicable information and instructions

# Screenshots

### 11x Home
![Screenshot from 2024-11-25 12-58-57](https://github.com/user-attachments/assets/46187ec3-bbc6-424f-bd72-1aafdf5c237b)

### Dashboard with React Component Profiler showing fetched data
![Screenshot from 2024-11-25 13-00-32](https://github.com/user-attachments/assets/c9b09d91-6597-4e6d-8d47-a9f37bd118a9)

### Data GOT (translation: past tense GET request) straight from Gateway
![Screenshot from 2024-11-25 13-01-29](https://github.com/user-attachments/assets/abd171af-c3c2-4543-83f0-8404edb2231c)

### Generated FASTQ files, R1 and R2 of same sample/lane side by side
![Screenshot from 2024-11-25 13-03-06](https://github.com/user-attachments/assets/ba664a59-669b-4f0f-8f73-20b5d738c959)

# Demo 

# Proposed High Level Next Steps
I'm probably not going to do these on my own accord, unless there is some expressed interest as a sort of coding test, in which case a request/directed task might be appropriate.
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



