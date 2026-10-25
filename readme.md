Transport Legacy-to-AI System
An AI-assisted interface for working with legacy transport data. The project combines a Streamlit application, language-model orchestration, semantic retrieval, and SQL database access to help users interact with existing data through a more accessible workflow.
Project status: Development / proof of concept. Configuration and run commands may need to be adapted to your local environment.

Overview
Legacy business systems often store useful operational information in relational databases and documents that are difficult to explore without knowing the schema, SQL, or where relevant information lives. This project brings AI-based retrieval and database tools together in a Python application.

The repository's dependencies indicate the use of Streamlit, LangChain/LangGraph, OpenAI-compatible model APIs, Pinecone, Hugging Face sentence-transformer embeddings, and SQLAlchemy/pyodbc for database connectivity.
Key capabilities
- AI application interface: Streamlit-based application layer.
- LLM orchestration: LangChain and LangGraph components for building tool-enabled workflows.
- Semantic retrieval: Embedding-based retrieval using sentence-transformers and vector-search tooling.
- Vector database integration: Pinecone support for managed vector search.
- Relational database connectivity: SQLAlchemy and pyodbc for connecting to supported SQL databases, including SQL Server when correctly configured.
- Structured data handling: Pandas and OpenPyXL for working with tabular data and Excel files.
The exact features available at runtime depend on the modules configured in src/ and the services enabled in your environment.
Technology stack
Area	Technologies
Language	Python 3.12.13 (version specified in requirements.txt)
User interface	Streamlit
AI orchestration	LangChain, LangGraph
Model API	OpenAI Python SDK
Embeddings	Hugging Face sentence-transformers
Vector search	Pinecone; FAISS CPU is also listed as a dependency
Database access	SQLAlchemy, pyodbc
Data processing	Pandas, OpenPyXL
Configuration	python-dotenv, pydantic-settings


Repository structure
Transport-legacy-to-AI_system/
├── data/             # Project data and supporting files
├── scripts/          # Utility and setup scripts
├── src/              # Application and AI/database modules
├── .gitignore
├── requirements.txt  # Python dependencies
└── README.md
Getting started
1. Prerequisites
- Python 3.12.x is recommended because requirements.txt specifies Python 3.12.13.
- Git
- Access credentials for whichever model API, vector database, and SQL database you configure.
- For SQL Server connections, an appropriate Microsoft ODBC driver installed on your operating system.
2. Clone the repository
git clone https://github.com/shitijrajpoot12-cyber/Transport-legacy-to-AI_system.git
cd Transport-legacy-to-AI_system
3. Create and activate a virtual environment
macOS / Linux:
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
Windows PowerShell:
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
4. Install dependencies
python -m pip install -r requirements.txt
If installation fails for a package with native components, check that your Python version and platform are supported by the pinned package version before changing dependency versions.
5. Configure environment variables
Create a .env file in the repository root. Add only the credentials and settings required by the modules you intend to run. Variable names below are examples; match them to the names actually read by your code.
# Model API
OPENAI_API_KEY=your_model_api_key

# Pinecone (if using Pinecone retrieval)
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=your_index_name

# SQL Server (example placeholders; adapt to your configuration)
DB_SERVER=your_server
DB_NAME=your_database
DB_USERNAME=your_read_only_username
DB_PASSWORD=your_database_password
Security notes
- Never commit .env, API keys, database passwords, access tokens, or real customer data.
- Keep .env in .gitignore.
- Use least-privilege, preferably read-only, database credentials for exploratory AI workflows.
- If a secret has been committed or shared accidentally, rotate it and remove it from the repository history where appropriate.
- Do not paste secrets into issue reports or logs.
6. Launch the application
The repository contains a src/ directory, but the correct Streamlit entry-point filename should be confirmed from the files in that directory. From the repository root, run the actual application file, for example:
python -m streamlit run src/<your_streamlit_entrypoint>.py
Replace <your_streamlit_entrypoint>.py with the real filename. Do not assume the entry point is src/app.py unless that file exists.

If you are unsure which file starts the UI, search for Streamlit imports:
grep -R -n "import streamlit\|from streamlit" src
Run an individual module directly only if it is intended to be executable. For example, a tool-definition module may initialise database connections or require environment variables when executed.
Troubleshooting
ModuleNotFoundError
Install dependencies with the same Python interpreter used to run the app:
python -m pip install -r requirements.txt
python -m pip show streamlit torch torchvision transformers
Check which interpreter and Streamlit executable are being used:
which python
python --version
which streamlit
python -m streamlit --version
Using python -m streamlit helps ensure Streamlit runs from the active Python environment. Avoid mixing packages installed into Conda, system Python, and a virtual environment.
SQL Server connection errors
- Verify the server, database, username, and password.
- Confirm that the relevant ODBC driver is installed.
- Check whether the server requires encryption and certificate validation.
- Confirm that the database account has the required permissions.
- Avoid embedding credentials directly in Python source code.
Pinecone or model API configuration errors
- Confirm that the required environment variables are present in the process running the application.
- Ensure .env is loaded from the repository root when the code expects it there.
- Verify that the configured index exists and is compatible with the embedding model and vector dimensions.
- Never print or share the full values of API keys.
Development notes
- Keep database access, retrieval logic, and UI code separated where practical.
- Validate AI-generated SQL or database actions before execution; prefer read-only credentials unless writes are explicitly required.
- Treat retrieved documents and database values as untrusted input.
- Add tests for database tools, retrieval behaviour, and error handling as the project evolves.
Contributing
1. Fork the repository.
2. Create a focused feature branch.
3. Make changes and test them in your own configured environment.
4. Open a pull request describing the change, test results, and any configuration updates.
Do not include secrets, production data, or private connection details in contributions.
 
Author
Shitij Chauhan