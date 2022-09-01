import requests
import urllib
import base64

from manim import config, logger
from manim.utils.tex_file_writing import generate_tex_file
import manim.mobject.text.tex_mobject


def tex_to_svg_file_online(expression, environment=None, tex_template=None):
    """Takes a tex expression and returns the path to the svg file of the compiled tex
    after compiling it via one of two online rendering services: LaTeXCluster or QuickLaTeX

    Parameters
    ----------
    expression : :class:`str`
        String containing the TeX expression to be rendered, e.g. ``\\sqrt{2}`` or ``foo``
    environment : Optional[:class:`str`], optional
        The string containing the environment in which the expression should be typeset, e.g. ``align*``
    tex_template : Optional[:class:`~.TexTemplate`], optional
        Template class used to typesetting. If not set, use default template set via `config["tex_template"]`

    Returns
    -------
    :class:`str`
        Path to generated SVG file.
    """
    if tex_template is None:
        tex_template = config["tex_template"]
    tex_file = generate_tex_file(expression, environment, tex_template)

    # NOTE: QuickLaTeX is a much smaller service than LaTeXCluster. As such, it is preferred that
    # quicklatex be used if and only if LaTeXCluster is down.

    hosts = [
        "https://www.latexcluster.org/api/compileLatex",
        "https://www.quicklatex.com/latex3.f",
    ]

    try:
        hostid = (
            1
            if urllib.request.urlopen("https://www.latexcluster.org").getcode() != 200
            else 0
        )
    except urllib.error.HTTPError:
        hostid = 1

    if hostid == 0:
        params = {
            "content": tex_template.get_texcode_for_expression_in_env(
                expression, environment
            )
            if environment is not None
            else tex_template.get_texcode_for_expression(expression),
            "compile_mode": "full",  # So we can give them the entire latex file.
            "crop": True,
            "format": "svg",
            "resolution": 100,
        }
        payload = params
    elif hostid == 1:
        if environment is not None:
            begin, end = tex_template._texcode_for_environment(environment)
            formula = f"{begin}\n{expression}\n{end}"
        else:
            formula = expression
        params = {
            "formula": formula,
            "preamble": tex_template.preamble,
            "out": 2,  # 2 For SVG output (though the recieved URL is a png...)
        }
        payload = urllib.parse.urlencode(
            params, quote_via=urllib.parse.quote
        )  # This is so requests doesn't use plus signs instead of spaces like it usually does.

    logger.debug(f'Rendering "{expression}" via {hosts[hostid]}...')

    response = requests.post(hosts[hostid], data=payload)

    if hostid == 0:
        responsedict = response.json()
        if responsedict["error"] == True:
            if responsedict["content"].find("! LaTeX Error") > -1:
                relevant_error_start = responsedict["content"].find("! LaTeX Error")
                error = responsedict["content"][relevant_error_start:]
            else:
                error = responsedict["content"]
            logger.error(error)
        else:
            svgtext = base64.b64decode(responsedict["content"]).decode("utf-8")

    elif hostid == 1:
        if not response.text.startswith("0"):
            error = "\n".join(
                response.text.split("\r\n")[2:]
            )  # First 2 lines are API error code and error image URL resp.
            logger.error(error)
        else:
            svgurl = response.text.split("\n")[-1].split(" ")[0].replace("png", "svg")
            svgtext = requests.get(svgurl, headers={"Accept-Encoding": "identity"}).text

    svgfilepath = tex_file.replace("tex", "svg")
    with open(svgfilepath, "w") as svgfile:
        svgfile.write(svgtext)
    logger.debug(f'SVG of "{expression}" written to {svgfilepath}')

    return svgfilepath


manim.mobject.text.tex_mobject.tex_to_svg_file = tex_to_svg_file_online
