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

#rxshort17 = pd.read_csv('rx_short17.csv')
#rxshort18 = pd.read_csv('rx_short18.csv')
#rxshort19 = pd.read_csv('rx_short19.csv')
#rxshort20 = pd.read_csv('rx_short20.csv')
#rxshort21 = pd.read_csv('rx_short21.csv')

dff = pd.concat([rxshort17,rxshort18,rxshort19,rxshort20,rxshort21])

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
                            'content': 'width=device-width, initial-scale=1.0'}],
                suppress_callback_exceptions=True)

server = app.server

algo = dbc.Container([

    # Title
    html.Br(),
    dbc.Row(
        dbc.Col(html.H2("Med Reimbursement Genie",
                        className='text-center text-primary mb-4'),
                width=12)
    ),

    dbc.Row([
        dbc.Col(html.Label(['Step 1: Choose Med:'], style={'font-weight': 'bold', "text-align": "center"})),
        dbc.Col(html.Label(['Step 2: Choose Insurance Plan:'], style={'font-weight': 'bold', "text-align": "center"})),
        dbc.Col(html.Label(['Step 3: Choose Plan Group:'], style={'font-weight': 'bold', "text-align": "center"}))
    ]),

    # Choose Med & Plan
    dbc.Row([
        dbc.Col(dcc.Dropdown(id='meds-dpdn', multi=False, value='LOSARTAN 100MG TAB',
                             options=[{'label': x, 'value': x}
                                      for x in sorted(drug_str)]),
                # width={'size': 5, "offset": 1, 'order': 1}
                ),

        dbc.Col(dcc.Dropdown(id='plans-dpdn',
                             value=[],
                             options=[])

                # width={'size': 5, "offset": 0, 'order': 2}
                ),
    
        dbc.Col(dcc.Dropdown(id='groups-dpdn',
                             value=[],
                             options=[])
                )]),

    # Heading for Content
    html.Br(),
    dbc.Row(
        dbc.Col(html.H3("Find the Best Reimbursed Medication For:",
                        className='text-center text-primary mb-4'),
                width=12)
    ),

    # Output for Content
    dbc.Row([
        dbc.Col(children=
                html.H3(id='ind_heading')
                )
    ]),

    html.Div([
        dcc.Tabs(id='tabs-example', value='tab-1', children=[
            dcc.Tab(label='', id='first-tab', value='tab-1'),
            dcc.Tab(label='', id='second-tab', value='tab-2'),
            dcc.Tab(label='', id='third-tab', value='tab-3')
        ]),
        html.Div(id='tabs-example-content')
    ])
])

howto = html.Div([
    dbc.Row(html.P()),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1('How Do I Use This?'),
                html.P(
                    'To find the best reimbursed solution for a particular medication on a particular plan, you will need to choose three different variables:'),
                dcc.Markdown('1) The medication & strength (either type in or use the dropdown)\n2) The insurance plan\n3) The Insurance group',
                             style={"white-space": "pre"}),
                html.P(
                    'This will then open up three tabs/paths for you to explore the best reimbursed medication for:'),
                dcc.Markdown(
                    '1) This exact medication and strength (precise)\n2) The same class of the medication you chose (broader)\n3) The same indication of the medication you chose (broadest)',
                    style={"white-space": "pre"}),
                html.P(),
                dcc.Markdown(
                    'Example:\nLet’s say you choose atorvastatin 20mg under insurance plan A and group 1.  This is a statin class medication for high cholesterol  The three tabs will show you:',
                    style={"white-space": "pre"}),
                dcc.Markdown(
                    '1) The best reimbursed NDC for atorvastatin 20mg under plan A, group 1\n2) The best reimbursed NDC for the entire statin class under plan A, group 1\n3) The best reimbursed NDC for any medication from any class that treats high cholesterol under plan A, group 1',
                    style={"white-space": "pre"}),
                html.P(),
                dcc.Markdown(
                    'Spreads in this tool are defined per unit.\nFor example, if thirty atenolol 100mg costs $2.00 and the plan reimburses $5.00, there is a net of $3.00 for thirty pills which would calculate to $0.10 spread per pill(unit).\nNote that in other dosage forms, such as solutions, eye drops, or inhalers, a unit may be defined by however that product is measured, such as an ml or gram.',
                    style={"white-space": "pre"}),
            ]),
            width={"size": 10, "offset": 1}
        )
    ])
])

background = html.Div([
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
                    'In many cases, pharmacists are paid differently based on the National Drug Code (NDC) for a particular medication.  When a medication loses its patent and becomes generic, you will find that there are multiple companies making that particular medication and strength, and each would have it’s own NDC.  For different reasons (usually related to contracts that PBMs have with drug manufacturers), reimbursement can be different based on NDC - even though you are dispensing the same exact medication and strength.  Unfortunately, in many cases, choosing the correct NDC can mean the difference between filling a prescription for a profit and filling it for a loss.'),
                dcc.Markdown(
                    '**TL;DR: Using existing and continuously updating data, this tool aims to give pharmacists assistance to make better-informed decisions regarding which NDCs to purchase based on more favorable reimbursements (and therefore better spreads).**'),
                html.P(
                    '*Note this tool will be mainly useful for generic medications only.  Brand name medications are single-source items with documented, industry standard pricing.  This is the one area in a PBM contract where reimbursement would be much more concrete.  Unfortunately, brand name items make up less than 10% of the marketplace (a figure that has lowered every year for almost two decades), so this tool still applies to over 90% of prescriptions filled.')
            ]),
            width={"size": 10, "offset": 1}
        )
    ])
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
                    dbc.Col(dbc.NavbarBrand("DataRx", className="ml-2")),

                    dbc.NavLink("Home", href="/home", active="exact"),
                    dbc.NavLink("How To Use This", href="/howto", active="exact"),
                    dbc.NavLink("Background", href="/background", active="exact")

                ],
                align="center",
                no_gutters=True,
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

