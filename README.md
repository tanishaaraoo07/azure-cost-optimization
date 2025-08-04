# Azure Cost Optimizer

## Overview
The Azure Cost Optimizer project aims to enhance the efficiency of data storage and retrieval processes by implementing an archiving solution. This project focuses on reducing costs associated with data storage in Azure by archiving old records and providing a seamless retrieval mechanism for both active and archived data.

## Project Structure
- **archive_pipeline/archive.py**: Contains the script responsible for archiving old records.
- **retrieval_layer/retrieve.py**: Implements logic to fetch data from either a Cosmos database or archived records.
- **utils/config.py**: Defines environment variables and constants used throughout the project.
- **docs/**: Contains documentation files, including architecture diagrams and cost comparisons.
- **tests/**: Includes unit tests for both archiving and retrieval functionalities.
- **requirements.txt**: Lists the dependencies required for the project.
- **.env**: Stores environment variables securely.

## How to Run
1. Clone the repository:
   ```
   git clone <repository-url>
   cd azure-cost-optimizer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in the `.env` file.

4. Run the archiving script:
   ```
   python archive_pipeline/archive.py
   ```

5. To retrieve data, execute:
   ```
   python retrieval_layer/retrieve.py
   ```

## Design Decisions
- The decision to archive old records was made to optimize storage costs and improve data retrieval times.
- The architecture was designed to ensure that both active and archived data can be accessed efficiently without compromising performance.
- Unit tests were implemented to validate the functionality of both the archiving and retrieval processes, ensuring reliability and maintainability.

## Future Work
- Enhance the archiving logic to include more sophisticated criteria for identifying records to archive.
- Implement additional metrics to monitor the cost savings achieved through the archiving process.
- Expand the documentation to include more detailed usage examples and best practices.