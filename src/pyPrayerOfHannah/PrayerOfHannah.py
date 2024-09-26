from fasthtml import common as fh

app,rt = fh.fast_app()

@rt('/')
def get(): return fh.Div(fh.P('Hello World!'), hx_get="/change")

fh.serve()