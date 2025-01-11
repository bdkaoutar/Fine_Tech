# FinTech Crypto Application

## Overview
The *FinTech Crypto Application* is a scalable, secure platform designed to revolutionize financial transactions by integrating blockchain, data analytics, and a microservices architecture. This project uses cutting-edge technologies to deliver seamless cryptocurrency transactions, smart contract functionalities, and financial data insights.


## Features
- **Microservices Architecture**: Modular design for scalability and maintainability.
- **Blockchain Integration**: Secure financial transactions via Ethereum.
- **Data Analytics**: Insights into market trends and user behaviors.
- **FastAPI Framework**: High-performance APIs for backend services.
- **Frontend (SPA)**: Responsive Angular interface for users.
- **DevOps**: Automated deployment with Docker, Kubernetes, and Jenkins.
- **Cloud Deployment**: Scalable and accessible infrastructure using AWS services.


---

## Architecture
### Technologies Used:
- **Frontend**: Angular (SPA)
- **Backend**: FastAPI, SQLAlchemy
- **Blockchain**: Ethereum (Sepolia Testnet), Solidity, MetaMask, Web3.py
- **Database**: PostgreSQL
- **Data Analytics**: Pandas, NumPy, Plotly, Seaborn
- **DevOps**: Docker, Jenkins, Kubernetes, Terraform
- **Cloud**: AWS (EC2, RDS, S3, CloudWatch)

### Microservices:
1. **User Management Service**: 
   - Handles user accounts and wallets.
   - Manages authentication with JWT and OAuth2.
   - CRUD operations for users and wallets.
2. **Transaction Service**: 
   - Processes financial transactions.
   - Validates wallets and tracks transaction history.
3. **Blockchain Service**:
   - Executes smart contracts on Ethereum.
   - Integrates MetaMask for wallet authentication.
4. **Data Analytics Service**:
   - Processes transaction data for insights.
   - Generates dashboards and visualizations.


---

## Components

### User Management Microservice
#### Features:
- Secure user authentication and account management.
- Wallet creation and balance tracking.
- Role-based access control for admin functionalities.

#### Key Files:
1. **`database/main.py`**:
   - Initializes the database and manages session creation.
2. **`user/model.py`**:
   - Defines models for `User` and `Wallet`.
3. **`user/repository.py`**:
   - Encapsulates database operations for users and wallets.
4. **`user/services.py`**:
   - Implements business logic for user and wallet management.
5. **`user/routes.py`**:
   - Exposes RESTful endpoints for authentication, user, and wallet management.
6. **`utils/auth.py`**:
   - Provides JWT-based authentication and password hashing.
7. **`config.py`**:
   - Centralizes configuration using environment variables.

#### Endpoints:
- **`/register`**: User registration.
- **`/token`**: JWT token generation for authentication.
- **`/users/{username}/wallets`**: Wallet creation.
- **Admin Actions**:
  - Manage users: CRUD operations.
  - Disable or enable user accounts.


---

### Blockchain Integration
#### Smart Contract:
- **Language**: Solidity
- **Features**:
  - Payable contract for receiving Ether.
  - Withdraw function for transferring funds.
  - Balance retrieval.
- **Deployment**:
  - Ethereum Sepolia Testnet.
  - Verified on Etherscan.

#### Tools:
- MetaMask: Wallet and transaction management.
- Web3.py: Backend integration with Ethereum.
- Infura: Blockchain connectivity.


---

### Data Analytics
#### Financial Data Analysis:
- **Data Source**: CoinGecko API.
- **Libraries**: Pandas, NumPy, Plotly, Seaborn.
- **Visualizations**:
  - Candlestick charts.
  - Transaction volume graphs.
  - Closing price trends.
  - Log-transformed price graphs.


---

## DevOps Implementation
#### Docker:
- Containerized microservices for consistency.

#### Docker Compose:
- Orchestrated the deployment of frontend, backend, and database.

#### Jenkins CI/CD:
- Automated build, test, and deployment pipelines.

#### Kubernetes:
- Deployed Dockerized containers on AWS EKS.

#### Terraform:
- Infrastructure as code for scalable and consistent setups.


---

## Deployment
- **Frontend**: Accessible at `http://localhost`.
- **Backend**: Available at `http://localhost:8000/docs`.
- **Database**: Managed via PostgreSQL.

---

## Conclusion
The *FinTech Crypto Application* demonstrates the potential of integrating microservices, blockchain, and data analytics to address modern financial challenges. Its modular design ensures scalability, security, and ease of maintenance, providing a solid foundation for future enhancements.

---

## How to Run Locally
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd fintech-project
   ```
2. Set up the environment:
   - Create a `.env` file with:
     ```
     DATABASE_URL=<your_database_url>
     SECRET_KEY=<your_secret_key>
     ```
3. Start the services:
   ```bash
   docker-compose up --build
   ```
4. Access:
   - Frontend: `http://localhost`
   - Backend: `http://localhost:8000/docs`

---

## License
This project is licensed under the MIT License.
