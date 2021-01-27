# manim-onlinetex

A Manim Plugin that renders LaTeX for Mobjects like `Tex` and `MathTex` via online services.
This plugin will try to render the LaTeX required by such Mobjects via [LaTeX4Technics](https://www.latex4technics.com/), and if for some reason LaTeX4Technics is down, will attempt to use [QuickLaTeX](https://quicklatex.com/).

## Usage instructions

Import the contents of `manim_onlinetex` AFTER `manim` has been imported, like so:

```py
from manim import *
from manim_onlinetex import *
```

Then, use a `Mobject` that requires `LaTeX` rendering. If the
Plugin is doing its job, then the `Tex` folder of your `media`
directory should have the source `.tex` file, the final `.svg` 
file, and no intermediary files (like `.dvi` files), since that's
all handled by the online service.