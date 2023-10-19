import pickle, gzip
from operator import itemgetter
from typing import Dict, List

from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
# import pandas as pd

import Levenshtein

MIN_LEVEN_SIM_SCORE = 0.75

with gzip.open("searchModel_2.pickle.gz", "rb") as zf:
    model = pickle.load(zf)
    SELECTED_ESCO_SPANS: List[str] = model["spans"]
    COMPARE_SCORE = model["scores"]


# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder_unfiltered.csv')

app = Dash(
    title="Related jobpostings",
    name=__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app._favicon = None

app.layout = html.Div([
    html.H1(children='Related Skills', style={'textAlign':'center'}),
    # dcc.Dropdown(df.country.unique(), 'Canada', id='dropdown-selection'),
    # dcc.Graph(id='graph-content')
])
app.layout = dbc.Container(
    # dbc.Alert("Hello Bootstrap!", color="success"),
    [
        dbc.Row(dbc.Col(
            [
                html.H1(children='Related Skills', style={'textAlign':'center'}),
            ]
        )),
        dbc.Row(
            [
                dbc.Col(dbc.Input(placeholder="A large input...", size="lg", id="searchInput"), width=10),
                dbc.Col(dbc.Button("Search", id="searchButton", n_clicks=0)),
                # dbc.Col(html.Div("One of three columns")),
            ],
            align="center"
        ),
        dbc.Row([

        ], className="m-4", id="searchOutputDiv"),
    ],
    className="p-5",
)

@callback(
    Output("searchOutputDiv", "children"),
    [Input("searchButton", "n_clicks"), State("searchInput", "value")]
    , prevent_initial_call=True
)
def on_searchbutton_click(_, searchInput: str):
    print(searchInput)
    sr = search_span(searchInput)

    if len(sr) == 0:
        return dbc.Alert("Cannot found related jobspans.", color="warning")

    return html.Div([
        html.H3(f"Jobspans similar to {searchInput}:"),
        html.Ol([
            html.Li([
                html.H5(ss),
                html.Ol([html.Li(rs) for rs in rps])
            ], className="mb-5")
            for ss, rps in sr.items()
        ])
    ])
    return str(sr)

def search_span(span: str) -> Dict[str, List[str]]:
    span = span.lower().strip()
    
    if span in SELECTED_ESCO_SPANS:
        spans = [span]
    else:
        most_similar_esco_spans = [
            (s, Levenshtein.ratio(span, s, processor=lambda t: t.lower(), score_cutoff=MIN_LEVEN_SIM_SCORE))
            for idx, s in enumerate(SELECTED_ESCO_SPANS)
        ]
        most_similar_esco_spans = filter(lambda p: p[1] > 0.0, most_similar_esco_spans)
        most_similar_esco_spans = list(sorted(most_similar_esco_spans, key=itemgetter(1), reverse=True))
        # print(most_similar_esco_spans)
        spans = list(map(itemgetter(0), most_similar_esco_spans[:5]))

        # span_index = list(map(itemgetter(0))) most_similar_esco_spans[0][0]

        # selected_span_near_to_input = SELECTED_ESCO_SPANS[most_similar_esco_spans[0][0]]
    
    # print(spans)
    result: Dict[str, List[str]] = dict()
    for s in spans:
        idx = SELECTED_ESCO_SPANS.index(s)
        sims = COMPARE_SCORE[idx]
        most_similar = np.argsort(sims)[-2:-12:-1]
        result[s] = [SELECTED_ESCO_SPANS[sidx] for sidx in most_similar]
        # print(SELECTED_ESCO_SPANS[idx], " ==> ", SELECTED_ESCO_SPANS[most_similar])

    return result


if __name__ == '__main__':
    app.run(debug=True)
