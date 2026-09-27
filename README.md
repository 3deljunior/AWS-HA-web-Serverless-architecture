# End-to-End AWS Cloud Architecture: High-Availability Flask Web App & Serverless Image Filtering Pipeline

## 📌 Project Summary
I designed and manually provisioned this multi-tier cloud architecture from scratch in the AWS **Frankfurt** region[cite: 2]. The project features a Dockerized Python Flask web application deployed via `Amazon ECR` across a private `Auto Scaling group`, backed by a Multi-AZ `Amazon RDS` database and an event-driven AWS `Lambda` pipeline that automatically applies an image `Filter` to files uploaded to Amazon S3[cite: 2].

![Architecture Diagram](./assets/architecture-diagram.png)

---

## 🌐 Custom Network & Routing Design

The custom `VPC` is segmented into isolated public and private tiers across five subnets with dedicated route tables[cite: 2]:

| Tier | Subnet CIDR | Provisioned Resources | Route Table Configuration |
| :--- | :--- | :--- | :--- |
| **Public Tier** | `10.0.0.0/20`[cite: 2] | `Bastion Host` (`Port 22`)[cite: 2] | `0.0.0.0/0` -> `IGW`[cite: 2] |
| **Private App Tier** | `10.0.128.0/20`, `10.0.144.0/20`[cite: 2] | Containerized Flask `Web Server` EC2s in `Auto Scaling group`[cite: 2, 3] | `0.0.0.0/0` -> `NAT GW`<br>`S3` -> `GW-endpoint`[cite: 2] |
| **Private DB Tier** | `10.0.48.0/20`, `10.0.64.0/20`[cite: 2] | `Amazon RDS` (`Main` & `FailOver`)[cite: 2] | Internal VPC Routing[cite: 2] |

---

## 🛠️ Architecture & Implementation Breakdown

### 1. VPC Networking & Private Connectivity
* Provisioned a custom `VPC` in **Frankfurt** with an Internet Gateway (`IGW`) and a `Public Route table` (`0.0.0.0/0` -> `IGW`)[cite: 2].
* Deployed a `Regional NAT GW` in the `Private Route table` (`0.0.0.0/0` -> `NAT GW`) so private instances can securely pull packages and container images without public IP exposure[cite: 2].
* Configured a VPC Gateway Endpoint (`GW Endpoint`) for `S3` (`S3` -> `GW-endpoint`) so all image transfers between the `Web Server` instances and the `S3 Bucket` remain on the private AWS network[cite: 2].

### 2. Containerized Flask Application & Auto Scaling (`my-flask-app/`)
* Developed a Python Flask web application (`app.py`, `templates/index.html`, `requirements.txt`) and packaged it into a container image using a custom `Dockerfile` and `.dockerignore`[cite: 3].
* Pushed the container image to `Amazon ECR`[cite: 2].
* Configured an EC2 `Auto Scaling group` across private subnets `10.0.128.0/20` and `10.0.144.0/20` with an attached `IAM Role` (granting ECR pull and S3 access) and Security Group rules for `Port 22,80`[cite: 2].
* Placed an Application Load Balancer (`ALB`) in front of the `Auto Scaling group` for HTTP traffic distribution, a `Bastion Host` (`Port 22`) in `10.0.0.0/20` for SSH management, and Amazon `SNS` notifications to send `Email` alerts on scaling events[cite: 2].

### 3. Multi-AZ Database Layer
* Deployed `Amazon RDS` in private database subnets with a primary (`Main`) database in `10.0.48.0/20` and synchronous replication (`Sync`) to a standby (`FailOver`) instance in `10.0.64.0/20`[cite: 2].

### 4. Serverless S3 & Lambda Image Filtering Pipeline
* **Private Upload:** Users upload raw images through the Flask `Web Server`, which writes objects to the source `S3 Bucket` via the `GW Endpoint`[cite: 2, 3].
* **Automated Image Filter:** Uploading an image triggers an AWS `Lambda` function that applies an image `Filter` to the file[cite: 2].
* **Processed Storage:** The `Lambda` function saves the filtered output image into a second destination `S3 Bucket`[cite: 2].
