
# 🚀 Azure Cost Optimizer

## 🧩 Overview
chatgpt prompt link : "https://chatgpt.com/share/6891154a-b898-8011-a226-a419e0ba43b1"

**Azure Cost Optimizer** is a practical solution for managing data growth and optimizing cloud expenditure. This project introduces a streamlined archival pipeline for Azure Cosmos DB that automatically migrates stale records (e.g., older than 90 days) to Azure Blob Storage. The retrieval layer ensures seamless access to both active and archived records, offering a cost-effective and performant data architecture.

## 🗂️ Project Structure

```
azure-cost-optimizer/
├── archive_pipeline/
│   ├── archive.py              # Azure Function: orchestrates archival logic
│   ├── archive_logic.py        # Core logic for querying, archiving, and deleting old records
├── retrieval_layer/
│   ├── retrieve.py             # REST API to fetch records from Cosmos DB or blob archive
│   ├── helper.py               # Utility for deserializing and querying blobs
├── utils/
│   ├── config.py               # Loads environment configs from .env
├── tests/                      # Unit tests for archiving and retrieval
├── docs/                       # Documentation (architecture, setup, cost analysis)
├── requirements.txt            # Project dependencies
├── .env                        # Environment variables (not committed)
└── README.md                   # Project documentation
```

## ⚙️ How to Run

> Ensure [Azurite](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azurite) is running locally if testing with local emulators.

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd azure-cost-optimizer
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**

   * Copy `.env.example` (if available) to `.env`
   * Set your values for:

     ```env
     COSMOS_URI=
     COSMOS_KEY=
     COSMOS_DB_NAME=
     COSMOS_CONTAINER_NAME=
     AZURE_STORAGE_CONNECTION_STRING=
     BLOB_CONTAINER_NAME=
     ```

4. **Run archiving logic (standalone or as Azure Function)**

   ```bash
   python archive_pipeline/archive.py
   ```

5. **Run retrieval layer (Azure Function host or test directly)**

   ```bash
   func start --verbose
   ```

6. **Test endpoint**
   Visit:

   ```
   http://localhost:7071/api/retrieval_layer
   ```

## 🧠 Design Decisions

* **Hybrid storage**: Active data remains in Cosmos DB; cold data is archived to Blob Storage.
* **Cost-driven**: Archival of stale records helps reduce RU charges and overall Azure costs.
* **Seamless retrieval**: Retrieval API checks Cosmos DB first, falls back to blobs if data is archived.
* **Local dev support**: Emulates services with [Azurite](https://github.com/Azure/Azurite) for offline testing.
* **Fail-safe deletion**: Skips deletion of records that lack a valid partition key (`userId`) with warning logs.
* **Defensive storage handling**: Blob container creation is exception-safe for robustness.

## 🧪 Testing

* Unit tests are available in the `/tests` directory.
* Use `pytest` to run:

  ```bash
  pytest tests/
  ```

## 🌱 Future Enhancements

* ✅ Add retention policies or configuration-based archival rules (e.g., by type, usage).
* 🔍 Add monitoring and logging dashboards for archival metrics and blob usage.
* 🧾 Enable query capabilities over blob data using Azure Data Lake or Synapse.
* 🔒 Implement RBAC/Access tokens for secure blob access.
* 📚 Extend docs with setup scripts, example queries, and performance benchmarks.


