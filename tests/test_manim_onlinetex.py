from manim_onlinetex import __version__
from os import listdir
from os.path import splitext, isfile, join

from manim import *
from manim_onlinetex import *


def test_version():
    assert __version__ == "0.1.0"


def test_rendering():
    singlestringmathtex = SingleStringMathTex(r"\alpha")
    mathtex = MathTex(r"\alpha", r"\beta")
    tex = Tex(r"gamma")
    bulletedlist = BulletedList(r"delta", r"epsilon")
    title = Title(r"zeta", r"eta")

    files = [
        f
        for f in listdir(config.get_dir("tex_dir"))
        if (isfile(join(config.get_dir("tex_dir"), f)) and not (f.startswith(".")))
    ]

    assert all([splitext(f)[1] in (".tex", ".svg") for f in files])
