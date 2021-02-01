#app for deployment

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

rxshort = pd.read_csv('https://raw.githubusercontent.com/adamagovino/rx-app/main/rx_short.csv')

df = rxshort

app.layout = html.Div([
    
    html.Label("Med Reimbursement Genie", style={'fontSize':70, 'textAlign':'center'}),
    html.Label("______________________________________________", style={'fontSize':30, 'textAlign':'center'}),
    html.Label("Choose Your Med:", style={'fontSize':50, 'textAlign':'center'}),
    
    dcc.Dropdown(
        id='meds-dpdn',
        options=[{'label': s, 'value': s} for s in sorted(df.Drug_Name.unique())],

        clearable=False
    ),

    html.Label("Insurance Plan:", style={'fontSize':30, 'textAlign':'center'}),
    dcc.Dropdown(
        id='plans-dpdn', 
        options=[],

    ),
    
    html.Label("Highest Reimbursed with this Indication:", style={'fontSize':40, 'textAlign':'center'}),
    html.Div(id="table1"),
    
    html.Label("Highest Reimbursed Med with Exact Strength:", style={'fontSize':40, 'textAlign':'center'}),
    html.Div(id='table2'),
    
    html.Label("Highest Reimbursed Med, Any Strength:", style={'fontSize':40, 'textAlign':'center'}),
    html.Div(id='table3')
        
])


@app.callback(
    Output('plans-dpdn', 'options'),
    Input('meds-dpdn', 'value')
)
def plans(chosen_plan):
    dff = df[df.Drug_Name==chosen_plan]
    return [{'label': c, 'value': c} for c in sorted(dff.Plan.unique())]

@app.callback(
    Output('plans-dpdn', 'value'),
    Input('plans-dpdn', 'options')
)
def plans_value(available_options):
    return [x['value'] for x in available_options]


@app.callback(
    Output('table1', 'children'),
    Input('plans-dpdn', 'value'),
    State('meds-dpdn', 'value'),
)


def update_table(plan,med):

    filt_exact = df[df['Drug_Name']==med]
    ndc = filt_exact['NDC'].iloc[0]
    brand_gen = filt_exact['Brand/Generic'].iloc[0]

    if len(filt_exact) < 1:
        print ('Drug Not Found')

    else:
        split_name = (med.split())[0]
        first6 = split_name[0:6].lower().replace(' ','')
        filt_med = df[(df['Drug Name First6']==first6) & (df['Plan']==plan)]

        strength = df[df['Drug_Name']==med]['Strength'].iloc[0]
        filt_strength = filt_med[filt_med['Strength']==strength]

        if (len(filt_med) < 1) or (len(filt_strength) <1):
            
            data = {'This Medicine Does not Have Enough Comps to Make a Table or Something Else iS Wrong':  ['First value']}

            end_function_df = pd.DataFrame(data, columns = ['This Medicine Doesnt Have Accurate Comps'])
            
            print("Drug and/or Strength Not Found Using This Plan")
            
            return html.Div([dt.DataTable(
                data=end_function_df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in end_function_df.columns],
                ),
                html.Hr()
                            ])

        #2) filtering out by 1) same med+strength 2) same med, any strength, 3) same class (any med any strength)
        else:
            med_class = filt_exact['New_Class'].iloc[0]
            indication1 = filt_exact['Indication_One'].iloc[0]
            indication2 = filt_exact['Indication_Two'].iloc[0]
            indications = [indication1,indication2]
            route = filt_exact['Route'].iloc[0]

            filt_class = df[(df['New_Class']==med_class) & (df['Plan']==plan) & (df['Route']==route)]
            filt_ind = df[(df['Indication_One']==indication1) | (df['Indication_One']==indication2) | (df['Indication_Two']==indication1) | (df['Indication_Two']==indication2)]
            
            #Table based on Indication
            ndci = list(set(filt_ind['NDC']))
            ndci_list = []
            spui_list = []
            datei_list = []
            medi_list = []
            for ndc in ndci:
                ndci_list.append(ndc)
                filti = filt_ind[filt_ind['NDC']==ndc]
                filti.sort_values(by=['Date'], inplace=True, ascending=False)
                latest_spui = filti['SPU'].iloc[0]
                latest_datei = filti['Date'].iloc[0]
                med_namei = filti['Drug_Name'].iloc[0]
                spui_list.append(latest_spui)
                datei_list.append(latest_datei)
                medi_list.append(med_namei)

            ndci_df = pd.DataFrame({'Med':medi_list,'NDC':ndci_list,'Spread':spui_list,'Date':datei_list})
            ndci_df.sort_values(by=['Spread'], inplace=True, ascending=False)
            ndci_df = ndci_df.head()
            
            return html.Div([dt.DataTable(
                data=ndci_df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in ndci_df.columns],
                ),
                html.Hr()
                            ])
        
@app.callback(
    Output('table2', 'children'),
    Input('plans-dpdn', 'value'),
    State('meds-dpdn', 'value'),
)

