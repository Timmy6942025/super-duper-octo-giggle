1. In the terminal, run:
   python ingest.py
This will create the vector store. It will usually take 2-5 minutes, and you only have to do it once unless you end/stop the codespace
      if you get:

    Traceback (most recent call last):
  File "/home/user/super-duper-octo-giggle/ingest.py", line 3, in <module>
    from langchain.document_loaders import PyMuPDFLoader
ModuleNotFoundError: No module named 'langchain'

in your terminal, run:
   pip install langchain

3. Once it finishes, also in the terminal, run:
   python main.py
4. Open whatever development link it gives you and use the app.

ctrl+c in terminal to stop the app

models: 

-embeddings model: all-MiniLM-L6-v2

-executer model: Gemini-2.5-flash-preview-05-20
