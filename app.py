from bag_plot import make_plot
from pattern_plot import make_pattern_plot
from dash import Dash, dcc, html, Input, Output, callback


#parameters of pounch
height = 12
top_width = 16
bottom_width = 14
depth = 8


#TODO
# print dimensions on pattern piece 
# set autosizing of plots
# arrange items better


fig_pattern = make_pattern_plot(height, top_width, bottom_width, depth)

fig = make_plot(height, top_width, bottom_width, depth)



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
#app = Dash(__name__)

label_style= {"padding": "20px 40px 15px"}
app.layout = html.Div( [

html.Div([
        html.Div("height/cm", style= label_style),
        dcc.Slider(id='height-slider',
                   min=0,
                   max=20,
                   step=0.5,
                   value=height,
                   marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode = 'drag',
        ),
        html.Div("top width/cm", style= label_style),
        dcc.Slider(
                   id='top-width-slider',
                   min=0,
                   max=20,
                   step=0.5,
                   value=top_width,
                   marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode = 'drag'
        ),
        html.Div("bottom width/cm", style= label_style),
        dcc.Slider(
                   id='bottom-width-slider',
                   min=0,
                   max=20,
                   step=0.5,
                   value=bottom_width,
                   marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode = 'drag'
        ),
        html.Div("bottom depth/cm", style= label_style),
        dcc.Slider(
                   id='depth-slider',
                   min=0,
                   max=20,
                   step=0.5,
                   value=depth,
                   marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode = 'drag'
        )
     ],style={'width': '30%', 'display': 'inline-block', 'float':'left'}),
     html.Div( dcc.Graph(figure=fig, id='3dplot',style={'width': '65%', 'float': 'left', 'display': 'inline-block'})), 
     html.Div( dcc.Graph(figure=fig_pattern, id='pattern_plot',style={'width': '80%', 'float': 'left', 'display': 'inline'}, config={"staticPlot":False}))
])

@callback(
    Output('3dplot', 'figure'), 
    Output('pattern_plot', 'figure'), 
    Input('height-slider', 'value') , 
    Input('top-width-slider', 'value'),
    Input('bottom-width-slider', 'value'),
    Input('depth-slider', 'value')
    )
def update_chart(height, top_width, bottom_width, depth):
    #print("height = %s \n top width = %s"%(height, top_width))
    fig=make_plot(height, top_width, bottom_width, depth)
    fig_pattern = make_pattern_plot(height, top_width, bottom_width, depth)
    return fig, fig_pattern

if __name__ == '__main__':
    app.run(debug=True, port = 8053)
