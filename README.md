# Widest Path in Networks with Gains and Losses
This repository contains the implementation of the code described in the paper: [https://www.mdpi.com/2075-1680/13/2/127](https://www.mdpi.com/2075-1680/13/2/127).

Please note that the specifications in this repository differ from those in the paper. The new experiments were conducted on the following hardware:

- **CPU**: Intel i7-13700F
  - **Base Frequency**: 2.1 GHz
  - **Turbo Frequency**: 5.2 GHz
  - **Cores**: 16 (8 performance cores + 8 efficient cores)
  - **L1 Cache**: 1.4 MB 
  - **L2 Cache**: 24.0 MB 
  - **L3 Cache**: 30.0 MB
- **GPU**: NVIDIA GeForce RTX 4070TI
  - **Memory**: 12 GB GDDR6X, 21008 MHz
  - **CUDA Cores**: 7680
- **RAM**: 32 GB DDR5, 4800 MHz, Dual Channel (16+16 GB)
- **CUDA Version**: 12.5

In the paper, the following table of reference is provided for the networks generated:

| ID | No. of Instances | No. of Nodes | No. of Paths | Erdős–Rényi Probability |
|----|------------------|--------------|--------------|-------------------------|
| 1  | 10000            | 1000         | 500          | 0.5                     |
| 2  | 10000            | 1000         | 500          | 0.7                     |
| 3  | 10000            | 1000         | 500          | 0.9                     |
| 4  | 1000             | 2000         | 1000         | 0.1                     |
| 5  | 1000             | 2000         | 1000         | 0.15                    |
| 6  | 1000             | 2000         | 1000         | 0.6                     |
| 7  | 1000             | 2000         | 1000         | 0.6                     |
| 8  | 100              | 5000         | 2500         | 0.1                     |
| 9  | 100              | 5000         | 2500         | 0.2                     |
| 10 | 100              | 5000         | 2500         | 0.3                     |
| 11 | 5                | 10000        | 5000         | 0.15                    |
| 12 | 5                | 10000        | 5000         | 0.3                     |
| 13 | 5                | 10000        | 5000         | 0.5                     |
| 14 | 3                | 15000        | 7500         | 0.15                    |
| 15 | 2                | 20000        | 7500         | 0.15                    |
| 16 | 1                | 25000        | 8000         | 0.15                    |

*Table 1: Network generator parameters used for experiments.*

Due to complications (too many arcs generated) during path generation, this project uses the number of arcs generated as a reference. Therefore, the number of paths will be much lower, but this does not mean that only the given number of paths are present; it merely ensures the minimum.

`*` indicates missing data in my notes. The C++ code used in the paper was not versioned. I will attempt to recover it from my old computer, or, if necessary, rewrite it.

If you notice discrepancies in the configurations compared to the paper's parameters, it is because I am following the specifications in Table 2, which focus on the actual size of the networks.

| No. of Nodes | Erdős–Rényi Probability | No. of Arcs |
|--------------|-------------------------|-------------|
| 1000         | 0.5                     | 502,949     |
| 1000         | 0.7                     | 702,955     |
| 1000         | 0.9                     | 900,158     |
| 2000         | 0.1                     | 406,696     |
| 2000         | 0.15                    | 608,077     |
| 2000         | 0.6                     | 2,413,862   |
| 2000         | 0.6                     | 2,526,737   |
| 5000         | 0.1                     | 5,041,275   |
| 5000         | 0.2                     | 7,556,983   |
| 5000         | 0.3                     | 15,124,614  |
| 10000        | 0.15                    | 15,124,614  |
| 10000        | 0.3                     | 20,161,784  |
| 10000        | 0.5                     | 50,356,783  |
| 15000        | 0.15                    | 34,007,566  |
| 20000        | 0.15                    | 60,441,434  |
| 25000        | 0.15                    | *           |
| 30000        | 0.15                    | 36,256,723  |

*Table 2: Number of arcs per instance.*