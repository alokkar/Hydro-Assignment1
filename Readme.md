# Hydroninformatics - Assignment 1


## Requirements

### Python
- numpy
- pandas
- geopandas
- matplotlib
- descartes
- scipy 
- shapely

### Bash
- ffmpeg
- python3

## How to Run
- Make folders "images", "aridity" and "average" in current directory/folder.
- Add the data files to current folder.

### For q1:
- make sure you have "average" folder
- run `python3 q1.py`

### For q2:
- make sure you have "average" folder
- run `python3 q2.py`

### For q2 video:
- make sure you have "aridity" folder
- run `python3 q2_video.py` (will around 12-15 minutes)
- go to "aridity" forlder the run command
 `ffmpeg -f image2 -r 3 -i %d.png -vcodec mpeg4 -y aridity_movie.mp4`

### For q3:
- Make sure you have "images" folder
- run `python3 q3.py` (will take 10 minutes to finish)
- go to images folder then run command
 `ffmpeg -f image2 -r 3 -i %d.png -vcodec mpeg4 -y movie.mp4`
