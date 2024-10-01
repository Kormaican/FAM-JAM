# rag-tutorial-v2 - modified for use with Fam-JAM

Here is the link to the original youtube tutorial, in order to debug any issues you run into:
https://youtu.be/tcqEUSNCn8I?si=61A9dtNWdgPZ0SKX

Run `python populate_database.py` to add files to the chroma databse (you can use -r to reset the chroma database)
Then run the test-case`test_extraction_for_fam_jam()` in `test_rag.py` to see basic operation. (I was using PyCharm
community edition, it made this very simple.)

Be sure to download and install Ollama, as well as the Mistral model and the nomic-embed-text model.
