# Makes Sphinx create a <link> to feedparser.css in the HTML output
def setup(app):
    app.add_css_file("feedparser.css")
    return {
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
