# AI VKU Suport for Virtual assistant supports looking up academic information and enrollment information

This is a system that supports looking up information from the student handbook of VKU. Look up VKU admission plan.
### Live sever: https://aivkusupports.streamlit.app/T%C6%B0_v%E1%BA%A5n_VKU

## Step 1: Clone the Repository and Prepare Directories
Open the Command Prompt (CMD) and run the following command to clone the repository:
```bash
git clone https://github.com/RP502/AI_VKU_Support.git
```
## Step 2: Create venv python version 3.11
```bash
python -m venv .venv
```

## Step 3: Install Dependencies
Run the following command to install the necessary libraries:
```bash
pip install -r requirements.txt
```
## Step 4: Preprocess vector database
To preprocess the images for training, run the following command:
Create .env same to .example.env
```bash
python run data_processor.py
```
## Step 5: Change key gemini and qdrant
go to pages/1_💬_Tư vấn VKU.py change key gemini and qdrant
## Step 6: Run the Program
To start the AI_VKU_Support program, execute:
```bash
streamlit python run 🏠_Home.py
```