def update_table2(plan,med):

    filt_exact = df[df['Drug_Name']==med]
    ndc = filt_exact['NDC'].iloc[0]
    brand_gen = filt_exact['Brand/Generic'].iloc[0]

    if len(filt_exact) < 1:
        print ('Drug Not Found')

    else:
        split_name = (med.split())[0]
        first6 = split_name[0:6].lower().replace(' ','')
        filt_med = df[(df['Drug Name First6']==first6) & (df['Plan']==plan)]

        strength = df[df['Drug_Name']==med]['Strength'].iloc[0]
        filt_strength = filt_med[filt_med['Strength']==strength]

        if (len(filt_med) < 1) or (len(filt_strength) <1):
            
            data = {'This Medicine Does not Have Enough Comps to Make a Table or Something Else iS Wrong':  ['First value']}

            end_function_df = pd.DataFrame(data, columns = ['This Medicine Doesnt Have Accurate Comps'])
            
            print("Drug and/or Strength Not Found Using This Plan")
            
            return html.Div([dt.DataTable(
                data=end_function_df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in end_function_df.columns],
                ),
                html.Hr()
                            ])

        else:
            med_class = filt_exact['New_Class'].iloc[0]
            indication1 = filt_exact['Indication_One'].iloc[0]
            indication2 = filt_exact['Indication_Two'].iloc[0]
            indications = [indication1,indication2]
            route = filt_exact['Route'].iloc[0]

            filt_class = df[(df['New_Class']==med_class) & (df['Plan']==plan) & (df['Route']==route)]
            filt_ind = df[(df['Indication_One']==indication1) | (df['Indication_One']==indication2) | (df['Indication_Two']==indication1) | (df['Indication_Two']==indication2)]

            #Table based on same drug and strength
            ndcs = list(set(filt_strength['NDC']))
            ndc_list = []
            spu_list = []
            date_list = []
            for ndc in ndcs:
                ndc_list.append(ndc)
                filtst = filt_strength[filt_strength['NDC']==ndc]
                filtst.sort_values(by=['Date'], inplace=True, ascending=False)
                latest_spu = filtst['SPU'].iloc[0]
                latest_date = filtst['Date'].iloc[0]
                spu_list.append(latest_spu)
                date_list.append(latest_date)

            ndc_df = pd.DataFrame({'NDC':ndc_list,'Spread':spu_list,'Date':date_list})
            ndc_df.sort_values(by=['Spread'], inplace=True, ascending=False)
            
            return html.Div([dt.DataTable(
                data=ndc_df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in ndc_df.columns],
                ),
                html.Hr()
                            ])
        
        

@app.callback(
    Output('table3', 'children'),
    Input('plans-dpdn', 'value'),
    State('meds-dpdn', 'value'),
)


def update_table3(plan,med):

    filt_exact = df[df['Drug_Name']==med]
    ndc = filt_exact['NDC'].iloc[0]
    brand_gen = filt_exact['Brand/Generic'].iloc[0]

    if len(filt_exact) < 1:
        print ('Drug Not Found')

    else:
        split_name = (med.split())[0]
        first6 = split_name[0:6].lower().replace(' ','')
        filt_med = df[(df['Drug Name First6']==first6) & (df['Plan']==plan)]

        strength = df[df['Drug_Name']==med]['Strength'].iloc[0]
        filt_strength = filt_med[filt_med['Strength']==strength]

        if (len(filt_med) < 1) or (len(filt_strength) <1):
            
            data = {'This Medicine Does not Have Enough Comps to Make a Table or Something Else iS Wrong':  ['First value']}

            end_function_df = pd.DataFrame(data, columns = ['This Medicine Doesnt Have Accurate Comps'])
            
            print("Drug and/or Strength Not Found Using This Plan")
            
            return html.Div([dt.DataTable(
                data=end_function_df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in end_function_df.columns],
                ),
                html.Hr()
                            ])

        else:
            med_class = filt_exact['New_Class'].iloc[0]
            indication1 = filt_exact['Indication_One'].iloc[0]
            indication2 = filt_exact['Indication_Two'].iloc[0]
            indications = [indication1,indication2]
            route = filt_exact['Route'].iloc[0]

            filt_class = df[(df['New_Class']==med_class) & (df['Plan']==plan) & (df['Route']==route)]
            filt_ind = df[(df['Indication_One']==indication1) | (df['Indication_One']==indication2) | (df['Indication_Two']==indication1) | (df['Indication_Two']==indication2)]

            #Table based on same class
            ndcc = list(set(filt_class['NDC']))
            ndcc_list = []
            spuc_list = []
            datec_list = []
            med_list = []
            for ndc in ndcc:
                ndcc_list.append(ndc)
                filtcl = filt_class[filt_class['NDC']==ndc]
                filtcl.sort_values(by=['Date'], inplace=True, ascending=False)
                latest_spuc = filtcl['SPU'].iloc[0]
                latest_datec = filtcl['Date'].iloc[0]
                med_name = filtcl['Drug_Name'].iloc[0]
                spuc_list.append(latest_spuc)
                datec_list.append(latest_datec)
                med_list.append(med_name)

            ndcc_df = pd.DataFrame({'Med':med_list,'NDC':ndcc_list,'Spread':spuc_list,'Date':datec_list})
            ndcc_df.sort_values(by=['Spread'], inplace=True, ascending=False)
            ndcc_df_short = ndcc_df[:5]
            
            fig = px.scatter(ndcc_df, x="Date", y="Spread")

            graph = dcc.Graph(figure=fig)
            
            return html.Div([dt.DataTable(
                data=ndcc_df_short.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in ndcc_df.columns],
                ),
                html.Hr()
                            ]), graph 


if __name__ == '__main__':
    app.run_server(debug=False, port = 3050)
    #debug = True on IPE