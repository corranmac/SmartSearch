from transformers import pipeline
import torch


# Init is ran on server startup
# Load your model to GPU as a global variable here using the variable name "model"


def init():
    import pandas as pd 
    import requests, io
    device = 0 if torch.cuda.is_available() else -1
    %cd vila/examples/end2end-sci-pdf-parsing
    os.system("docker build -t vila-service .")
    os.system("docker run -p 8080:8080 -ti vila-service")

# Inference is ran for every server call
# Reference your preloaded global model variable here.
def inference(inputs:dict) -> dict:
    path = inputs.get("type",None)
    pdfType= inputs.get("pdf",None)
    if path == None:
        return {'message': "No pdf path provided"}

    if pdfType == "bytes":
        try: 
            files = {"pdf_file": ("pdf.pdf", path, "multipart/form-data")}
            r = requests.post('http://localhost:8080/parse', files=files)
            parsed = pd.read_csv(io.StringIO(r.content.decode('utf-8')))
        except:
            return {'message': "Invalid pdf bytes"}
    elif pdfType =="url":
        try:
            relative_coordinates = True # whether returning relative coordinates or not 
            parsed = pd.read_csv(f"http://127.0.0.1:8080/parse/?pdf_url={path}&relative_coordinates={relative_coordinates}")
        except:
            return {'message': "Invalid url or pdf at url"}
    else:
      return {'message': "Invalid pdf"}
    result= {'pd_df":parsed}
    # Return the results as a dictionary
    return result
