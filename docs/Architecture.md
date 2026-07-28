# ClaimsIQ v2 Enterprise Platform Architecture

## Overview

ClaimsIQ v2 Enterprise Platform is designed as a cloud-native, modular, and scalable data engineering platform built entirely on AWS. The platform follows Infrastructure as Code (IaC) principles using Terraform, enabling repeatable, automated, and consistent infrastructure deployment.

The architecture separates networking, compute, storage, analytics, monitoring, and automation into independent modules, making the platform easier to maintain, scale, and extend.

---

## High-Level Architecture

```
                         GitHub Repository
                                │
                                ▼
                        GitHub Actions CI
                                │
                                ▼
                           Terraform IaC
                                │
                                ▼
                    AWS Infrastructure Platform
                                │
        ┌───────────────────────┼────────────────────────┐
        │                       │                        │
        ▼                       ▼                        ▼
   Networking               Compute                 Storage
   ──────────              ─────────             ───────────
   • VPC                  • EC2                 • S3 Bronze
   • Public Subnets       • Launch Template     • S3 Silver
   • Private Subnets      • Auto Scaling        • S3 Gold
   • Route Tables         • IAM Roles           • Scripts Bucket
   • Internet Gateway
   • NAT Gateway
   • Security Groups

                                │
                                ▼
                      Data Processing Layer
                                │
             ┌──────────────────┼──────────────────┐
             ▼                  ▼                  ▼
      Glue Catalog        Glue Crawler      Glue ETL Job

                                │
                                ▼
                         Analytics Layer

                         Amazon Athena

                                │
                                ▼
                      Monitoring & Operations

                         Amazon CloudWatch
```

---

## Architecture Layers

### Networking Layer

The networking layer provides secure communication between AWS resources. It consists of a Virtual Private Cloud (VPC), public and private subnets, route tables, Internet Gateway, NAT Gateway, and security groups. This layer isolates resources while allowing controlled internet access where required.

---

### Compute Layer

The compute layer uses Amazon EC2 instances deployed through Launch Templates and managed by an Auto Scaling Group. This enables automatic scaling and high availability based on workload demands.

---

### Storage Layer

Amazon S3 serves as the central data lake, organised into three logical layers:

- Bronze – Raw data
- Silver – Cleaned and transformed data
- Gold – Business-ready curated data

An additional scripts bucket stores ETL scripts used by AWS Glue.

---

### Data Processing Layer

AWS Glue provides metadata management and data transformation.

Components include:

- AWS Glue Data Catalog
- AWS Glue Crawlers
- AWS Glue ETL Jobs

These services automatically discover datasets and transform raw data into structured datasets suitable for analytics.

---

### Analytics Layer

Amazon Athena enables serverless SQL queries directly against data stored in Amazon S3 without requiring dedicated database infrastructure.

---

### Monitoring Layer

Amazon CloudWatch provides operational visibility through:

- Metrics
- Logs
- Dashboards
- Alarms

This allows continuous monitoring of infrastructure health and application performance.

---

### Automation Layer

Terraform provisions all infrastructure resources through reusable modules.

GitHub Actions performs automated validation by executing:

- Terraform Format Check
- Terraform Initialization
- Terraform Validation
- Terraform Plan

before infrastructure changes are merged.

---

## Design Principles

The platform has been designed around the following principles:

- Infrastructure as Code
- Modular architecture
- Scalability
- High availability
- Security by design
- Automation
- Reusability
- Operational visibility

---

## Future Enhancements

The architecture is designed to support future expansion without major redesign.

Planned enhancements include:

- Amazon Bedrock
- Retrieval-Augmented Generation (RAG)
- Intelligent document processing
- AI-powered claims assistant
- Multi-agent workflow orchestration