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
    def getColor(self, x):
        length = self.length()
        if length == 1:
            return self.palette[0]

        # h = float [0,1] position in palette
        x = max(0., min(x,1.))

        # don't need to interpolate edges
        if x == 1:
            return self.palette[length-1].rgb
        elif x == 0:
            return self.palette[0].rgb
        
        # scale x to palette length
        x = x*(length-1)

        i = int(x) # integer portion / index of left color
        t = (x%1) # decimal portion / lerp value
        
        return self.interpolate(self.palette[i], self.palette[i+1], t)

    
    # plist - list of hex strings 
    def setPalette(self, plist):
        self.palette = []
        for item in plist:
            self.palette.append(Color(item))
        #print("PALETTE RECEIVE")
        #for item in self.palette:
         #   print(item)
    
    def length(self):
        return len(self.palette)
            
        

    # HSL interpolation with two Color() objects
    # returns rgb color which is (t)% between the two
    def interpolate(self, color1, color2, t):
        h1,s1,l1 = color1.hsl
        h2,s2,l2 = color2.hsl
        
        # find shortest path between hues (using hue as circle)
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
                
        # interpolate saturation and lightness normally
        s = s1+((s2-s1)*t)
        l = l1+((l2-l1)*t)
        
        return Color(hsl=(h,s,l)).rgb
        
        
            
        
        
    
    
        
