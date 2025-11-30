# Visual Inventory Manager

A robust, AI-powered application that transforms images of receipts or shelves into structured inventory data. Built with **FastAPI**, **React**, and **OpenAI GPT-4o**.

## 🚀 Features

- **AI Vision Pipeline**: Uses Multimodal LLMs (GPT-4o) to identify items, quantities, and prices from images.
- **Strict Validation**: Enforces structured data output using **Pydantic** models to ensure database consistency.
- **Robust Error Handling**:
  - **Blur Detection**: Automatically rejects low-quality images before processing.
  - **Retry Logic**: Handles API rate limits and transient network failures with exponential backoff.
  - **Confidence Checks**: Flags low-confidence extractions for human review.
- **Modern UI**: A clean, dark-themed React interface with drag-and-drop upload and real-time feedback.
- **Cloud Database**: Seamlessly integrated with **Supabase (PostgreSQL)** via the `supabase-py` client for reliable data persistence.

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Supabase Client, Pydantic, OpenCV (for image analysis).
- **AI/ML**: OpenAI API (GPT-4o Vision).
- **Frontend**: React, Vite, Axios, Lucide React (Icons).
- **Database**: Supabase (PostgreSQL).

## 📂 Project Structure

```
Visual Inventory/
├── backend/                # Python FastAPI Backend
│   ├── main.py             # API Entry Point
│   ├── vision_pipeline.py  # Core AI Logic & Error Handling
│   ├── models.py           # Pydantic Data Schemas
│   ├── database.py         # Supabase Connection
│   ├── schema.sql          # PostgreSQL Schema
│   └── requirements.txt    # Python Dependencies
│
└── frontend/               # React Frontend
    ├── src/
    │   ├── App.jsx         # Main UI Component
    │   └── App.css         # Styling
    └── package.json        # JS Dependencies
```

## ⚡ Getting Started

### Prerequisites

- **Python 3.8+**
- **Node.js & npm**
- **OpenAI API Key**
- **Supabase Project**

### 1. Backend Setup

1.  Navigate to the backend directory:

    ```bash
    cd backend
    ```

2.  Create and activate a virtual environment (Recommended):

    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  Install dependencies:

    ```bash
    pip install -r requirements.txt
    pip install supabase # Ensure supabase client is installed
    ```

4.  Configure Environment Variables:

    - Create a `.env` file in the `backend` folder.
    - Add your keys:
      ```env
      OPENAI_API_KEY=your_sk_key_here
      SUPABASE_URL=https://your-project-ref.supabase.co
      SUPABASE_KEY=your_anon_key
      ```

5.  Run the Server:
    - **Easy Mode**: Double-click `run.bat`.
    - **Manual**: `uvicorn main:app --reload`

### 2. Frontend Setup

1.  Navigate to the frontend directory:

    ```bash
    cd frontend
    ```

2.  Install dependencies:

    ```bash
    npm install
    ```

3.  Run the Development Server:

    - **Easy Mode**: Double-click `run.bat`.
    - **Manual**: `npm run dev`

4.  Open your browser at `http://localhost:5173`.

## 🛡️ Security & Robustness

- **Prompt Injection Mitigation**: The system uses strict schema enforcement and logic validation (e.g., checking if `unit_price * quantity ≈ total_price`) to prevent malicious data entry.
- **Sanitization**: Inputs are validated against strict types before ever reaching the database.
- **Row Level Security (RLS)**: Database policies are configured to control access to data.

## 📝 License

This project is open-source and available under the MIT License.
