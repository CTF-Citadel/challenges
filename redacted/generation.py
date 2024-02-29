import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image, ImageDraw

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
