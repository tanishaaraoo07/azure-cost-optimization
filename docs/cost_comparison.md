# Cost Comparison of Azure Cost Optimizer

## Overview

This document provides a detailed comparison of costs incurred before and after the implementation of the Azure Cost Optimizer project. The goal of this project is to optimize data storage and retrieval processes, thereby reducing overall operational costs.

## Cost Analysis

### Before Implementation

- **Storage Costs**: 
  - Monthly cost for Cosmos DB: $X
  - Estimated data size: Y GB
  - Cost per GB: $Z

- **Retrieval Costs**:
  - Average number of retrieval operations per month: A
  - Cost per operation: $B

- **Total Monthly Cost**: 
  - Storage Cost + Retrieval Cost = $X + (A * $B)

### After Implementation

- **Storage Costs**: 
  - Monthly cost for Cosmos DB: $C
  - Monthly cost for Archive Storage: $D
  - Estimated data size in Cosmos DB: E GB
  - Estimated data size in Archive Storage: F GB
  - Cost per GB for Cosmos DB: $G
  - Cost per GB for Archive Storage: $H

- **Retrieval Costs**:
  - Average number of retrieval operations per month: I
  - Cost per operation from Cosmos DB: $J
  - Cost per operation from Archive Storage: $K

- **Total Monthly Cost**: 
  - Storage Cost + Retrieval Cost = ($C + $D) + (I * $J + (F * $K))

## Summary of Savings

- **Total Cost Before Implementation**: $Total_Before
- **Total Cost After Implementation**: $Total_After
- **Monthly Savings**: $Total_Before - $Total_After

## Conclusion

The implementation of the Azure Cost Optimizer has resulted in significant cost savings by optimizing data storage and retrieval processes. This document serves as a reference for understanding the financial benefits of the project and can be used to justify further investments in optimization technologies.