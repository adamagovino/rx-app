import pandas as pd
import numpy as np
from pandas import DataFrame

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table as dt
from dash.dependencies import Input, Output, State

import flask

import plotly.express as px
import plotly.graph_objs as go

import time
import datetime

import warnings

warnings.filterwarnings('ignore')

rxshort17 = pd.read_csv('https://raw.githubusercontent.com/adamagovino/rx-app/main/rx_short17.csv')
rxshort18 = pd.read_csv('https://raw.githubusercontent.com/adamagovino/rx-app/main/rx_short18.csv')
rxshort19 = pd.read_csv('https://raw.githubusercontent.com/adamagovino/rx-app/main/rx_short19.csv')
rxshort20 = pd.read_csv('https://raw.githubusercontent.com/adamagovino/rx-app/main/rx_short20.csv')
rxshort21 = pd.read_csv('https://raw.githubusercontent.com/adamagovino/rx-app/main/rx_short21.csv')

# rxshort17 = pd.read_csv('rx_short17.csv')
# rxshort18 = pd.read_csv('rx_short18.csv')
# rxshort19 = pd.read_csv('rx_short19.csv')
# rxshort20 = pd.read_csv('rx_short20.csv')
# rxshort21 = pd.read_csv('rx_short21.csv')

dff = pd.concat([rxshort17, rxshort18, rxshort19, rxshort20, rxshort21])

exempt_classes = ['Covid Testing']
inverse_boolean_series = ~dff.New_Class.isin(exempt_classes)
df = dff[inverse_boolean_series]

drug_array = df['Drug_Name'].unique()
drug_list = drug_array.tolist()

drug_str = (str(w) for w in drug_list)

# https://www.bootstrapcdn.com/bootswatch/
# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}],

                suppress_callback_exceptions=True)

server = app.server

image1 = 'data:image/jpeg;base64,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'
image2 = "data:image/jpeg;base64,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"
image3 = 'https://previews.123rf.com/images/sanek13744/sanek137442004/sanek13744200400956/145465385-prescription-icon-in-comic-style-rx-document-cartoon-vector-illustration-on-white-isolated-backgroun.jpg'
image4 = 'data:image/jpeg;base64,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'
genie = 'https://t4.ftcdn.net/jpg/03/35/87/09/360_F_335870951_YOHbsBpoBva5TFpCwNqRdsurzzwLukuI.jpg'

