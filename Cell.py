class Cell:
    def __init__(self, type, row_num, col_num):
        self.type = type
        self.row_num = row_num
        self.col_num = col_num
        self.name = self.type + str(self.row_num) + str(self.col_num)
        self.value = None
        self.domain = []
        self.copyOfDomain = []
        self.row_constraint = None
        self.col_constraint = None
        self.row_neighbors = []
        self.col_neighbors = []

    def set_row_constraint(self, row_constraint):
        self.row_constraint = row_constraint

    def set_col_constraint(self, col_constraint):
        self.col_constraint = col_constraint

    def set_domain(self, array_of_domain):
        if self.type == "V":
            self.domain = array_of_domain

    def add_vertical_neighbors(self, arr):
        self.col_neighbors = arr

    def add_horizontal_neighbors(self, arr):
        self.row_neighbors = arr

    def set_copy_of_domain(self):
        self.copyOfDomain = self.domain.copy()

    def __repr__(self):
        return self.name