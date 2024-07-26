FROM python:3.10.14-slim


LABEL maintainer="Nikos Episkopos <https://linkedin.com/in/nepiskopos/>"


# Set language
ENV LANG=C.UTF-8


# Set target CPU architecture
ARG TARGETARCH=amd64


# Create a directory for the app
RUN mkdir /root/app/
RUN mkdir -p /root/app/cache
RUN mkdir -p /root/app/nltk_data


# Copy the application directory and required files from host to container
ADD ./src/ /root/app/
ADD ./requirements.txt /root/app/


# Change working directory
WORKDIR /root/app/


# Set Python output direction for printing Python messages from the container
ENV PYTHONUNBUFFERED=1


# Add app directory to Python app
ENV PYTHONPATH="${PYTHONPATH}:/root/app/"


# Install required Python packages
RUN python3 -m pip install --no-cache-dir -r ./requirements.txt


# Download NLTK data
RUN python3 -m nltk.downloader -d ./nltk_data vader_lexicon words


# Download HuggingFace models
RUN python3 -c "from transformers import BertForMaskedLM; BertForMaskedLM.from_pretrained(pretrained_model_name_or_path='bert-base-uncased', cache_dir='./cache');"
RUN python3 -c "from transformers import BertTokenizer; BertTokenizer.from_pretrained(pretrained_model_name_or_path='bert-base-uncased', cache_dir='./cache');"


# Expose port 8000
EXPOSE 8000


# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
