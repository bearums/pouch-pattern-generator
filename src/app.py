from bag_plot import initialise_bag_plot, update_bag_plot
from pattern_plot import update_pattern_plot, find_theta, initialise_pattern_plot
from dash import Dash, dcc, html, Input, Output, callback, State
from dash import callback_context
from math import pi
#initial parameters of pounch
height = 12
top_width = 16
bottom_width = 14
depth = 8
button_val = 0

theta_init = find_theta(height, top_width, bottom_width, depth, 0, pi)



fig_pattern = initialise_pattern_plot()

fig_bag = initialise_bag_plot()


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)
#app = Dash(__name__)

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server

label_style= {"padding": "10px 10px"}
app.layout = html.Div( [
html.Div([
        html.Div("height/cm", style= label_style),
        dcc.Slider(id='height-slider',
                   min=4,
                   max=30,
                   step=1,
                   value=height,
                   marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode = 'mouseup',
        ),
        html.Div("top width/cm", style= label_style),
        dcc.Slider(
                   id='top-width-slider',
                   min=5,
                   max=30,
                   step=1,
                   value=top_width,
                   marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode = 'mouseup'
        ),
        html.Div("bottom width/cm", style= label_style),
        dcc.Slider(
                   id='bottom-width-slider',
                   min=5,
                   max=30,
                   step=1,
                   value=bottom_width,
                   marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode = 'mouseup'
        ),
        html.Div("bottom depth/cm", style= label_style),
        dcc.Slider(
                   id='depth-slider',
                   min=1,
                   max=20,
                   step=1,
                   value=depth,
                   marks=None,
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode = 'mouseup'
        ),
         html.Button('Submit', id='button', n_clicks=0)
     ],style={'width': '30%', 'display': 'inline-block', 'float':'left'}),
     html.Div( dcc.Graph(figure=fig_bag, 
                         id='3dplot',
                         style={'width': '40%', 'float': 'left', 'display': 'inline-block'})), 
     html.Div( dcc.Graph(figure=fig_pattern, 
                         id='pattern_plot',
                         style={'width': '80%', 'float': 'left', 'display': 'flex'}, 
                         config={"staticPlot":False}))
])

@callback(
    Output('3dplot', 'figure'), 
    Output('pattern_plot', 'figure'), 
    
    Input('height-slider', 'value') , 
    Input('top-width-slider', 'value'),
    Input('bottom-width-slider', 'value'),
    Input('depth-slider', 'value'),
    Input('button', 'n_clicks'),
    )




def update_chart(height, top_width, bottom_width, depth,button, theta_init=theta_init, fig_bag=fig_bag, fig_pattern=fig_pattern):
    theta_new = find_theta(height, top_width, bottom_width, depth, 0.5*theta_init, 1.5*theta_init)
    fig_bag=update_bag_plot(height, top_width, bottom_width, depth, fig_bag)
    
    
   
    global button_val
    #print(button_val, button)
    if button>button_val:
        button_val = button
        fig_pattern = update_pattern_plot(height, top_width, bottom_width, depth, theta_new,fig_pattern)
    elif fig_pattern.data !=[] :
        fig_pattern.data = []
    return fig_bag, fig_pattern

if __name__ == '__main__':
    app.run(debug=True, port = 8053) 

