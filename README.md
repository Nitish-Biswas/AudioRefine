# Transcription


## Prerequisites

- Python 3.8+
- ffmpeg
  ```sh
  brew install ffmpeg
  ```


## Project and environment setup
  
 1. **Clone the repository:**

    ```sh
    git clone https://github.com/Nitish-Biswas/Transcription.git
    cd Dish-Management
    ```
2. **Create a virtual environment and activate it:**

    ```sh
    python3 -m venv venv
    ```
    
   ***On macOS***
   ```sh
   source venv/bin/activate
   ```
   
   ***On Windows***
   ```sh
   venv\Scripts\activate
   ```


3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```


4. **Set the Google Cloud credentials:**

   ****Each time you activate your virtual environment, you must set the GOOGLE_APPLICATION_CREDENTIALS environment variable. This can be done by running the following command:****

   ```sh
    export GOOGLE_APPLICATION_CREDENTIALS="\path\to\your\json\file.json "
    ```

## Run the APP:

   ```sh
    streamlit run app.py
   ```




