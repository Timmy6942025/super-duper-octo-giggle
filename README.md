# Quick Start

1. **Clone the repo:**
```bash
git clone https://github.com/Timmy6942025/super-duper-octo-giggle.git
cd super-duper-octo-giggle
```
2. **Install required packages:**
```bash
pip install -r requirements.txt
```
3. **Run the app:**
```bash
python main.py
```
4. **Click the link that appears in the terminal and start chatting.**  
5. **Press `Ctrl + C` in the terminal to stop the app.**

---

## Want a Different Embedding Model?

The app works out of the box, but if you want to use another embedding model (e.g., `all-MiniLM-L6-v2`), do this **once**:

1. Open the `faiss_index` folder.  
   You’ll see files like:
   - `index.faiss` and `index.pkl` (full index files from the default model)  
   - `index.faiss(1)` and `index.pkl(1)` (empty files ready for a new index)

2. To rebuild the index with your new embedding model:  
   - Rename the full files (without `(1)`) by adding `(1)` at the end  
   - Rename the empty files (with `(1)`) to remove the `(1)`

3. Using a code editor like **VS Code**, open both `ingest.py` and `main.py` and find the line with the embedding model name:  
   ```python
   "BAAI/bge-m3"
   ```  
   Change it to your preferred embedding model name (same in both files).

4. Run:  
```bash
python ingest.py
```
(*Takes ~2–20 minutes depending on the embedding model*)

5. Then start the app:  
```bash
python main.py
```

That’s it — your new model is now active!

---

## Default Models

- **Embedding:** `BAAI/bge-m3`  
- **Executor (chat):** `Gemini-2.5-flash`
