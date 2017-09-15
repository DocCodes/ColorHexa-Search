import sublime, sublime_plugin
import re
from sys import platform
from os import startfile
from subprocess import Popen

__version__ = "1.0.0"

zeroPad = lambda txt: txt[::-1]+"0"*(2-len(txt))
def getFmt(txt):
   """Determines the format of the color
   
   Arguments:
      txt {str} -- The text to determine
   """
   fmt = {}
   fmt["isHex"] = re.match("#?[0-f]{3,6}", txt) != None
   if(fmt["isHex"]): fmt["isHexMN"] = re.match("#?[0-f]{6}", txt) == None
   fmt["isRGB"] = re.match("rgb\([0-9]{1,3},\s?[0-9]{1,3},\s?[0-9]{1,3}\)", txt) != None
   fmt["isRGBA"] = re.match("rgba\([0-9]{1,3},\s?[0-9]{1,3},\s?[0-9]{1,3},\s?[.-9]*\)", txt) != None
   return fmt

def toHex(txt, fmt):
   """Converts the color to hex format
   
   [description]
   
   Arguments:
      txt {str} -- The raw color's text
      fmt {dict} -- The format of the color
   
   Returns:
      str -- The hex converted color
   """
   col = ""
   if(fmt["isHex"]):
      col = txt.replace("#", "")
      if(fmt["isHexMN"]): return "".join([s*2 for s in col])
      return col
   if(fmt["isRGB"] or fmt["isRGBA"]):
      rgb = re.sub("[^,0-9]", "", txt).split(",")
      rgb = [int(s) for s in rgb[:3]]

      for seg in rgb:
         h = str(hex(seg))[2:]
         col += zeroPad(h)
      
      return col

def openSite(url):
   """Opens the specified url

   Arguments:
      url {str} -- The URL of the webpage
   """
   if(platform == "win32"):
      startfile(url)

class ColorHexaSearch(sublime_plugin.TextCommand):
   def run(self, edit):
      """Main code
      """
      sel = self.view.sel()[0]
      txt = self.view.substr(sel).lower()

      fmt = getFmt(txt)
      col = toHex(txt, fmt)
      url = "http://www.colorhexa.com/{}".format(col)
      openSite(url)