algo = dbc.Container([

    # Title
    html.Br(),

    dbc.Row([

        dbc.Container([
            html.H1("RX Insurance Genie", style={'textAlign': 'center', 'fontSize': 85}, className="display-3"
                    ),
            html.P(
                "Independent Pharmacists: Make More Efficient Prescription Filling Decisions to Improve Your Business Using Aggregrate Data",
                style={'textAlign': 'center', 'font-size': 20,  # 'font-weight': 'bold'
                       },
                # className="lead",
            )
        ], style={'backgroundColor': '#DCDCDC',  # 'textAlign':'center'
                  }
        ),
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.CardDeck(
                [
                    dbc.Card([
                        html.Div(html.Img(src=image1, style={'height': '100%', 'width': '50%'}),
                                 style={'textAlign': 'center'}),

                        # dbc.CardImg(src=image1, top=True),
                        dbc.CardBody([

                            html.H4([html.Span("Step 1: Choose Med", id='tooltip-target1',
                                               style={"textDecoration": "underline", "cursor": "pointer"},
                                               className="card-title")], style={'textAlign': 'center'}),

                            dbc.Tooltip(
                                "Type in the medication you are researching",
                                target="tooltip-target1",
                            ),

                            dcc.Dropdown(id='meds-dpdn', multi=False, value='LOSARTAN 100MG TAB',
                                         options=[{'label': x, 'value': x}
                                                  for x in sorted(drug_str)])
                        ])
                    ], color='primary', outline=True),

                    dbc.Card([
                        html.Div(html.Img(src=image4, style={'height': '150%', 'width': '50%'}),
                                 style={'textAlign': 'center'}),

                        dbc.CardBody([

                            html.H4([html.Span("Step 2: Choose Insurance", id='tooltip-target2',
                                               style={"textDecoration": "underline", "cursor": "pointer"},
                                               className="card-title")], style={'textAlign': 'center'}),

                            dbc.Tooltip(
                                "Determine which prescription insurance you are billing",
                                target="tooltip-target2",
                            ),

                            dcc.Dropdown(id='plans-dpdn',
                                         value=[],
                                         options=[])
                        ])

                    ], color='primary', outline=True),

                    dbc.Card([
                        html.Div(html.Img(src=image3, style={'height': '100%', 'width': '50%'}),
                                 style={'textAlign': 'center'}),

                        dbc.CardBody([

                            html.H4([html.Span("Step 3: Choose Plan Group", id='tooltip-target3',
                                               style={"textDecoration": "underline", "cursor": "pointer"},
                                               className="card-title")],
                                    style={'textAlign': 'center'}),

                            dbc.Tooltip(
                                "Determine the specific group under your chosen insurance",
                                target="tooltip-target3",
                            ),

                            dcc.Dropdown(id='groups-dpdn',
                                         value=[],
                                         options=[])
                        ])
                    ], color='primary', outline=True
                    )

                ]
            )

        ])
    ], no_gutters=True),

    # Heading for Content
    html.Br(),

    dbc.Card([
        html.Div(html.Img(src=genie, style={'height': '15%', 'width': '15%'}), style={'textAlign': 'center'}),

        dbc.CardBody([
            html.H4([html.Span("Step 4: Find the Best Spread For Each NDC For:",
                               id='spread',
                               style={"textDecoration": "underline", "cursor": "pointer"}, className="card-title"
                               ),
                     ], style={'textAlign': 'center', }),

            dbc.Tooltip(
                "Spread is the net difference between what you are reimbursed for a medication and what it costs you to purchase.  In this tool, spread is defined per unit."
                "For example, if thirty atenolol 100mg costs $2.00 and the plan reimburses $5.00, there is a net of $3.00 for thirty pills which would calculate to $0.10 spread per pill(unit)."
                "Note that in other dosage forms, such as solutions, eye drops, or inhalers, a unit may be defined by however that product is measured, such as an ml or gram.",
                target="spread"),

        ])
    ], color='primary', outline=True),

    # Output for Content
    dbc.Row([
        dbc.Col(children=
                html.H3(id='ind_heading')
                )
    ]),

    html.Div([
        dcc.Tabs(id='tabs-example', value='tab-1', children=[

            dcc.Tab(label='', style={"textDecoration": "underline", "cursor": "pointer"}, id='first-tab',
                    value='tab-1'),
            dcc.Tab(label='', style={"textDecoration": "underline", "cursor": "pointer"}, id='second-tab',
                    value='tab-2'),
            dcc.Tab(label='', style={"textDecoration": "underline", "cursor": "pointer"}, id='third-tab', value='tab-3')
        ]),
        html.Div(id='tabs-example-content')
    ]),

    dbc.Tooltip(
        "Results from the exact medication/strength you are researching. These are the most PRECISE results with regard to the medication and strength you have selected.",
        target="first-tab"),
    dbc.Tooltip(
        "Results from the entire class of medications based on the medication you input (ie if you chose atorvastatin, this tab would show all of the statin medications and all of their strengths, including pravastatin, simvastatin, rosuvastatin, etc).  These are BROADER results, but would give you a WIDER range of optional reimbursement opportunities.",
        target="second-tab"),
    dbc.Tooltip(
        "Results from the entire disease state based on the medication you input (ie if you chose atorvastatin, you would get ALL possible classes of medications used to treat cholesterol - statins, bile acid sequestrants, fish oils, etc).   These are the BROADEST possible results, but would give you the WIDEST range of optional reimbursement opportunities.",
        target="third-tab"),

],  # fluid=True
)

