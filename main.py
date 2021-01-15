from tkinter import *
import random

class CGL(Frame):

	def __init__(self, parent):
		Frame.__init__(self, parent)
		self.parent = parent
		self.grid(column=0, row=0)
		self.configure(height=600, width=600)
		self.paused = True

		self.CELL_SIZE = 20
		self.CANVAS_DIM = (600, 400)
		self.COLS = self.CANVAS_DIM[0] // self.CELL_SIZE
		self.ROWS = self.CANVAS_DIM[1] // self.CELL_SIZE

		#INITIALIZE CELLS
		self.cells = [[0] * self.COLS for i in range(self.ROWS)]

		# RANDOMLY ADD CELLS
		for i in range(200):
			rx = random.randint(0, self.COLS-1)
			ry = random.randint(0, self.ROWS-1)
			self.cells[ry][rx] = 1

		self.buildUI()
			
	def clear_cells(self):
		self.cells = [[0] * self.COLS for i in range(self.ROWS)]
		self.draw_cells(False)

	def buildUI(self):
		# MAKE BUTTON BAR
		button_bar = Frame(self, padx=10, pady=10)
		button_bar.grid(column=0, row=0)
			
		gen = Button(button_bar, text="gen", command=self.gen)
		gen.grid(column=0, row=0)

		clear = Button(button_bar, text="clear", command=self.clear_cells)
		clear.grid(column=1, row=0)

		self.play = Button(button_bar, text="play", command=self.pp)
		self.play.grid(column=2, row=0)

		# MAKE CANVAS/GRID CONSTRUCT
		self.canvas = Canvas(self, width=self.CANVAS_DIM[0], height=self.CANVAS_DIM[1], bg="white")
		self.canvas.grid(column=0, row=1)
		self.canvas.bind("<Button-1>", self.canvas_click)
		self.draw_grid()
		self.draw_cells(False)

	def canvas_click(self, event):
		row = event.x // self.CELL_SIZE
		col = event.y // self.CELL_SIZE
		self.cells[col][row] = self.cells[col][row] ^ 1
		self.draw_cells(False)

	def pp(self):
		if self.paused:
			self.play.configure(text="pause")
			self.paused = False
			self.draw_cells(True)
		else:
			self.play.configure(text="play")
			self.paused = True

	def gen(self):
		rand_cells = [[0] * self.COLS for i in range(self.ROWS)]

		# RANDOMLY ADD CELLS
		for i in range(200):
			rx = random.randint(0, self.COLS-1)
			ry = random.randint(0, self.ROWS-1)
			rand_cells[ry][rx] = 1
		
		self.cells = rand_cells

		self.draw_cells(False)

	def draw_grid(self):
		self.canvas.create_rectangle(0, 0, self.CANVAS_DIM[0], self.CANVAS_DIM[1], fill="white")
		for i in range(0, self.CANVAS_DIM[0], self.CELL_SIZE):
			self.canvas.create_line(i, 0, i, self.CANVAS_DIM[1])

		for i in range(0, self.CANVAS_DIM[1], self.CELL_SIZE):
			self.canvas.create_line(0, i, self.CANVAS_DIM[0], i)

	def draw_cells(self, animate=True):
		self.draw_grid()
		sc = self.cells
		for i in range(len(sc)):
			y_pos = i * self.CELL_SIZE
			for j in range(len(sc[0])):
				x_pos = j * self.CELL_SIZE
				if sc[i][j] == 1:
					self.canvas.create_rectangle(x_pos, 
						y_pos, 
						x_pos + self.CELL_SIZE, 
						y_pos + self.CELL_SIZE,
						fill="yellow"
					)
	
		if animate and not self.paused:
			self.simulate()

	def simulate(self):
		#ADD SIMULATION LOGIC
		new_cells = [[0] * self.COLS for i in range(self.ROWS)]
		for i in range(len(self.cells)):
			for j in range(len(self.cells[0])):
				curr_n = self.getN(i, j)
				alive = self.cells[i][j] == 1
				if alive:
					if curr_n < 2:
						new_cells[i][j] = 0
					elif curr_n in [2, 3]:
						new_cells[i][j] = 1
					elif curr_n > 3:
						new_cells[i][j] = 0
				else:
					if curr_n == 3:
						new_cells[i][j] = 1
		self.cells = new_cells
		root.after(100, self.draw_cells)
				
		
	def getN(self, x, y):
		c = self.cells
		n = 0
			
		for i in range(-1, 2):
			for j in range(-1, 2):
				if not(i == 0 and j == 0):
					curr_x = x + i
					curr_y = y + j
					if curr_x >= 0 and curr_x <= (self.ROWS-1) \
						and curr_y >= 0 and curr_y <= (self.COLS-1) \
						and c[curr_x][curr_y] == 1:
							n+=1
												

		return n

root = Tk()
game = CGL(root)
root.mainloop()

