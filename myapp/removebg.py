from rembg import remove
import easygui
from PIL import Image

inputp = easygui.fileopenbox()
out = easygui.filesavebox()

def removebg(inputpath, out):
    input = Image.open(inputpath)
    output = remove(input)
    output.save(out)

removebg(inputp, out)