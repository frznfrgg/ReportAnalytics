# Project Setup Instructions

Follow the steps below to run the project locally:

1. **Create a Python or Conda environment**  
   You can create the environment from either `environment.yml` or `requirements.txt`.

   Using Conda:
   ```bash
   conda env create -f environment.yml
   conda activate skolkovo
   ```

   Using pip:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate    # On Windows
   pip install -r requirements.txt
   ```

2. **Navigate to the project's root folder**
   ```bash
   cd path/to/project
   ```

3. **Run the Streamlit app**
   ```bash
   PYTHONPATH=src streamlit run src/app/emba_exit_dashboard.py
   ```

4. **Access the website**  
   The website will be available at the address stated in the terminal (usually http://localhost:8501).

5. **Additional information about deployment**  
   For more details, visit the [Streamlit deployment documentation](https://docs.streamlit.io/deploy).