howto = dbc.Container([
    dbc.Row(html.P()),
    
    html.H1('How Do I Use This?'),

    dbc.Row(html.P()),

    dcc.Markdown('**To find the best reimbursed solution for a particular medication on a particular plan, you will need to follow these 4 steps:**'),
    dbc.Row(html.P()),
    
    html.P('Step 1: Choose the medication & strength (either type in or use the dropdown)'),
    html.P('Step 2: Choose the insurance plan'),
    html.P('Step 3: Choose the insurance group'),
    dbc.Row(html.P()),
    
    dcc.Markdown('**This will lead to Step 4: Opening up three tabs/paths for you to explore the NDC with the best spread for:**'),
    dbc.Row(html.P()),
    
    html.P('1) The exact medication and strength you chose (precise)'),
    html.P('2) The same class of the medication you chose (broader)'),
    html.P('3) The same indication of the medication you chose (broadest)'),
    dbc.Row(html.P()),        
    
    dcc.Markdown('**Example: Let’s say you choose atorvastatin 20mg under insurance plan A and group 1.  This is a statin class medication for high cholesterol.  The three tabs will show you:**'),
    html.P('1) The most recent spread for each atorvastatin 20mg NDC under plan A, group 1.'),
    html.P('2) The NDCs with the best spreads for the entire statin class under plan A, group 1'),
    html.P('3) The NDCs with the best spreads for any medication from any class that treats high cholesterol under plan A, group 1'),
    dbc.Row(html.P()),

    dcc.Markdown('**Notes**'),
    html.P('- Tables are pre-sorted according to the highest spread.  You also have the ability to sort by date as the highest spread NDC may be an older claim.'),
    html.P('- Spread is the net difference between what you are reimbursed for a medication and what it costs you to purchase.  In this tool, spread is defined per unit. For example, if thirty atenolol 100mg costs $2.00 and the plan reimburses $5.00, there is a net of $3.00 for thirty pills which would calculate to $0.10 spread per pill (Note that in other dosage forms, such as solutions, eye drops, or inhalers, a unit may be defined by however that product is measured, such as an ml or gram).'),

])

background = dbc.Container([

    dbc.Row(html.P()),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1('Background'),
                html.P(
                    'A majority of business for an independent retail pharmacist comes from processing prescriptions through insurance plans.  A patient visits the doctor and a prescription is sent over to the pharmacy to be filled.  One would imagine that the business of running a pharmacy would generally follow a very simple model - if you fill more prescriptions, you’ll be more profitable.  Not only that, but if you know what prescriptions you’re filling and can estimate your volume, you’ll have a pretty clear idea of where you\'ll be sitting when it comes time to tally up the finances - pretty simple, right?'),
                html.P(
                    'Unfortunately, for years, pharmacists have operated not knowing what they’ll get paid for a generic medication until it is time to fill that prescription.  What should be a very simple and predictable business model suddenly becomes completely unpredictable.  If a patient is given a prescription for a one month supply with six refills, it is entirely possible (and not at all rare) for that pharmacy to get six different reimbursements over the six month life of that prescription.  How can you operate a retail establishment not knowing what you’ll make on the products you dispense?'),
                html.P(
                    'Reimbursements for prescriptions are based on the contracts that pharmacies (are forced to) sign with insurance companies.  These contracts are incredibly (and purposely) vague, giving the processors of prescriptions - pharmacy benefit managers (or ‘PBMs’) the ability to give ambiguity to each individual generic prescription reimbursement and what a pharmacist will get paid for it.  The hows and whys of this paradigm are a separate battle (and one that is being fought on a daily basis) for pharmacists - but the fact remains that independent pharmacists are forced to operate under these conditions if they want to continue business.  Before you ask - no, these contracts are not negotiable as PBMs have the power to force a “take it or leave it” approach.'),
                html.P(
                    'In many cases, pharmacists are paid differently based on the National Drug Code (NDC) for a particular medication.  When a medication loses its patent and becomes generic, you will find that there are multiple companies making that particular medication and strength, and each would have it’s own NDC.  For different reasons (usually related to contracts that PBMs have with drug manufacturers), reimbursement can be different based on NDC - even though you are dispensing the same exact medication and strength.  Unfortunately, in many cases, choosing the correct NDC can mean the difference between filling a prescription for a profit and filling it for a loss.  To explore each NDC option would add an inordinate amount of time to each prescription fill.'),
                dcc.Markdown(
                    '**TL;DR: Using existing and continuously updating data, this tool aims to give pharmacists assistance to make better-informed decisions regarding which NDCs to purchase based on more favorable reimbursements (and therefore better spreads).**'),
                html.P(
                    '*Note this tool will be mainly useful for generic medications only.  Brand name medications are single-source items with documented, industry standard pricing.  This is the one area in a PBM contract where reimbursement would be much more concrete.  Unfortunately, brand name items make up less than 10% of the marketplace (a figure that has lowered every year for almost two decades), so this tool still applies to over 90% of prescriptions filled.')
            ]),

        )
    ])
])

