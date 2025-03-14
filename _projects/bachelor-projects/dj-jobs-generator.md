---
title: "DL Jobs Generator"
supervisors: ["Kawsar Haghshenas", "Mahmoud Alasmar"]
available: false
date: 2024-11-01
type: bachelor
---
In this project you will implement a job generator process. As an input, a JSON configuration (JSON) file and jobs generation rate (jobs per unit time) will be provided. The configuration file contains metadata about different Deep learning jobs, such as the path to the executable file and required arguments. Your task is to design and implement a generator which works as follows: Randomly select a job from the JSON file, use the metadata of the selected job to prepare a YAML/Batch script, a script template will be provided, and submit the prepared script to another process using an RPC protocol. The rate at which a job is sampled and submitted should be equal to the given generation rate. In addition, an implementation of an RPC protocol is required, the description of the protocol will be provided. You may choose any programming language for coding, but advisably to use Python. You will be provided with a supplementary code with helper functions, RPC protocol description and script/configuration files description. 