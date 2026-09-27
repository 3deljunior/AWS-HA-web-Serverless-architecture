# End-to-End AWS Cloud Architecture: High-Availability Web & Serverless Pipeline

## 📌 Project Summary
I designed and manually provisioned this multi-tier cloud architecture from scratch in the AWS **Frankfurt** region. The project demonstrates hands-on implementation of custom VPC networking, private subnet isolation, container deployment via `Amazon ECR`, high-availability database replication, and an event-driven serverless file compression pipeline.

![Architecture Diagram](./assets/architecture-diagram.png)

---

## 🌐 Custom Network & Routing Design

I configured a custom `VPC` divided into isolated public and private tiers across five subnets with custom route tables[cite: 1, 2]:

| Tier | Subnet CIDR | Provisioned Resources | Route Table Configuration |
| :--- | :--- | :--- | :--- |
| **Public Tier** | `10.0.0.0/20`[cite: 1, 2] | `Bastion Host` (`Port 22`)[cite: 1, 2] | `0.0.0.0/0` -> `IGW`[cite: 1, 2] |
| **Private App Tier** | `10.0.128.0/20`, `10.0.144.0/20`[cite: 1, 2] | `Web Server` EC2s in `Auto Scaling group`[cite: 1, 2] | `0.0.0.0/0` -> `NAT GW`<br>`S3` -> `GW-endpoint`[cite: 1, 2] |
| **Private DB Tier** | `10.0.48.0/20`, `10.0.64.0/20`[cite: 1, 2] | `Amazon RDS` (`Main` & `FailOver`)[cite: 1, 2] | Internal VPC Routing[cite: 1, 2] |

---

## 🛠️ Step-by-Step Implementation Breakdown

### 1. VPC, Subnets & Connectivity
* Created a custom `VPC` in the **Frankfurt** region with an attached Internet Gateway (`IGW`)[cite: 1, 2].
* Configured a `Public Route table` routing `0.0.0.0/0` to the `IGW` for public resources[cite: 1, 2].
* Deployed a `Regional NAT GW` and configured the `Private Route table` (`0.0.0.0/0` -> `NAT GW`) so private instances can securely reach the `Public Internet` for updates and image pulls without exposing public IPs[cite: 1, 2].
* Provisioned a VPC `GW Endpoint` for `S3` (`S3` -> `GW-endpoint`) to keep storage traffic entirely inside the AWS network and eliminate NAT data transfer costs[cite: 1, 2].

### 2. Security & Administrative Access
* Deployed a `Bastion Host` in the public subnet (`10.0.0.0/20`) locked down via Security Group to `Port 22` for secure SSH administration of private instances[cite: 1, 2].
* Configured the private tier Security Group to allow inbound traffic on `Port 22,80` (SSH from the `Bastion Host` and HTTP from the `ALB`)[cite: 1, 2].
* Attached a custom `IAM Role` to the `Web Server` instances granting least-privilege access to `Amazon ECR` and the `S3 Bucket`[cite: 1, 2].

### 3. Compute, Containers & Auto Scaling
* Built the web application container image and pushed it to a private `Amazon ECR` repository[cite: 1, 2].
* Created a Launch Template and `Auto Scaling group` spanning private subnets `10.0.128.0/20` and `10.0.144.0/20` to automatically pull the image from `Amazon ECR` and run the `Web Server` containers[cite: 1, 2].
* Configured an Application Load Balancer (`ALB`) to distribute incoming user traffic across the `Auto Scaling group`[cite: 1, 2].
* Integrated the `Auto Scaling group` with Amazon `SNS` to send real-time `Email` alerts on instance scaling events[cite: 1, 2].

### 4. High-Availability Database Layer
* Deployed `Amazon RDS` in a Multi-AZ configuration across dedicated private database subnets[cite: 1, 2].
* Placed the `Main` primary database in `10.0.48.0/20` with automated synchronous replication (`Sync`) to a `FailOver` standby instance in `10.0.64.0/20` for automatic disaster recovery[cite: 1, 2].

### 5. Serverless S3 & Lambda Media Pipeline
* Configured `Web Server` instances to upload raw assets into a source `S3 Bucket` via the `GW Endpoint`[cite: 1, 2].
* Set up an S3 Event Notification with a `Filter` rule that triggers an AWS `Lambda` function whenever new objects are uploaded[cite: 1, 2].
* Wrote the `Lambda` function to execute automated `Compression` and output the optimized files into a secondary destination `S3 Bucket`[cite: 1, 2].

---

## 📸 Deployment Verification
*(Add your AWS Console screenshots here)*
* **VPC Resource Map:** `./assets/screenshots/vpc-resource-map.png`
* **Auto Scaling & ALB Target Health:** `./assets/screenshots/asg-instances.png`
* **RDS Multi-AZ Status:** `./assets/screenshots/rds-multi-az.png`
* **Lambda Execution Logs & Compressed S3 Output:** `./assets/screenshots/s3-lambda-compression.png`
