# WORK IN PROGRESS

Project to download youtube video and extract a PDF from images.
Optimized for static presentations and sheet music where the only thing on screen is the document/slides

# Basic features

- Simple frontend to paste a URL and download the resulting PDF
- Removes duplicate images and crops to remove black borders
- Prints to a single PDF file
  
# Planned features

- Select starting time (to remove intros)-> Implemented in backend but needs to be available from front
  - Ideally, after putting the URL in, it will preview the video and you can seek in the video itself to set the starting time
- Show a spinner while it's processing
- Start download immediately