# Amazon Scraper 

This is a fullstack web application with a **FastAPI** backend and a **React** frontend.

---

## ⚙️ Setup Instructions

### 🐍 Backend (FastAPI)

1. **Navigate to the backend directory:**

    ```bash
    cd backend
    ```

2. **Create a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the FastAPI server:**

    ```bash
    uvicorn main:app --reload
    ```

    > Make sure your `main.py` is the entry file and contains the FastAPI app instance as `app`.

5. **API should now be running at:**

    ```
    http://localhost:8000
    ```

---

### ⚛️ Frontend (React)

1. **Navigate to the frontend directory:**

    ```bash
    cd frontend
    ```

2. **Install dependencies:**

    ```bash
    npm install
    ```

3. **Start the React development server:**

    ```bash
    npm run dev
    ```

4. **The frontend should now be running at:**

    ```
    http://localhost:5173
    ```

---
### API Keys required 

1. **An env.example file is present in backend**

    ```bash
    cd backend
    ```
2. **Generate API Key from AI Studio by Google**
3. **Add API Key for Gemini from Google AI Sudio (Free)**

---
## 📝 Notes

* Assumption: Ports 3000 (React) and 8000 (FastAPI) are not in use.
