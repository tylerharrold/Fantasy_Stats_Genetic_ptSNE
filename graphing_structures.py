# Script for drawing visual representations of the neural network tests
from graphics import *
from training_structure_visualization import get_test_structure_report
from pathlib import Path

# used for testing
class BoundingBox:
    def __init__(self , x , y , bound_width , bound_height , num):
        self.num = num
        self.bound_upper_left = Point(x , y)
        self.bound_lower_right = Point(x + bound_width , y + bound_height)
        self.text_anchor = Point(x + bound_width / 2 , y + bound_height / 2)

    def draw(self, win):
        rect = Rectangle(self.bound_upper_left , self.bound_lower_right)
        text = Text(self.text_anchor , 'bound box ' + str(self.num))
        rect.draw(win)
        text.draw(win)

class LayerBar:
    def __init__(self , x , y , bound_width, bound_height , unit_size , color='blue'):
        self.color = color
        self.upper_left_point = Point(x + bound_width / 2 - unit_size / 2 , y)
        self.lower_right_point = Point(x + bound_width / 2 + unit_size / 2 , y + bound_height)

    def draw(self , win):
        rect = Rectangle(self.upper_left_point , self.lower_right_point)
        rect.setFill(self.color)
        rect.draw(win)

class Network:
    def __init__(self ,  x , y , pixel_width , pixel_height , perplexity , network_structure , buffer_pixels = 5 , max_layers=8):
        self.x = x
        self.y = y
        self.max_x = x + pixel_width - buffer_pixels
        self.min_y = y + buffer_pixels
        self.min_x = x + buffer_pixels
        self.max_y = y + pixel_height - buffer_pixels
        self.pixel_width = pixel_width
        self.pixel_height = pixel_height
        self.perplexity = str(perplexity)
        self.network = network_structure
        self.number_of_bars = len(self.network)
        self.max_layers = max_layers
        self.draw_objects = []
        self.setup()

    def setup(self):
        max_height_pixels = self.max_y - self.min_y
        num_divisions = self.max_layers + 1
        unit = (self.max_x - self.min_x) / num_divisions
        midpoint = Point(self.x + self.pixel_width / 2 , self.y + self.pixel_height / 2)
        line = Line(Point(self.min_x , midpoint.y) , Point(self.max_x , midpoint.y))
        self.draw_objects.append(line)
        in_circle = Circle(Point(self.min_x + unit / 4  , midpoint.y) , unit / 4)
        in_circle.setFill("black")
        out_circle = Circle(Point(self.max_x - unit / 4 , midpoint.y) , unit / 4)
        out_circle.setFill("black")
        x_start = self.min_x + unit / 2
        bound_width = self.max_layers * unit / len(self.network)
        self.draw_objects.append(in_circle)
        for layer_num , percentage_height in enumerate(self.network):
            x_offset = x_start + layer_num * bound_width
            #bound_box = BoundingBox(x_offset , self.min_y , bound_width , max_height_pixels , layer_num)

            bar_height = max_height_pixels * percentage_height
            y_offset = midpoint.y - bar_height / 2
            new_bar = LayerBar(x_offset , y_offset , bound_width , bar_height , unit)

            #self.draw_objects.append(bound_box)
            self.draw_objects.append(new_bar)
        self.draw_objects.append(out_circle)

    def draw(self , win):
        for go in self.draw_objects:
            go.draw(win)
        perp_text = Text(Point(self.x +  10, self.y + 10) , str(self.perplexity))
        perp_text.draw(win)


#TEST METHOD
def test():
    win = GraphWin("My Circle" , 500 , 500)
    t = [50, [614, 563, 1440, 1902]]
    mxm = max(t[1])
    t[1] = [i / mxm for i in t[1]]
    test_network = Network(0 , 0 , 500 , 500 , t[0] , t[1])
    test_network.draw(win)
    win.getMouse()
    win.close()


# simple function for drawing a neural network as a concept
def test_draw_network(window_width , window_heigh , perplexity , network_structure):
    win = GraphWin("Test Network Draw" , window_width , window_heigh)
    # get layer count
    num_layers = len(network_structure)
    # normalize data
    mxm = max(network_structure)
    normalized = [i / mxm for i in network_structure]



# function to test drawing a full generation
def test_draw_generation():
    test_dir = Path.cwd() / 'TestData' / "normalized_combine_30_40_half_auc"
    gen_data = get_test_structure_report(test_dir)
    generation_1 = gen_data[0]
    generation_1 = [[x[1] , x[2]] for x in generation_1]

    # normalize gen layer sizes
    max = generation_1[1][0]
    for perplexity , structure in generation_1:
        for size in structure:
            if size > max:
                max = size

    for index, child in enumerate(generation_1):
        working_list = child[1]
        norm = list(map(lambda x: x / max , working_list))
        generation_1[index][1] = norm

    # begin to draw
    win = GraphWin("Test Generation Draw" , 612 , 792)
    x = 0
    y = 0
    cols = 5
    rows = 6
    box_width = 612 / cols
    box_height = 792 / rows
    networks = []
    for child_num , child in enumerate(generation_1):
        xstart = x + (box_width * (child_num % cols))
        ystart = y + box_height * (child_num // cols)
        print(str(xstart) , ',' , str(ystart))
        new_network = Network(xstart , ystart , box_width , box_height , child[0] , child[1])
        networks.append(new_network)

    for network in networks:
        network.draw(win)
    win.getMouse()
    win.close()


if __name__ == "__main__":
    test_draw_generation()
