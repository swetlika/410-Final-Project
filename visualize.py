from bokeh.layouts  import row, column
from bokeh.plotting import figure, curdoc
from bokeh.models   import LinearAxis, Range1d, Div
from bokeh.driving  import count
import random

# hello.py 

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models.widgets import TextInput, Button, Paragraph
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import PreText, Select
from bokeh.plotting import reset_output

from bokeh.io import output_file, show
from bokeh.layouts import widgetbox
from bokeh.models.widgets import Dropdown

from os.path import dirname, join

# setup
# Make sure these variables are consistent with streaming.py
#tickers = ['TSLA','SNAP','AAPL','AMZN','UAL']
ticker = ''
refresh = 5
#path = "/Users/mrudulavysyaraju/Desktop/410-Final-Project/data"
path = "/home/nila/Projects/410-Final-Project/data"

# create some widgets
output_file("dropdown.html")

menu = [('--Companies--','--Companies--'),
        ('Amazon','AMZN'),
        ('Apple','AAPL'),
        ('Facebook','FB'),
        ('Google','GOOGL'),
        ('IBM','IBM'),
        ('Microsoft','MSFT'),
        ('Nvidia','NVDA'),
        ('Snapchat','SNAP'),
        ('Tesla','TSLA'),
        ('Uber','UBER'),
        ('Yahoo','YHOO')]

tickers = [x[0] for x in menu]

#dropdown = Dropdown(label="Companies", button_type="warning", menu=menu)
dropdown = Select(value='--Companies--', options=tickers) 
def input_handler(attr,old,new):
    update()

dropdown.on_change('value', input_handler)
#dropdown.on_click(input_handler)

show(widgetbox(dropdown))
content_filename = join(dirname(__file__), "description.html")
description = Div(text=open(content_filename).read(),
                  render_as_text=False, width=600)
output = Paragraph(text="""""",
width=200, height=100)

# add a callback to a widget
def update():
    ticker = dropdown.value
    plot = []
    visualize(ticker, refresh, path, plot)
#button.on_click(update)

# create a layout for everything
layout = column(description, dropdown, output)

# add the layout to curdoc
curdoc().add_root(layout)

#def readUpdates(filename):
#    updates = {}
#    with open(filename, 'r') as infile:
#        for line in infile:
#            l = line.strip('\n').split(',')
#            volume = int(l[1])
#            sentiment = 0
#            if l[2] != 'N/A': sentiment = float(l[2])
#            updates[l[0]] = (volume, sentiment)
#    return updates

def readUpdates(filename):
    updates = {}
    with open(filename, 'r') as infile:
        for line in infile:
            l = line.strip('\n').split(',')
            volume = int(l[1])
            sentiment = 0
            if l[2] != 'N/A': sentiment = float(l[2])
            #updates[l[0]] = (volume, sentiment)
            updates[l[0]] = (sentiment)
    return updates


def extrapolate(tweets):
    return tweets*99+random.randint(0,99)

def getPlot(title):
    p = figure(plot_height=400, plot_width=800, min_border=40, toolbar_location=None, title=title, y_axis_label='Sentiment Value', x_axis_label='Time', y_range=(-1,1))
    p.background_fill_color = "#2e484c"          # Background color
    p.title.text_color = "#660066"               # Title color
    p.title.text_font = "helvetica"              # Title font
    p.x_range.follow = "end"                     # Only show most recent window of data
    p.x_range.follow_interval = 60               # Moving window size
    p.xaxis.major_tick_line_color = None         # Turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None         # Turn off x-axis minor ticks
    p.yaxis.major_tick_line_color = None         # Turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None         # Turn off y-axis minor ticks
    p.xgrid.grid_line_alpha = 0                  # Hide X-Axis grid
    p.ygrid.grid_line_alpha = 0                  # Hide Y-Axis grid
    p.xaxis.major_label_text_color = "#660066"   # X-Axis color
    p.yaxis.major_label_text_color = "#660066"   # Y-Axis color
    #p.extra_y_ranges = {"sentiment": Range1d(start=-1, end=1)}
    #p.add_layout(LinearAxis(y_range_name="sentiment", major_tick_line_color = None, minor_tick_line_color = None), 'left')
    return p

def visualize(coins, seconds, path, plot):
    ms = seconds*1000

    plot.append(getPlot(coins))
    plot.append(plot[0].line([], [], line_alpha = 0.7, color="#66ffff", line_width=3))
    plot.append(plot[1].data_source)

    rows = []
    
    @count()
    def update(t):
        #Grab updates
        updates = readUpdates('%supdates.txt' % path)

        plot[2].data['x'].append(t)
        plot[2].data['y'].append(updates[coins])
        plot[2].trigger('data', plot[2].data, plot[2].data)
        

    

    #rows.append(row(plot[0]))
    main_row = row(plot[0])
    root = column(main_row)

    #root = column([r for r in rows])
    curdoc().add_root(root)
    curdoc().add_periodic_callback(update, ms)


'''
Steps to run local bokeh server
1. Make sure streaming.py is running...
2. Traverse in console to the directory containing visualize.py
3. python -m bokeh serve --show visualize.py
'''

# Note: Volume is the thick blue line while sentiment is the thin white line
