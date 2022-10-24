import os
os.system("color")


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Kakuro:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.board = [[0]*col for i in range(row)]
        self.variables = []
        self.ac3_counter = 10

    def start(self):
        self.set_variables()
        self.set_neighbors()
        self.calculate_domain()
        self.set_copy_of_domain_each_node()
        self.ac3()
        # for var in self.variables:
        #     print(var.copyOfDomain)
        print(self.backtrack(0))

    def set_variables(self):
        for i in range(self.row):
            for j in range(self.col):
                node = self.board[i][j]
                if node.name[0] == 'V':
                    self.variables.append(node)

    def set_copy_of_domain_each_node(self):
        for node in self.variables:
            node.set_copy_of_domain()

    def set_neighbors(self):
        for i in range(self.row):
            for j in range(self.col):
                neighbors = []
                node = self.board[i][j]
                if node.name[0] == 'V':
                    for k in range(j + 1, self.col):
                        n = self.board[i][k]
                        if n.name[0] == 'V':
                            if n.name != node.name:
                                neighbors.append(n)
                        else:
                            break

                    for k in range(j, -1, -1):
                        n = self.board[i][k]
                        if n.name[0] == 'V':
                            if n.name != node.name:
                                neighbors.append(n)
                        else:
                            if n.name[0] == 'C':
                                node.set_row_constraint(n.row_constraint)
                                break
                    node.add_horizontal_neighbors(neighbors)

                    neighbors = []
                    for k in range(i + 1, self.row):
                        n = self.board[k][j]
                        if n.name[0] == 'V':
                            if n.name != node.name:
                                neighbors.append(n)
                        else:
                            break

                    for k in range(i - 1, -1, -1):
                        n = self.board[k][j]
                        if n.name[0] == 'V':
                            if n.name != node.name:
                                neighbors.append(n)
                        else:
                            if n.name[0] == 'C':
                                node.set_col_constraint(n.col_constraint)
                            break
                    node.add_vertical_neighbors(neighbors)

    def calculate_domain(self):
        for i in range(self.row):
            for j in range(self.col):
                domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                node = self.board[i][j]
                if node.name[0] == 'V' and node.value is None:
                    number_of_neighbors = 1
                    for k in range(0, len(node.row_neighbors)):
                        if node.row_neighbors[k].value is None:
                            number_of_neighbors += 1
                    max_value = int(node.row_constraint - ((number_of_neighbors * (number_of_neighbors - 1)) / 2))
                    min_value = int(node.row_constraint - ((20 - number_of_neighbors) * (number_of_neighbors - 1)) / 2)
                    domain = [x for x in domain if x >= min_value]
                    domain = [x for x in domain if x <= max_value]
                    node.set_domain(domain)

                    number_of_neighbors = 1
                    for k in range(0, len(node.col_neighbors)):
                        if node.col_neighbors[k].value is None:
                            number_of_neighbors += 1
                    max_value = int(node.col_constraint - ((number_of_neighbors * (number_of_neighbors - 1)) / 2))
                    min_value = int(node.col_constraint - ((20 - number_of_neighbors) * (number_of_neighbors - 1)) / 2)
                    domain = [x for x in domain if x >= min_value]
                    domain = [x for x in domain if x <= max_value]
                    if node.domain != domain:
                        if len(domain) < len(node.domain):
                            node.set_domain(domain)

    def mrv(self):
        min_value = 10
        min_node = None
        for node in self.variables:
            if len(node.copyOfDomain) <= min_value and node.value is None:
                return node
        return min_node

    def lcv(self, node):
        domain_conflict = []
        for domain in node.copyOfDomain:
            sum = 0
            for neighbor in node.row_neighbors:
                if domain in neighbor.copyOfDomain:
                    sum += 1
            for neighbor in node.col_neighbors:
                if domain in neighbor.copyOfDomain:
                    sum += 1
            domain_conflict.append((domain, sum))
        domain_conflict.sort(key=lambda dc: dc[1])
        return node.copyOfDomain

    def backtrack(self, num_assigned):
        if num_assigned < len(self.variables):
            # node = self.arrOfValueNodes[number_in_arr_of_value]
            node = self.mrv()
            # for domain in node.copyOfDomain:
            for domain in self.lcv(node):
                node.value = domain
                print(node, " = ", node.value)
                if self.is_consistent(node):
                    if self.forward_checking(node):
                        if self.backtrack(num_assigned + 1):
                            return True
                    self.undo_forward_checking(node)
                node.value = None
        else:
            self.print_board_value(self.row, self.col, self.board)
            exit()

    def forward_checking(self, node):
        for x in node.col_neighbors:
            if node.value in x.copyOfDomain:
                x.copyOfDomain.remove(node.value)
            if len(x.copyOfDomain) <= 0 and x.value is None:
                return False
        for x in node.row_neighbors:
            if node.value in x.copyOfDomain:
                x.copyOfDomain.remove(node.value)
            if len(x.copyOfDomain) <= 0 and x.value is None:
                return False
        return True

    def undo_forward_checking(self, node):
        for x in node.col_neighbors:
            if node.value in x.domain:
                x.copyOfDomain.append(node.value)
                x.copyOfDomain = list(dict.fromkeys(x.copyOfDomain))
                x.copyOfDomain.sort()
        for x in node.row_neighbors:
            if node.value in x.domain:
                x.copyOfDomain.append(node.value)
                x.copyOfDomain = list(dict.fromkeys(x.copyOfDomain))
                x.copyOfDomain.sort()

    def ac3(self):
        queue = {(var1, var2) for var1 in self.variables for var2 in var1.row_neighbors}
        queue1 = {(var1, var2) for var1 in self.variables for var2 in var1.col_neighbors}
        queue.update(queue1)
        while len(queue) != 0:
            var1, var2 = queue.pop()
            if self.revise(var1, var2):
                if len(var1.copyOfDomain) == 0:
                    return False
                for neighbor in var1.row_neighbors:
                    if neighbor.name != var2.name:
                        queue.add((neighbor, var1))
        return True

    def revise(self, var1, var2):
        revised = False
        for d1 in var1.copyOfDomain:
            conflict = True
            for d2 in var2.copyOfDomain:
                if self.have_conflict(var1, d1, var2, d2):
                    conflict = False
                if not conflict:
                    break
            if conflict:
                var1.copyOfDomain.remove(d1)
                revised = True
        return revised

    def have_conflict(self, var1, d1, var2, d2):
        if d1 == d2:
            return False
        if var1.row_num == var2.row_num:
            line = self.board[var1.row_num]
            desired_sum = -1
            for cell in line:
                if cell.type == 'C':
                    desired_sum = cell.row_constraint
                    break
        else:
            column = []
            for line in self.board:
                column.append(line[var1.col_num])
            desired_sum = -1
            for cell in column:
                if cell.type == 'C':
                    desired_sum = cell.col_constraint
                    break
        if desired_sum == -1:
            return True
        sum = d1 + d2
        completed = True
        neighbors = var1.row_neighbors if var1.row_num == var2.row_num else var1.col_neighbors
        # neighbors.remove(var2)
        for n in neighbors:
            if n.name != var2.name and n.value is not None:
                sum += n.value
            else:
                completed = False
        if completed:
            if sum == desired_sum:
                return True
            else:
                return False
        else:
            if sum < desired_sum:
                return True
            else:
                return False

    def is_consistent(self, node):
        col_sum = node.value
        row_sum = node.value
        row_counter = 0
        col_counter = 0
        for x in node.col_neighbors:
            if x.value is not None:
                if x.value == node.value:
                    return False
                col_counter += 1
                col_sum += x.value

        for x in node.row_neighbors:
            if x.value is not None:
                if x.value == node.value:
                    return False
                row_counter += 1
                row_sum += x.value

        if row_sum > node.row_constraint:
            return False
        elif col_sum > node.col_constraint:
            return False
        elif col_counter == len(node.col_neighbors) and col_sum != node.col_constraint:
            return False
        elif row_counter == len(node.row_neighbors) and row_sum != node.row_constraint:
            return False
        return True

    def print_board_value(self, row, col, board):
        for i in range(row):
            for j in range(col):
                if board[i][j].value is None and board[i][j].type == 'V':
                    print(" ", 0, end=" ")
                elif board[i][j].type == 'C':
                    if board[i][j].row_constraint is not None:
                        print(Colors.OKGREEN, board[i][j].row_constraint, Colors.ENDC, end="")
                    elif board[i][j].col_constraint is not None:
                        print(Colors.OKGREEN, board[i][j].col_constraint, Colors.ENDC, end="")
                elif board[i][j].type == 'B':
                    print(Colors.FAIL, -1, Colors.ENDC, end="")
                else:
                    print("", board[i][j].value, end=" ")
            print()
