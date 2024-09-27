from dbms import Dbms
from fasthtml import common as fh
from models import Song_Book
from sqlmodel import Session, select

db = Dbms()
db.create_database_structure()


def song_book_row(sb: Song_Book) -> fh.Div:
    return fh.Tr(fh.Td(sb.name, sb.code))


def song_books():
    with Session(db.engine) as session:
        results: Sequence[Song_Book] = session.exec(select(Song_Book).order_by(Song_Book.name)).all()
        return fh.Table(map(song_book_row, results))



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
def get():
    title = "Prayer Of Hannah"
    body = fh.Div(fh.P('Hello World!'), hx_get="/song_books")
    return fh.Title(title), fh.Container(body)

@rt('/song_books')
def get():
    title = "Prayer Of Hannah"
    body = fh.Div(fh.P(song_books()), hx_get="/song_books")
    return fh.Title(title), fh.Container(body)

def main() -> None:
    fh.serve()

if __name__ == "__main__":
    main()

'''
    <h1>Prayer of Hannah: Authors</h1>
    {{#if error}}<h2><b>Error: {{error}}</b></h2>{{/if}}

	<table class="author_list">
		<caption>Authors of Songs/Hymns</caption>
		<thead>
			<tr><th>Surname, First Name</th></tr>
			<tr><th>Display Name</th></tr>
		</thead>
		<tbody>
	  		{{#each authors.authors}}
	  			<tr>
					<td><a href="/Song/Author/{{id}}"><b>{{surname}}</b>, {{first_name}}</a></td>
					<td>{{display_name}}</td>
				</tr>
		  {{/each}}
		</tbody>
	</table>
	<p>
		<form style="display: inline;" action="/Song/Author/add" method="GET" enctype="application/x-www-form-urlencoded">
			<input style="display: inline;" type="submit" name="Submit" value="Add" />
		</form>
	</p>
'''