data = dbc.Container([
    dbc.Row(html.P()),

    html.H1('Data FAQ'),
    dbc.Row(html.P()),

    dcc.Markdown('**Why am I getting more than one result for NDC with the best spread?**'),
    html.P(
        'PBM reimbursements can be very fickle.  What may have been the highest spread yesterday may not be the highest spread today.'
        'The tables that result from your inquiries can have up to five results.  This will give you options to get the highest possible spread according to your parameters'),
    dbc.Row(html.P()),

    dcc.Markdown('**Where does the data come from?**'),
    html.P(
        'The data used in this tool is an aggregate of reimbursement data collected from prescription insurance claims.'
        "  It is limited in that it only represents a tiny fraction of the billions of prescriptions filled nationwide."),
    dbc.Row(html.P()),

    dcc.Markdown('**How often is the data updated?**'),
    html.P("The data is currently updated on a weekly basis."),
    dbc.Row(html.P()),

    dcc.Markdown('**What is the goal of this tool?**'),
    html.P(
        "The tool would be best used if a healthy number of independent pharmacies were able to submit their reimbursement data in realtime"
        " on a constant basis, as this would allow for the most data and thus the greatest possible spread accuracy for use by pharmacists."),
    dcc.Markdown(
        '*The goal would be for the tool to function and view medication reimbursement in the same vein as the stock market.*'),
    dbc.Row(html.P()),

    dcc.Markdown('**Can you use machine learning for predictive analysis and build that into the tool?**'),
    html.P(
        "The mechanisms by which the PBM function to price reimbursement seem to vary without any discernable pattern, though this is something that I am looking for trends on."),
    dbc.Row(html.P()),

    dcc.Markdown('**What can be improved upon in this tool?**'),
    html.P(
        "One thing that will vary from pharmacy to pharmacy is acquisition cost of medication, which obviously can affect the spread.  As more pharmacies use the tool, there would need to be a way to keep track of this cost in order to properly calculate an accurate spread."),
    dbc.Row(html.P()),

])

PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

navbar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                    dbc.Col(dbc.NavbarBrand("RxGenie", className="ml-2")),

                    dbc.NavLink("Home", href="/home", active="exact"),
                    dbc.NavLink("Background", href="/background", active="exact"),
                    dbc.NavLink("How To Use This", href="/howto", active="exact"),
                    dbc.NavLink("Data FAQ", href="/data", active="exact")

                ],
                align="center",
                # no_gutters=True,
            ),
            href="https://my-rxtool.herokuapp.com/home",
        ),
        dbc.NavbarToggler(id="navbar-toggler")
    ],
    color="dark",
    dark=True,
)

