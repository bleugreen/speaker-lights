from palette import Palette
import cairo

from screen import Screen

class Ambient:
    def drawLinearGradient(ctx, params, palette):
        speakers = params['layout']
        panels = params['panels']

        if 'left' in panels and 'right' in panels and 'center' in panels:
            drawLinearGradientLCR(ctx, params, palette)
        elif 'left' in panels and 'center' in panels:
            drawLinerGradientLC(ctx, params, palette)
        elif 'right' in panels and 'center' in panels:
            drawLinerGradientCR(ctx, params, palette)
        elif 'left' in panels and 'right' in panels:
            drawLinerGradientLR(ctx, params, palette)
        