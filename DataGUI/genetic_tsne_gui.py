from tkinter import Tk, Label, Button, Frame


class Genetic_Tsne_GUI:
    def __init__(self, master):
        self.master = master
        master.title = ("Genetic TSNE Training and Evaluation")

        self.window = Frame(master , width=800, height=600)
        self.window.pack()

        self.train_button = Button(master , text="Train a Generation of Networks" , command=self.print_clicked)
        self.train_button.pack()

        self.test_button = Button(master, text="Test a Trained Model" , command = self.print_clicked)
        self.test_button.pack()

        self.report_button = Button(master, text="Generate Reports" , command=self.print_clicked)
        self.report_button.pack()

        self.viz_button = Button(master, text="Generate Visualizations" , command=self.print_clicked)
        self.report_button.pack()

        self.quit_button = Button(master , text="Quit Application" , command=master.quit)
        self.quit_button.pack()

    def print_clicked(self):
        print("clicked")

class BreedFrame:
    def __init__(self, master):
        self.master = master

    self.testBtn = Button(master , text="BreedFrameBtn" , command=self.print_clicked)
    self.testBtn.pack()

    def print_clicked(self):
        print("testbnt clicked")


root = Tk()
app = Genetic_Tsne_GUI(root)
root.mainloop()
