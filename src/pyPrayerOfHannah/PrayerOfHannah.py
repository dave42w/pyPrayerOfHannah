from fasthtml import common as fh

def _not_found(req, exc): return fh.Titled('Oh no!', fh.Div('We could not find that page :('))

markdown_js = """
import { marked } from "https://cdn.jsdelivr.net/npm/marked/lib/marked.esm.js";
proc_htmx('.markdown', e => e.innerHTML = marked.parse(e.textContent));
"""


app = fh.FastHTML(exception_handlers={404: _not_found},
                  hdrs=(fh.picolink,
                        fh.Style(':root { --pico-font-size: 100%; }'),
                        fh.SortableJS('.sortable'),
                        fh.Script(markdown_js, type='module')
                       )
                 )

rt = app.route

@rt('/')
def get(): return fh.Div(fh.P('Hello World!'), hx_get="/change")

def main() -> None:
    #db = Dbms()
    #db.create_database_structure()
    fh.serve()

if __name__ == "__main__":
    main()
