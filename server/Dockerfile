FROM python:3.11.9-bookworm as prod

RUN pip install poetry==1.8.3

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY server/pyproject.toml server/poetry.lock server/app/src/ 
WORKDIR /server/app/src

# Installing requirements
RUN poetry install --only main


# Copying actual application
COPY . server/app/src ./

# Install the Kaggle CLI
# RUN pip install kaggle torch transformers datasets tokenizers
RUN pip install sqlalchemy torch transformers tokenizers

# Download NLTK corpora (if needed, like 'punkt')
RUN python -m nltk.downloader punkt
RUN python -m nltk.downloader punkt_tab

# ADDED LATE TO REDUCE IMAGE SIZE... (will this work?)
RUN rm -rf /root/nltk_data/corpora 

# RUN python -m nltk.downloader averaged_perceptron_tagger
# RUN python -m nltk.downloader averaged_perceptron_tagger_eng

# # Create the .kaggle directory in the root's home directory
# RUN mkdir -p /root/.kaggle

# # Copy the kaggle.json file to the .kaggle directory
# COPY kaggle.json /root/.kaggle/kaggle.json

# # Set permissions to secure the API key file
# RUN chmod 600 /root/.kaggle/kaggle.json

ENV PYTHONPATH "${PYTHONPATH}:/server/app/src"

CMD [ "uvicorn", "server.app.src.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug", "--timeout-keep-alive", "1200000"]
# CMD ["fastapi", "run", "app/src/main.py", "--port", "80"]

FROM prod as dev

RUN poetry install

# Install Playwright and system dependencies required by Playwright
RUN poetry run playwright install-deps

# Install Playwright browsers
RUN poetry run playwright install
