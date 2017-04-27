import os
import json
from flask import Flask
from flask import Response
from subprocess import call

app = Flask(__name__)

@app.route('/')
def hello():
    call(["./ringlwe/rlwe_512_25601_gaussian"])
    infile = "output_file.txt"

    f  = open(infile, "r")
    full_text = f.read()
    
    poly_names = ["a", "public_alice", "bob_encapsulation", "cr_v", "mu_alice", "mu_bob"]
    full_data = {}
    
    for name in poly_names:
        full_data[name] = get_poly_data(name, full_text)
    
    json_data = json.dumps(full_data)
    return Response(json_data, mimetype='text/json')

def get_poly_data(name, full_text):
    # Takes name of the polynomial you want and the full text of the program
    # output, then return a dictionary of all the coefficients 
    start = full_text.find("<--START " + name.upper() + "-->") + 12 + len(name)
    end = full_text.find("<--END " + name.upper() + "-->") - 1
    element_list = full_text[start:end].split(" ")
    data = []

    for element in element_list:
        data.append(element)
    return data

app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))