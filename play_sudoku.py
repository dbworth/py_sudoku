
###########################
#                         #
#  Graphical Sudoku Game  #
#                         #
###########################

from Tkinter import *
from sudoku import *
import tkFileDialog

import platform
if platform.system() == 'Windows':
    small_font = ("Courier New", "10", "bold")
    large_font = ("Courier New", "21", "bold")
else:
    small_font = ("Courier New", "10", "bold")
    large_font = ("Courier New", "25", "bold") 

box_size = 50
half = box_size/2


class NumberButtons(Frame):
    """ A frame containing the 9 choice buttons """
    def __init__(self, parent):
        Frame.__init__(self, parent, relief=SUNKEN, bg = "grey")
        self.buttons = []
        self.current = IntVar()
        for i in range(1,10):
            bi = Radiobutton(self, text = str(i), value = i, 
                             variable = self.current,
                             indicatoron=0,
                             font = large_font, fg = "red",
                             selectcolor="yellow")
            bi.pack(side=TOP,ipadx = 4,pady = 3)
            self.buttons.append(bi)
        self.current.set(1)

    def get_current(self):
        """ Return the current choice """
        return self.current.get()


button_offset = 20
big_line_width = 3
shift = big_line_width

class Controller():
    """The controller for the app."""
    def __init__(self, master):
        self.master = master
        self.model = None
        self.filename = None
        self.show_choices = False
        # the game board widget
        self.view = View(master, self)
        self.view.pack(fill=BOTH, side=LEFT)
        self.view.canvas.bind("<Button-1>", self.mousePress)
        # the number buttons
        self.numberbuttons = NumberButtons(master)
        self.numberbuttons.pack(fill=BOTH,side=LEFT, padx = 20, pady = 20)
        # the command buttons
        self.commands = Commands(master, self)
        self.commands.pack(side=LEFT, fill=BOTH, pady=185, padx=20)
        # File menu
        self.menubar = Menu(master)
        master.config(menu=self.menubar)
        self.filemenu = Menu(self.menubar)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open Game",
                                  command=self.openGame)
        self.filemenu.add_command(label="Exit", command=self.exitApp)
        self.auto_fill = False

    # Not needed 
    def getCanvas(self):
        """ Get the canvas widget """
        return self.boardwidget.canvas

    # Not needed
    def getStatus(self):
        """ Get the status label widget """

        return self.boardwidget.status_label

    def getModel(self):
        """ Get the model """

        return self.model

    def getVal(self, r, c):
        """Get the value in row r, column c"""
        return self.model[r,c]

    def getChoices(self, r, c):
        """Get the choices in row r, column c"""
        return self.model.choices(r,c)

    def getGameStatus(self):
        """Get the status of the game"""
        return self.model.game_status()

    def openGame(self):
        """ Open a new game file and create the corresponding model """
        filename = tkFileDialog.askopenfilename()
        if filename:
            self.filename = filename
            self.model = Sudoku(filename, self.auto_fill)
            self.redraw()

    # This is used to stop interaction if game is not loaded
    # Not required for the assignment
    def loaded(self):
        """ Is a game currently loaded? """
        return self.model != None

    def mousePress(self, event):
        """ The mouse press even on the canvas """
        if not self.loaded():
            return
        # the row and column position of the choice
        column = (event.x - shift) / box_size
        row = (event.y - shift)/ box_size
        choices = self.model.choices(row, column)
        # the second part of test below not required for assignment
        if len(choices) == 1 and self.show_choices:
            pick = choices[0]
        else:
            pick = str(self.numberbuttons.get_current())
        if pick in choices:
            self.model[row, column] = pick
            self.redraw()

    def flip_choice_flag(self):
        """ Flip between showing choices and not showing choices """
        self.show_choices = not self.show_choices
        self.redraw()
        return self.show_choices

    def flip_af(self):
        """ Flip between auto filling and not auto filling """
        if self.loaded():
            self.auto_fill = self.model.flip_af()
            return self.auto_fill
        else:
            return False

    def undo(self):
        """ Undo the last move """
        if self.model:
            self.model.undo()
            self.redraw()

    def redraw(self):
        """ Redraw the game info """
        if self.loaded():
            self.view.redraw(self.show_choices)

    def exitApp(self):
        self.master.destroy()


class View(Frame):
    """The game view class.

    Constructor: View(controller)
    """
    def __init__(self, parent, controller):
        self.controller = controller
        Frame.__init__(self, parent, relief=SUNKEN, bd=2, bg = "grey")
        self.show_choices = False
        size = box_size*9+big_line_width
        self.canvas = Canvas(self, bd=0, height = size,width= size, 
                             bg = 'white')
        self.canvas.pack(fill=BOTH, padx = 20, pady = 20)
        self.status_label = Label(self, text = "", bg = "grey", fg="red", 
                                  font=large_font)
        self.status_label.pack(pady = 20)
        # draw the grid lines
        for i in range(10):
            line_width = (i%3) and 1 or big_line_width
            half_lw = line_width/2
            line_offset = shift + i*box_size - half_lw
            line_len = size
            self.canvas.create_line(line_offset,0,
                                    line_offset,
                                    line_len,
                                    width = line_width)
            self.canvas.create_line(0, line_offset,
                                    line_len,
                                    line_offset,
                                    width = line_width)

    def offset(self, box):
        """ Return the offset for drawing text at a given position """
        return box*box_size+half+shift

    def redraw(self, show_choices):
        """Redraw view.

        Precondition: a game is loaded
        """
        canvas = self.canvas
        canvas.delete('entry')
        for r in range(9):
            for c in range(9):
                val = self.controller.getVal(r,c)
                if val == ' ':
                    if show_choices:
                        # display the choices for the cell
                        choices = self.controller.getChoices(r,c)
                        val = ''.join(choices)
                        canvas.create_text(self.offset(c), self.offset(r), 
                                           text = val, fill="blue", 
                                           font= small_font, 
                                           tags = 'entry')
                else:
                    # display the value of this cell
                    canvas.create_text(self.offset(c), self.offset(r), 
                                       text = val, fill="red", 
                                       font= large_font, 
                                       tags = 'entry')
        # update the status label text
        self.status_label.config(text=self.controller.getGameStatus())


class Commands(Frame):
    """ A frame containing the 2 'command' buttons """
    def __init__(self, parent, controller):
        Frame.__init__(self, bg = "grey")
        self.controller =  controller
        self.do_fill = False
        self.choices = Button(self, text = "Show Choices", 
                              command=self.flipChoices)
        self.choices.pack(side=TOP,fill=X)
        self.af = Button(self, text = "Auto Fill", 
                              command=self.autofill)
        self.af.pack(side=TOP,fill=X,pady=20)
        self.undo = Button(self, text = "        Undo        ", 
                           command=self.undo)
        self.undo.pack(side=TOP,fill=X)
 
    def flipChoices(self):
        """ callback when choices button is pressed """
        if self.controller.flip_choice_flag():
            self.choices.config(text="Hide Choices")
        else:
            self.choices.config(text="Show Choices")

    def autofill(self):
        """ callback when the auto fill button is pressed """
        if self.controller.flip_af():
            self.af.config(text="No Auto Fill")
        else:
            self.af.config(text="Auto Fill")

    def undo(self):
        """ callback when undo button is pressed """
        self.controller.undo()

class SudokuApp():
    """ The Sudoku application """
    def __init__(self, master=None):
        master.title("Sudoku")
        master.config(bg = "grey")
        master.resizable(0,0)
        self.controller = Controller(master)


root = Tk()
app = SudokuApp(root)
root.mainloop()

