#!/bin/bash

# Check if virtual environment is activated
if ! which virtualenv >/dev/null 2>&1; then
  echo "Virtual environment is not activated. Installing dependencies..."
  pip install -r requirements.txt
else
  echo "Try to activate virtual environment..."
  source streamlit_chatbot/bin/activate
  echo "Virtual environment is activated."
fi

# Check if dependencies are installed
if [ -f "requirements.txt" ]; then
  echo "Checking dependencies..."

  # Check for installed packages against requirements
  if ! pip freeze | grep -q "$(cat requirements.txt)"; then  
    echo "Some requirements seem missing. Installing..."
    pip install -r requirements.txt
  else
    echo "All requirements are satisfied. Running..."
  fi
fi

# Set the working directory (adjust if needed)
cd /home/hozaifa/Desktop/my_projects/streamlit

# Start the Streamlit app
streamlit run app.py
