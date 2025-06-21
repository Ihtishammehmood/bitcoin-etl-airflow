<h1 align="center">Bitcoin ETL with Apache Airflow</h1>

![image](https://github.com/user-attachments/assets/6fae6071-6b66-4497-b621-fe2093757685)

# [Watch full youtube video here](https://youtu.be/gXs-BHNJlIQ)






## Overview

This is a comprehensive **ETL (Extract, Transform, Load) Pipeline** project designed for cryptocurrency data processing. The project combines multiple technologies including **Apache Airflow**, **PostgreSQL**, **Docker**, and **Python** to create a robust data pipeline for financial market analysis.

## 🏗️ Architecture

The project follows a modern data engineering architecture with the following components:

- **Data Sources**: Alpha Vantage API
- **Orchestration**: Apache Airflow for workflow management
- **Database**: PostgreSQL for data storage
- **Containerization**: Docker for deployment
- **Processing**: Python with pandas and technical analysis libraries


## 🚀 Features

### Data Extraction
- **Alpha Vantage API Integration**: Fetches real-time and historical 

### Data Transformation
- **Technical Indicators**: Comprehensive technical analysis using pandas-ta
  - Simple Moving Average (SMA)
  - Exponential Moving Average (EMA)
  - Relative Strength Index (RSI)
  - MACD (Moving Average Convergence Divergence)
  

### Data Loading
- **PostgreSQL Integration**: Efficient data storage with proper indexing

### Workflow Orchestration
- **Apache Airflow**: Professional-grade workflow management
- **Scheduled Execution**: Daily data pipeline execution
- **Task Dependencies**: Proper task ordering and dependency management

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Orchestration** | Apache Airflow  | Workflow management and scheduling |
| **Database** | PostgreSQL  | Data storage and querying |
| **Containerization** | Docker & Docker Compose | Application deployment |
| **Data Processing** | Python 3.13 | Core processing logic |
| **Technical Analysis** | pandas-ta | Financial indicators calculation |
| **Data Manipulation** | pandas | Data transformation and analysis |
| **Environment Management** | UV package manager | Dependency management |


### API Key
- **Alpha Vantage API Key**: Free registration at [alphavantage.co](https://www.alphavantage.co/support/#api-key)
  - Free tier: 5 requests/minute, 500 requests/day
  - place the api key into airlfow UI variables section as `alpha_vantage_api_key` along with actual `api key`

## 🔧 Installation & Setup

### 1. Environment Setup

```bash
# Clone the repository
git clone (https://github.com/Ihtishammehmood/bitcoin-etl-airflow.git)
# Install UV package manager
pip install uv

# Create and activate virtual environment
uv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install project dependencies
uv sync
```

### 2. Astro CLI Configuration

```bash
winget install -e --id Astronomer.Astro # This will install the astro CLI

astro dev start # this command will run the docker
astro dev restart # This command stops and restart the project

```

