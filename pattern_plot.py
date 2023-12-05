import plotly.graph_objects as go
from math import atan2, sqrt,pi, cos, sin
import numpy as np

patternplot_template = dict(
    layout=go.Layout( showlegend =False,
                        scene_aspectmode='data',
                        width=300,    
                        height=500, 
                        plot_bgcolor = "white",
                        )
)

def my_bisection(f, a, b, tol): 
    # approximates a root, R, of f bounded 
    # by a and b to within tolerance 
    # | f(m) | < tol with m the midpoint 
    # between a and b Recursive implementation
    
    # check if a and b bound a root
    if np.sign(f(a)) == np.sign(f(b)):
        raise Exception("The scalars a and b do not bound a root")
        
    # get midpoint
    m = (a + b)/2
    
    if np.abs(f(m)) < tol:
        # stopping condition, report m as root
        return m
    elif np.sign(f(a)) == np.sign(f(m)):
        # case where m is an improvement on a. 
        # Make recursive call with a = m
        return my_bisection(f, m, b, tol)
    elif np.sign(f(b)) == np.sign(f(m)):
        # case where m is an improvement on b. 
        # Make recursive call with b = m
        return my_bisection(f, a, m, tol)
        
def find_theta(height, top_width, bottom_width, depth, theta_guess_low, theta_guess_hi ):
    #calculate theta
    e = 0.5*top_width
    c = 0.5*bottom_width
    b = height
    d = height + 0.5*depth
    a= 0.5*depth
    
    res =lambda theta: b*cos(theta) + a*sin(theta) +c - e
    theta=my_bisection(res, theta_guess_low, theta_guess_hi, 1e-4)
    return theta
    
def calc_points(height, top_width, bottom_width, depth, theta):

    x = 0.5*depth*cos(theta - 0.5*pi)
    pattern_points = {'A':[0,0],
                 'B': [0.5*bottom_width,0],
                 'C': [0.5*bottom_width, 0.5*depth],
                 #'D': [0.5*bottom_width+x, 0.5*depth],
                 'E': [0.5*bottom_width+ (0.5*depth)*cos(theta-0.5*pi), 0.5*depth+ (0.5*depth)*sin(theta-0.5*pi) ],
                 'F': [0.5*top_width,height + 0.5*depth],
                 'G': [0,height + 0.5*depth]}
                 
    side_lengths = {'AB':0.5*bottom_width, 
                    'BC':  0.5*depth, 
                    'CE': None,
                    'EF': None,
                    'FG': 0.5*top_width,
                    'GA': height + 0.5*depth}             
    return {"pattern_points":pattern_points, "side_lengths":side_lengths, "theta":theta}

def make_pattern_plot(height, top_width, bottom_width, depth, theta):
    #break up into smaller functions
    # 1) plot lines
    # 2) plot dimensions
    fig_pattern = go.Figure()
    
    #plot lines of pattern
    calc_res= calc_points(height, top_width, bottom_width, depth, theta)
    pattern_points= calc_res['pattern_points']
    side_lengths= calc_res['side_lengths']
    ys = np.array([q[0] for q in pattern_points.values()])
    xs = np.array([q[1] for q in pattern_points.values()])
    fig_pattern.add_trace(go.Scatter(x=xs[-2:], y =ys[-2:] , line={'color':'black'})) # plot zipper side in black
    fig_pattern.add_trace(go.Scatter(x=xs[:-1], y =ys[:-1] , line={'color':'blue'})) 
    fig_pattern.add_trace(go.Scatter(x=[xs[0],xs[-1]], y =[ys[0],ys[-1]], line={'color':'blue'})) 
   
     
    # write line dimensions
    text_paddings = [(0.1, 0),(0, 0.1),(0,0),(0,0),(-0.35, -.3),(0, 0.2)   ] # for moving text away from line a bit
    txt_pos_x =[]
    txt_pos_y = []
    txt_list = []
    for i in range(0,len(pattern_points)-1):
        xa = xs[i]
        xb = xs[i+1]
        ya = ys[i]
        yb = ys[i+1]
        #print(i, text_paddings[i][0], text_paddings[i][1])
        x_ = 0.5*(xa + xb) + text_paddings[i][0]
        y_ = 0.5*(ya + yb) + text_paddings[i][1]
        txt_pos_x.append(x_)
        txt_pos_y.append(y_)
        txt = list(side_lengths.values())[i]
        txt_list.append(txt)
    txt_pos_x.append((xs[-1]+ xs[0])*0.5 + text_paddings[-1][0])
    txt_pos_y.append((ys[-1]+ ys[0])*0.5 + text_paddings[-1][1])
    txt_list.append(list(side_lengths.values())[-1])
    fig_pattern.add_trace(go.Scatter(x=txt_pos_x, y=txt_pos_y, mode='text', text = txt_list, textposition="top right"))


    #make triangle for angled section
    fig_pattern.add_trace(go.Scatter(x=[pattern_points['C'][1], pattern_points['C'][1],pattern_points['E'][1]],
                                     y=[pattern_points['C'][0],pattern_points['E'][0],pattern_points['E'][0]],
                                    mode='lines', 
                                    text = txt, 
                                    textposition="top right",  
                                    line=dict(color='firebrick', 
                                    width=2,
                              dash='dash')))
                                         
    text_padding_dotted_lines = (-0.1, -0.3)
    #label for vertical line
    txt = "%.2f"%abs(-pattern_points['C'][0]+pattern_points['E'][0])
    fig_pattern.add_trace(go.Scatter(x=[pattern_points['C'][1]+text_padding_dotted_lines[0]], 
                                     y=[(pattern_points['C'][0]+pattern_points['E'][0])*0.5], 
                                     mode='text', 
                                     text = txt, 
                                     textposition="top left"  ))         
    #label for horizontal line
    txt = "%.2f"%abs(-pattern_points['C'][1]+pattern_points['E'][1])
    fig_pattern.add_trace(go.Scatter(x=[(pattern_points['C'][1] + pattern_points['E'][1])*0.5], 
                                     y=[text_padding_dotted_lines[1]+pattern_points['E'][0]], 
                                     mode='text', 
                                     text = txt, 
                                     textposition="bottom center"  ))                    
                              
    # add central text with explanation
    explanation_pos = ((max(xs)+ min(xs)) *0.5, (max(ys)+ min(ys)) *0.1)
    txt = "<b>Seam allowance not included <br><br> All measurements in cm <br><br> Zip sewn onto black line"
    fig_pattern.add_trace(go.Scatter(x=[explanation_pos[0]], 
                                     y=[explanation_pos[1]], 
                                     mode='text', 
                                     text = txt, 
                                     textposition="top center" ,
                                     textfont_size=20 ))                    
            
    
    # format plot
    #fig_pattern.update_layout(scene_aspectmode='data',width=800,    height=500, plot_bgcolor = "white")
    fig_pattern.update_layout( template=patternplot_template)
    fig_pattern.update_xaxes(showgrid=False,
                             gridcolor='LightPink', 
                             gridwidth=0.5, 
                             showticklabels=True,  
                             dtick=1, 
                             range =[-0.5, max(xs)+0.5],
                             scaleratio = 1)
    fig_pattern.update_yaxes(
    #scaleanchor = "x",
    scaleratio = 1,
    showgrid=False,gridcolor='LightPink', gridwidth=0.5,
    showticklabels =True , dtick=1,
    range = [-0.5, max(ys)+0.5]
    )

    return fig_pattern