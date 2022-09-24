
from screen import Screen
from palette import Palette
from analyzer import Analyzer
from smoothList import SmoothList
import time

screen = Screen()
analyzer = Analyzer(numBarkBands=27)
# palette = Palette(['red', 'orange', 'green', 'blue', 'red'])
palette = Palette(['#ff3b3b', '#fc6d00', '#fcce00', '#a8fc00', '#19fc00', '#00fcdb', '#008ffc', '#0004fc', '#7a00fc', '#bd00fc', '#fc00c2', '#b50024'])
pitch = 0
onset = 0
maxOnset = 1
bark = []
maxBark = []


maxLoud = 1
loudRatio = 1

mfccLen = 40
mfccBands = SmoothList(length=mfccLen, ceilDecay=0.9999, meanFrames=2)
mfccColors = []
for i in range(mfccLen):
    mfccColors.append(palette.getColor(float(i)/mfccLen))

pitchLen = 12
pitchColors = []
for i in range(12):
    pitchColors.append(palette.getColor(float(i)/12.0))

pitches = []
maxPitches = []
for i in range(12):
    maxPitches.append(1)
    pitches.append(0)

for i in range(27):
    bark.append(0)
    maxBark.append(0)



def pitchBars(ctx):
    global pitches, loudRatio
    i = 0
    for h in pitches:
        if h > 0.5:
            r,g,b = pitchColors[i]
            br = h*loudRatio
            width = (h)*7
            margin = (7-width)/2
            ctx.set_source_rgba(r,g,b,br)
            # ctx.rectangle(0+px, scaleIdx, 1, 1)
            ctx.rectangle(5+margin, i, width, .5)

            # ctx.rectangle(12+px, scaleIdx, 1, 1)
            # ctx.rectangle(12, pitch, 5, 2)

            # ctx.rectangle(17+px, scaleIdx, 1, 1)
            ctx.rectangle(22+margin, i, width, .5)

            # ctx.rectangle(29+px, scaleIdx, 1, 1)
            # ctx.rectangle(29, pitch, 5, 1.5)
            ctx.fill()
        i += 1





def main():
    global maxOnset
    prevTime = time.time()
    framecount = 0
    prevFramecount=0
    hfcMean = 100
    while(True):
        hpcp = analyzer.get('hpcp')
        updatePitch(hpcp)
        updateLoud(analyzer.get('loudness'))

        ctx = screen.getCtx()

        # bassBar(ctx, mfccBands)
        pitchBars(ctx)

        # hfc =max(rhfc-prevHfc, 0)
        # prevHfc =rhfc

        # if hfc > hfcMax:
        #     hfcMax = hfc
        # hfcMean = ((70*hfcMean)+(10*hfcMax)+(20*hfc))/100.0



        # spectrum(ctx, mfccBands)

        # if hfc > hfcMean*0.9:
        #     hfcRect(hfc/hfcMean, ctx)




        # rawOnset = analyzer.get('onset')
        # if rawOnset > maxOnset:
        #     maxOnset  = rawOnset
        # onset = rawOnset / maxOnset
        # onsetRect(onset, ctx)


        screen.update()

        t = time.time()
        framecount +=1
        if t - prevTime >= 1:
            print('frames: ',(framecount-prevFramecount)/5)
            print('loudness: ',analyzer.get('loudness'))
            prevTime = t
            prevFramecount=framecount



def updatePitch(hpcp):
    deltaT = 0.1
    global pitches, maxPitches
    i = 0
    max = 0
    currIdx = 0
    for w in hpcp:
        if w >= maxPitches[i]:
            maxPitches[i] = w
        pitchRatio = w/maxPitches[i]
        if pitchRatio > pitches[i]:
            pitches[i] = ((9*pitches[i])+(w/maxPitches[i]))/10.0
        else:
            pitches[i] = ((3*pitches[i])+(w/maxPitches[i]))/4.0
        i+=1

def updateLoud(l):
    global maxLoud, loudRatio
    if l > maxLoud:
        maxLoud = l
    loudRatio = l/maxLoud

main()