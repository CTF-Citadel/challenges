# Layered

## Idea
>[!NOTE]
> When first creating the challenge, the idea was to hide the flag in the metadata of the last layer. However, I ran into the issue that when hiding something with, for example, steghide in one picture and then layering it, after exporting the layered images, the metadata was also readable from the combined images instead of only one of the images. So, I decided to instead hide a split-up QR code inside the layers.

So, first, I created a QR code using (https://www.the-qrcode-generator.com/), and then I simply took four differently sized screenshots of it to split it up:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/1cabea0f-f93a-4dfa-86c9-5be65e63d941)

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/254fc522-ea65-493c-85b3-e0b964fa69c3)

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/24d7339f-70ca-4259-a81f-ef4c2f20668a)

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/c5c0f006-c01c-4a08-9ddd-5e3d09746676)

Then, I needed to create portraits of people, so I simply used AI to do so (https://perchance.org/ai-photo-generator).

Now, I opened the first picture in GIMP. GIMP is an open-source image editing software that has the function to layer pictures. If you want to layer a picture, you can simply drag one picture on top of another, and then a layer gets created:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/b181ff49-d8ff-443c-859b-9c8e00153473)

So now we just need to add the QR code I split up. You can simply copy the screenshot inside, and a 'floating layer' gets created. After creating the 'floating layer,' you can move it to the position you want it to be and then merge it with the layer after adjusting the position and size:

![image](https://github.com/CTF-Citadel/challenges/assets/115781703/3facd78f-5fc3-4cf3-8530-8283b36f91fb)

You can use the arrow buttons to move it and the 'Anchor' button to merge it with another layer. After finishing the editing, you need to click on File > Save As and save it as a .xcf file.









