from colour import Color
from scipy import interpolate

# Palette
# - stores current color palette
# - handles interpolation between palette indices
class Palette:
    
    def __init__(self, colors=["black"], lerp=True):
        self.setPalette(colors)
        self.lerp = lerp
    
    # Input: color index h (float) between 0,1
    # Output: rgb corresponding to palette[h]
    def getColor(self, h):
        # h = float [0,1] position in palette
        
        if h < 0:
            return self.palette
        if len(self.palette) == 1:
            return self.palette[0]
        h *= len(self.palette)-1
        t = (h%1)
        
        i = max(min(int(h), len(self.palette)-2),0)

        return self.interpolate(self.palette[i], self.palette[i+1], t)
    
    # plist - list of hex strings 
    def setPalette(self, plist):
        self.palette = []
        for item in plist:
            self.palette.append(Color(item))
        #print("PALETTE RECEIVE")
        #for item in self.palette:
         #   print(item)
            
        

    # HSL interpolation with two Color() objects
    # returns rgb color which is (t)% between the two
    def interpolate(self, color1, color2, t):
        h1,s1,l1 = color1.hsl
        h2,s2,l2 = color2.hsl
        
        # find shortest path between hues
        if h1 <= h2:
            distCW = h2-h1
            distCCW = 1-(distCW)
            if(distCW < distCCW):
                h = h1 + distCW*t
            else:
                h = h1 - distCCW*t
        else:
            distCW = h1-h2
            distCCW = 1-(distCW)
            if(distCW < distCCW):
                h = h1 - distCW*t
            else:
                h = h1 + distCCW*t
                
        # interpolate saturation and lightness
        s = s1+((s2-s1)*t)
        l = l1+((l2-l1)*t)
        
        return Color(hsl=(h,s,l)).rgb
        
        
            
        
        
    
    
        
