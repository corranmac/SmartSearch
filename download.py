# In this file, we define download_model
# It runs during container build time to get model weights built into the container

# In this example: A Huggingface BERT model

from transformers import pipeline
import os

def build_docker():
    os.system("git clone https://github.com/allenai/vila.git")
    os.system("git clone https://github.com/allenai/vila.git")
    os.system("cd vila/examples/end2end-sci-pdf-parsing")
    os.system("docker build -t vila-service .")
    os.system("docker run -p 8080:8080 -ti vila-service")

if __name__ == "__main__":
    build_docker()