# nav = dbc.Nav(
#     [
#         dbc.NavLink("Home", active=True, href="/home"),
#         dbc.NavLink("About", href="/about")
#     ]
# )

content = html.Div(id="page-content", children=[], style={'backgroundColor': 'white'})  # style=CONTENT_STYLE)

app.layout = html.Div([
    dcc.Location(id="url"),
    navbar,
    content
])


######CALLBACKS########

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def render_page_content(pathname):
    if pathname == "/home":
        return [algo]

    if pathname == '/howto':
        return [howto]

    if pathname == "/background":
        return [background]

    if pathname == "/data":
        return [data]

    else:
        return [algo]


# Populate the options of plans dropdown based on meds dropdown
@app.callback(
    Output('plans-dpdn', 'options'),
    [Input('meds-dpdn', 'value')]
)
def plans(chosen_med):
    dff = df[df.Drug_Name == chosen_med]
    return [{'label': c, 'value': c} for c in sorted(dff.Plan.unique())]


# populate initial value of plans dropdown
@app.callback(
    Output('plans-dpdn', 'value'),
    [Input('plans-dpdn', 'options')]
)
def plans_value(available_options):
    return available_options[0]['value']


# Populate the options of groups dropdown based on plans dropdown
@app.callback(
    Output('groups-dpdn', 'options'),
    [Input('plans-dpdn', 'value')],
    [State('meds-dpdn', 'value')]
)
def groups(chosen_plan, chosen_med):
    dff = df[(df.Drug_Name == chosen_med) & (df.Plan == chosen_plan)]
    return [{'label': c, 'value': c} for c in sorted(dff.Group.unique())]


# populate initial value of groups dropdown
@app.callback(
    Output('groups-dpdn', 'value'),
    [Input('groups-dpdn', 'options')]
)
def groups_value(available_options):
    return available_options[0]['value']


