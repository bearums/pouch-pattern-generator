import plotly.graph_objects as go

bagplot_template = dict(
    layout=go.Layout( width=500,    height=400, scene = dict(
        xaxis = dict(visible=False),
        yaxis = dict(visible=False),
        zaxis =dict(visible=False),
        aspectmode="data"
        ),
        margin=dict(
        l=10,
        r=10,
        b=10,
        t=10,
        pad=0
    ),
     autosize=True)
)

def initialise_bag_plot():
    fig = go.Figure()
    fig.update_layout( template=dict(
                                    layout=go.Layout( width=500,    height=400, 
                                                     scene = dict(
                                                                    xaxis = dict(visible=False),
                                                                    yaxis = dict(visible=False),
                                                                    zaxis =dict(visible=False),
                                                                    aspectmode="data"
                                                                    ),
                                                                    margin=dict(
                                                                    l=10,
                                                                    r=10,
                                                                    b=10,
                                                                    t=10,
                                                                    pad=0
                                                                ),
                                                                autosize=True)
                                                            )
                        )
    fig.update_layout(uirevision='constant') # do not reset camera view
    return fig


def update_bag_plot(height, top_width, bottom_width, depth, fig):

     #clear plot of all lines
    fig.data = []


    points = [[0.5*top_width,0, height], [-0.5*top_width, 0,height],
         [-0.5*bottom_width,  0.5*depth,0] ,[-0.5*bottom_width, -0.5*depth,0],
         [0.5*bottom_width, -0.5*depth,0],[0.5*bottom_width,  0.5*depth,0]]

    col='black'
    
    for points_ in [points, [points[1],points[3]],[points[0],points[-1]], [points[0],points[-2]],[points[2],points[-1]]]:
        fig.add_trace(go.Scatter3d(x=[p[0] for p in points_], 
                                    y= [p[1] for p in points_], 
                                    z= [p[2] for p in points_],
                                    mode='lines',
                                    line=dict(
                                            color=col,
                                            width=2),
                                    showlegend=False))
         

    return fig
    
