import pandas as pd
import csv
import random
from datetime import datetime as dt
import base64
#dash module imported 
import dash
#dash auth required requests module to be installed before 
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

"""
Documentation of csv

"""
databaseloc = r'E:\GitHub\project\snc_path_data.csv'
read = csv.reader(databaseloc)

columnNames = ['Date Time','IP', 'Source Node','City','Node Location','SNC-ID','Node','Path','Destination Node']
df = pd.read_csv(databaseloc,names = columnNames ,sep=',',index_col=False)

df = pd.DataFrame(df)
df.dropna(inplace=True)

#column reindex for prefrence look in table section of dash plotly 
df =df.reindex(columns=['Date Time','SNC-ID','Source Node','Destination Node','Path','City','Node','Node Location','IP'])

features =df['Source Node'].unique() 
features1 = df['Destination Node'].unique()


app = dash.Dash(__name__)

image_filename = r'E:\GitHub\project\optic.jpg' # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

#auth = dash_auth.BasicAuth(
#    app,
#    VALID_USERNAME_PASSWORD_PAIRS
#)


app.title = 'SNC Path Visualization'

# Boostrap CSS.
app.css.append_css({'external_url': 'https://codepen.io/amyoshino/pen/jzXypZ.css'})


app.layout = html.Div(
            
        html.Div(children=[
            html.Div([
                html.H3("ROADM Network-SNC Path",
                    className="nine columns",
                    style={
                        'color':'white',
                        'padding-top': '10px',
                        'margin-left': '2%',
                        'display': 'inline-block',
                        'textAlign':'center'
                        },
                    ),
                html.Img(src='data:image/png;base64,{}'.format(encoded_image),
                    className="three columns",
                     style={
                        'height': '8%',
                        'width': '8%',
                        'float': 'right',
                        'position': 'relative',
                        },
                    ),
                ],
                style={'backgroundColor':'rgb(66, 196, 247)',
                        'color':'white',
                        'border-radius': '2px'
                        },
                className="row"),
        
        html.Div([
            html.Div([
                dcc.Dropdown(
                        id='sourcenode',
                        options=[{'label': i, 'value': i} for i in features],
                        value='Source Node',
                        placeholder ="Source Node"),
                    ],
                style={'width': '25%', 'display': 'inline-block'},
                className='six columns'
            ),
           
           html.Div([
               dcc.Dropdown(
                        id='destinationnode',
                        options=[{'label': i, 'value': i} for i in features1],
                        value='Destination Node',
                        placeholder="Destination Node")
                    ],
                style={'width': '25%', 'float': 'right', 'display': 'inline-block'},
                className='six columns'
            ),
           ],className="row"),
        html.Div([
            html.Div(
                id='graph-container',className='tweleve columns'),
            ],className="row"),

           html.Div(    
            dash_table.DataTable(id='table',
            columns=[
                    {"name": i, "id": i} for i in df.columns
                ],
            pagination_settings={
                'displayed_pages':1,
                    'current_page': 0,
                    'page_size':20
                },
            
            pagination_mode='be',
            navigation="page",
            style_header={'backgroundColor': '#4CB5F5',
                            'font-weight':'bold',
                            'textAlign':'center'},
            style_cell={
                'backgroundColor': '#A5D8DD',
                'color': 'black',
                'textAlign':'left'
                },
             style_cell_conditional=[{
                 'if':{'row_index':'odd'},
                 'backgroundColor': '#4CB5F5'}
                 ],
            ),
            style={'height': 750, 'overflowY': 'scroll'},
            className='tweleve columns'
        ),
        dcc.Interval(
            id='interval-component',
            interval=5*1000, #in milliseconds
            n_intervals=0
            ),
        ]
    )

)
                      


@app.callback(
    Output('table', 'data'),
    [Input('table','pagination_settings'),
     Input('table','filtering_settings'),
     Input('sourcenode',"value"),
     Input('destinationnode','value'),
     Input('interval-component','n_intervals')])
    
def update_graph(pagination_settings,filtering_settings,source_node,destination_node,n):
    print(n)
    print(source_node)
    print(destination_node)
    df = pd.read_csv(databaseloc,names= columnNames, sep=',')
    df = pd.DataFrame(df)
    df.dropna(inplace=True)
    df=df.iloc[::-1]
    if (source_node == df['Source Node']).any() and (destination_node ==df['Destination Node']).any():
        filter_df= df[(df['Source Node']==source_node) & (df['Destination Node']==destination_node)]
        return filter_df.iloc[pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')

    elif (source_node == df['Source Node']).any():
        filter1_df= df[df['Source Node']==source_node]
        return filter1_df.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')
    
    elif (destination_node == df['Destination Node']).any():
        filter2_df= df[df['Destination Node']==destination_node]
        return filter2_df.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')

    else:
        return df.iloc[
        pagination_settings['current_page']*pagination_settings['page_size']:
        (pagination_settings['current_page'] + 1)*pagination_settings['page_size']
    ].to_dict('rows')


@app.callback(
    Output('graph-container',"children"),
    [Input('table',"data")])

def update_graph(rows):
    global dff
    dff = pd.DataFrame(rows)
    dff['Date Time'] = pd.to_datetime(dff['Date Time'],format="%d-%m-%Y %H:%M:%S")
    return html.Div(
            dcc.Graph(
                id = "graph",
                 figure= {
                    'data':[go.Scatter(
                        x = dff['Date Time'],
                        y = dff['SNC-ID'],
                            mode = 'markers',
                            text=dff['Node'],

                            marker = dict(       #Change the marker style
                                        size = 12,
                                        color = 'rgb(18,98,188)',
                                        symbol='circle',
                                        line =dict(
                                                width =2,
                                                    )
                                         )
                         )
                    ],
                    'layout':go.Layout(
                        title='SNC Data Visualization',
                        xaxis=dict(title='Date Time'),
                        #yaxis=dict(title='SNC'),
                        hovermode='closest'
                        )
                    }
                 )
        )

if __name__ == '__main__':
    app.run_server(debug=True)