# Three tabs content
@app.callback(
    Output('tabs-example-content', 'children'),
    [Input('tabs-example', 'value'),
     Input('plans-dpdn', 'value'),
     Input('groups-dpdn', 'value')],
    [State('meds-dpdn', 'value')]
)
def render_content(tab, plan, group, med):
    filt_exact = df[df['Drug_Name'] == med]
    ndc = filt_exact['NDC'].iloc[0]
    brand_gen = filt_exact['Brand/Generic'].iloc[0]
    route = filt_exact['Route'].iloc[0]

    split_name = (med.split())[0]
    first6 = split_name[0:6].lower().replace(' ', '')
    filt_med = df[(df['Drug Name First6'] == first6) & (df['Plan'] == plan) & (df['Group'] == group)]

    strength = df[df['Drug_Name'] == med]['Strength'].iloc[0]
    filt_strength = filt_med[filt_med['Strength'] == strength]
    filt_strength['Date'] = pd.to_datetime(filt_strength['Date']).dt.date
    filt_strength.sort_values(by=['Date'], inplace=True, ascending=False)  # This now sorts in date order

    med_class = filt_exact['New_Class'].iloc[0]
    indication1 = filt_exact['Indication_One'].iloc[0]
    indication2 = filt_exact['Indication_Two'].iloc[0]
    indications = [indication1, indication2]
    route = filt_exact['Route'].iloc[0]

    filt_class = df[
        (df['New_Class'] == med_class) & (df['Plan'] == plan) & (df['Route'] == route) & (df['Group'] == group)]
    filt_ind = df[((df['Plan'] == plan) & (df['Route'] == route) & (df['Group'] == group) & (
                df['Indication_One'] == indication1)) |
                  ((df['Plan'] == plan) & (df['Route'] == route) & (df['Group'] == group) & (
                              df['Indication_One'] == indication2)) |
                  ((df['Plan'] == plan) & (df['Route'] == route) & (df['Group'] == group) & (
                              df['Indication_Two'] == indication1)) |
                  ((df['Plan'] == plan) & (df['Route'] == route) & (df['Group'] == group) & (
                              df['Indication_Two'] == indication2))]

    # Table based on same drug and strength
    ndcs = list(set(filt_strength['NDC']))
    ndc_list = []
    spu_list = []
    date_list = []
    for ndc in ndcs:
        ndc_list.append(ndc)
        filtst = filt_strength[filt_strength['NDC'] == ndc]
        filtst.sort_values(by=['Date'], inplace=True, ascending=False)
        latest_spu = filtst['SPU'].iloc[0]
        latest_date = filtst['Date'].iloc[0]
        spu_list.append(latest_spu)
        date_list.append(latest_date)

    ndc_df = pd.DataFrame({'NDC': ndc_list, 'Spread': spu_list, 'Date': date_list})
    ndc_df.sort_values(by=['Spread'], inplace=True, ascending=False)

    # Table based on same class
    ndcc = list(set(filt_class['NDC']))
    ndcc_list = []
    spuc_list = []
    datec_list = []
    med_list = []
    for ndc in ndcc:
        ndcc_list.append(ndc)
        filtcl = filt_class[filt_class['NDC'] == ndc]
        filtcl.sort_values(by=['Date'], inplace=True, ascending=False)
        latest_spuc = filtcl['SPU'].iloc[0]
        latest_datec = filtcl['Date'].iloc[0]
        med_name = filtcl['Drug_Name'].iloc[0]
        spuc_list.append(latest_spuc)
        datec_list.append(latest_datec)
        med_list.append(med_name)

    ndcc_df = pd.DataFrame({'Med': med_list, 'NDC': ndcc_list, 'Spread': spuc_list, 'Date': datec_list})
    ndcc_df.sort_values(by=['Spread'], inplace=True, ascending=False)
    ndcc_df_short = ndcc_df[:5]

    # Table based on Indication
    ndci = list(set(filt_ind['NDC']))
    ndci_list = []
    spui_list = []
    datei_list = []
    medi_list = []
    for ndc in ndci:
        ndci_list.append(ndc)
        filti = filt_ind[filt_ind['NDC'] == ndc]
        filti.sort_values(by=['Date'], inplace=True, ascending=False)
        latest_spui = filti['SPU'].iloc[0]
        latest_datei = filti['Date'].iloc[0]
        med_namei = filti['Drug_Name'].iloc[0]
        spui_list.append(latest_spui)
        datei_list.append(latest_datei)
        medi_list.append(med_namei)

    ndci_df = pd.DataFrame({'Med': medi_list, 'NDC': ndci_list, 'Spread': spui_list, 'Date': datei_list})
    ndci_df.sort_values(by=['Spread'], inplace=True, ascending=False)
    ndci_df = ndci_df.head()

    # TAB 1: EXACT MED
    if tab == 'tab-1':

        heading = html.Div([

            html.H5([html.Span("Most Recent Spread for Each NDC Billed Under this Plan/Group",
                               id='heading1',
                               style={"cursor": "pointer"},
                               )
                     ], style={'textAlign': 'center', }),
            dbc.Tooltip(
                'Tables are pre-sorted according to the highest spread.  You also have the ability to sort by date as the highest spread NDC may be an older claim.',
                target="heading1", ),
        ])

        datatable = html.Div([dt.DataTable(
            data=ndc_df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in ndc_df.columns],
            sort_action="native",
            style_as_list_view=True,
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
            style_cell={
                'backgroundColor': '#DCDCDC',
            }

        )])

        lenf = len(filt_strength)

        if len(filt_strength) > 1:
            fig = go.Figure()
            # for ndc in ndcs:
            # new_filt = filt_strength[filt_strength['NDC'] == ndc]
            # fig.add_trace(go.Scatter(x=new_filt['Date'], y=new_filt['SPU'], mode='lines+markers', name=ndc))

            for ndc in ndcs:
                new_filt = filt_strength[filt_strength['NDC'] == ndc]
                fig.add_trace(go.Scatter(
                    x=new_filt['Date'],
                    y=new_filt['SPU'],
                    mode='lines+markers',

                    name=ndc,
                ))
            fig.update_layout(title={
                'text': 'Historical Spreads For ' + med,
                'y': 0.9,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'
            })

            spacing = html.Br()
            graph = html.Div(dcc.Graph(figure=fig))

            return spacing, heading, datatable, graph

        else:
            return html.Br(), heading, datatable

    # TAB 2: CLASS OF MEDS
    elif tab == 'tab-2':

        heading = html.Div([

            html.H5([html.Span("Top 5 Spreads For All " + med_class,
                               id='heading2',
                               style={"textDecoration": "underline", "cursor": "pointer"},
                               )
                     ], style={'textAlign': 'center', }),
            dbc.Tooltip(
                'Tables are pre-sorted according to the highest spread.  You also have the ability to sort by date as the highest spread NDC may be an older claim.',
                target='heading2', ),
        ])

        # heading = html.H5("Best Spreads For All " + med_class, className='text-center text-primary mb-4')

        datatable = html.Div([dt.DataTable(
            data=ndcc_df_short.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in ndcc_df.columns],
            style_as_list_view=True,
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
            style_cell={
                'backgroundColor': '#DCDCDC', }
        )])

        fig = px.bar(ndcc_df, x="Med", y="Spread",
                     color="NDC", hover_data=['NDC'],
                     barmode='group', )

        fig.update_layout(title_text='All Spreads For All ' + med_class, title_x=0.5,
                          yaxis_title="Spread Per Unit in Dollars")

        graph = html.Div(dcc.Graph(figure=fig))

        new_df = df[(df['New_Class'] == med_class) & (df['Route'] == route)]
        class_meds = new_df.Drug_Name.unique().tolist()
        meds_unsorted = pd.DataFrame(class_meds, columns=['Medications in This Class'])
        meds_df = meds_unsorted.sort_values('Medications in This Class')
        datatable2 = html.Div([dt.DataTable(
            data=meds_df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in meds_df.columns],
            style_as_list_view=True,
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
            style_cell={
                'backgroundColor': '#DCDCDC', }
        )])

        lenf = len(ndcc_df)

        if lenf > 1:

            return html.Br(), heading, datatable, html.Br(), graph

        else:
            return html.Br(), heading, datatable, html.Br()



    # TAB 3: INDICATION TAB
    elif tab == 'tab-3':
        # heading = html.H5('Top Spreads For ' + indication1, className='text-center text-primary mb-4')

        datatable = html.Div([dt.DataTable(
            data=ndci_df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in ndci_df.columns],
            style_as_list_view=True,
            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'color': 'white'},
            style_cell={
                'backgroundColor': '#DCDCDC', }
        )
        ])

        return html.Br(), datatable


@app.callback(Output('first-tab', 'label'), [Input('meds-dpdn', 'value')])
def update_label(med):
    return med


@app.callback(Output('second-tab', 'label'), [Input('meds-dpdn', 'value')])
def update_label(med):
    filt_exact = df[df['Drug_Name'] == med]
    med_class = filt_exact['New_Class'].iloc[0]
    return 'All ' + med_class


@app.callback(Output('third-tab', 'label'), [Input('meds-dpdn', 'value')])
def update_label(med):
    filt_exact = df[df['Drug_Name'] == med]
    indication1 = filt_exact['Indication_One'].iloc[0]
    return 'All Medications For ' + indication1


# add callback for toggling the collapse on small screens
@app.callback(Output("navbar-collapse", "is_open"), [Input("navbar-toggler", "n_clicks")],
              [State("navbar-collapse", "is_open")], )
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