content = html.Div(id="page-content", children=[])  # style=CONTENT_STYLE)

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
        # elif pathname == "/background":
        return [background]

    else:
        return [algo]


######CALLBACKS########

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
def groups(chosen_plan,chosen_med):
    dff = df[(df.Drug_Name == chosen_med)&(df.Plan==chosen_plan)]
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

    filt_class = df[(df['New_Class'] == med_class) & (df['Plan'] == plan) & (df['Route'] == route) & (df['Group'] == group)]
    filt_ind = df[((df['Plan'] == plan) & (df['Route'] == route) & (df['Group'] == group) & (df['Indication_One'] == indication1)) | 
                  ((df['Plan'] == plan) & (df['Route'] == route) & (df['Group'] == group) & (df['Indication_One'] == indication2)) | 
                  ((df['Plan'] == plan) & (df['Route'] == route) & (df['Group'] == group) & (df['Indication_Two'] == indication1)) |
                  ((df['Plan'] == plan) & (df['Route'] == route) & (df['Group'] == group) & (df['Indication_Two'] == indication2))
                 ]

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

        heading = html.H5("Most Recent Spread for Each NDC", className='text-center text-primary mb-4')
        datatable = html.Div([dt.DataTable(
            data=ndc_df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in ndc_df.columns],
            style_as_list_view=True,
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
            'backgroundColor': 'gray',
            'color': 'white'}

        )])

        lenf = len(filt_strength)

        if len(filt_strength) > 1:
            fig = go.Figure()
           # for ndc in ndcs:
                #new_filt = filt_strength[filt_strength['NDC'] == ndc]
                #fig.add_trace(go.Scatter(x=new_filt['Date'], y=new_filt['SPU'], mode='lines+markers', name=ndc))

            for ndc in ndcs:
                new_filt = filt_strength[filt_strength['NDC'] == ndc]
                fig.add_trace(go.Scatter(
                                x=new_filt['Date'], 
                                y=new_filt['SPU'], 
                                mode='lines+markers', 

                                name=ndc, 
                                ))
            fig.update_layout(title={
                'text':'Historical Spreads For ' + med,
                'y':0.9,
                'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
                })

            spacing = html.Br()
            graph = html.Div(dcc.Graph(figure=fig))

            return spacing, heading, datatable, graph

        else:
            return html.Br(),heading, datatable

    # TAB 2: CLASS OF MEDS
    elif tab == 'tab-2':

        heading = html.H5("Best Spreads For All " + med_class, className='text-center text-primary mb-4')

        datatable = html.Div([dt.DataTable(
            data=ndcc_df_short.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in ndcc_df.columns],
            style_as_list_view=True,
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
            'backgroundColor': 'gray',
            'color': 'white'},
            )])

        fig = px.bar(ndcc_df, x="Med", y="Spread",
                     color="NDC", hover_data=['NDC'],
                     barmode = 'group',
                    )
        fig.update_layout(
            title_text='All Spreads For All '+ med_class, 
            title_x=0.5, 
            yaxis_title="Spread Per Unit in Dollars"
        )
        graph = html.Div(dcc.Graph(figure=fig))

        
        new_df = df[(df['New_Class'] == med_class) & (df['Route']==route)]
        class_meds = new_df.Drug_Name.unique().tolist()
        meds_unsorted = pd.DataFrame(class_meds, columns = ['Medications in This Class'])
        meds_df = meds_unsorted.sort_values('Medications in This Class')
        datatable2 = html.Div([dt.DataTable(
            data=meds_df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in meds_df.columns],
            style_as_list_view=True,
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
            'backgroundColor': 'gray',
            'color': 'white'},
        )])
        
        lenf = len(ndcc_df)
            
        if lenf > 1:
            
            return html.Br(),heading, datatable, html.Br(), graph

        else:
            return html.Br(),heading, datatable, html.Br()



    # TAB 3: INDICATION TAB
    elif tab == 'tab-3':
        heading = html.H5('Top Spreads For ' + indication1, className='text-center text-primary mb-4')

        datatable = html.Div([dt.DataTable(
            data=ndci_df.to_dict('rows'),
            columns=[{'name': i, 'id': i} for i in ndci_df.columns],
            style_as_list_view=True,
            style_header={'backgroundColor': 'rgb(30, 30, 30)'},
            style_cell={
            'backgroundColor': 'gray',
            'color': 'white'},
        )
        ])

        return html.Br(),heading, datatable


@app.callback(
    Output('first-tab', 'label'),
    [Input('meds-dpdn', 'value')]
)
def update_label(med):
    return med


@app.callback(
    Output('second-tab', 'label'),
    [Input('meds-dpdn', 'value')]
)
def update_label(med):
    filt_exact = df[df['Drug_Name'] == med]
    med_class = filt_exact['New_Class'].iloc[0]
    return 'All ' + med_class


@app.callback(
    Output('third-tab', 'label'),
    [Input('meds-dpdn', 'value')]
)
def update_label(med):
    filt_exact = df[df['Drug_Name'] == med]
    indication1 = filt_exact['Indication_One'].iloc[0]
    return 'All Medications For ' + indication1 


# add callback for toggling the collapse on small screens
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run_server(debug=True)
