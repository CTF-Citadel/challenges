# Redacted

> [!NOTE]
>
> The focus of this `Forensics` challenge is the analysis of a `.pdf` file and extraction of hidden data. 

## Challenge Development

> [!NOTE]
> 
> I wanted this challenge to be the entrypoint to forensics challenges meaning this should be the easiest one. 

Starting off I created the `docker-compose.yml` file which contains only 1 container. <br/>
```yml
version: '3.9'

services:
  web:
    build:
      context: .
      args:
        FLAG: ${FLAG}
    ports:
      - "80:5000"
```

Mapping the port `5000` which is used by `Flask` to the exposed port `80`, which can be used be the user. <br/>
The `Dockerfile` sets up a python container and installs its dependencies, the `flag` is also being imported in the `Dockerfile`. <br/>
```docker
FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ARG FLAG
ENV FLAG=${FLAG}

RUN python3 /app/generation.py

CMD ["python", "service.py"]
```

The `Python Flask` service just provides the file `leaked_pdf_00.pdf` which contains the hidden `flag`. <br/>
```py
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# Index page to provide files
@app.route('/')
def index():
    return render_template('index.html')

# endpoint to download pdf
@app.route('/download_pdf')
def download_encryption_py():
    return send_from_directory('.', 'leaked_pdf_00.pdf', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
```

The generation of the `.pdf` file occurs within `generation.py`. <br/>
```py
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw

# Get flag from envvar
flag = f'TH{{{os.getenv("FLAG")}}}'

# create an image
out = Image.new('RGB', (240, 30), (255, 255, 255))
d = ImageDraw.Draw(out)

# draw multiline text
d.multiline_text((10, 10), flag, fill=(0, 0, 0))
out.save('goldnugget.png')


# Function to generate PDF with hidden flag
def generate_pdf():
    # Create a canvas object
    c = canvas.Canvas('leaked_pdf_00.pdf', pagesize=A4)

    c.setPageCompression(0)
    c.setPageDuration(0)

    # Fake Chat between 2 People
    c.drawString(50, 800, 'Agent_Bob:   It has come to my attention that we may have a mole in our company.')
    c.drawString(50, 760, 'Agent_Alice: Is there any evidence for your superstition?')
    c.drawString(50, 720, 'Agent_Bob:   Apparently somebody leaked the flag: ')
    c.drawString(50, 680, 'Agent_Alice: It would be pretty serious if someone leaked confidential documents.')
    c.drawString(50, 640, 'Agent_Bob:   No shit!')
    c.drawString(50, 600, 'Agent_Alice: Do you have any suspects in mind?')
    c.drawString(50, 560, 'Agent_Bob:   I did think that 2 employees were acting really suspicious today.')
    c.drawString(50, 520, 'Agent_Alice: I think you should report it to the higher-ups.')
    c.drawString(50, 480, "Agent_Bob:   I'm afraid I will be framed as a scapegoat.")
    c.drawString(50, 440, "Agent_Alice: That's a risk you have to take. If you delay it further the punishment will be worse.")
    c.drawString(50, 400, "Agent_Bob:   I guess you're right, I will commence an emergency meeting now.")

    # draw image into pdf
    c.drawImage('./goldnugget.png', 330, 710, width=240, height=30)

    # Draw a black rectangle over flag to black it out
    c.setFillColorRGB(0, 0, 0)
    c.rect(330, 715, 240, 20, fill=True, stroke=False)

    # Save the canvas to a PDF file
    c.save()

generate_pdf()
```

I used the library `reportlab` to generate the PLF with the content and the redacted flag. <br/> 
I used the library `pillow` to generate an image with the `flag` string inside. <br/>

> [!NOTE]
> Why did I generate an image containing the flag? <br/>
> I was running into issues when trying to redact the flag as text inside the `.pdf` file because it was still a selectable item. <br/>
> This meant that anyone could just use `strg+a` to select the flag although there was a black rectangle layered above the `flag` string. <br/>
> To solve this I generated an image with the `flag` and layered a black rectangle above it. <br/>

I additionally added a fake chat log with 2 agents to get some storyline for the challenge. <br/>
Creating the `.pdf` file concludes this documentation.