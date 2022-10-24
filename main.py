import CSP
import Cell

def main():
    file = open("input3.txt", 'r')
    row_num = int(file.readline()[0])
    col_num = int(file.readline()[0])
    game = CSP.Kakuro(row_num, col_num)
    for i in range(row_num):
        row_nums_string = file.readline().split(' ')
        for j in range(col_num):
            if row_nums_string[j].endswith('\n'):
                row_nums_string[j] = row_nums_string[j].split('\n')[0]
            if row_nums_string[j] == "0":
                node = Cell.Cell('V', i, j)
                game.board[i][j] = node
            elif row_nums_string[j] == "-1":
                node = Cell.Cell('B', i, j)
                game.board[i][j] = node
            else:
                node = Cell.Cell('C', i, j)
                if i == 0:
                    node.set_col_constraint(int(row_nums_string[j]))
                elif j == 0:
                    node.set_row_constraint(int(row_nums_string[j]))
                else:
                    node.set_row_constraint(int(row_nums_string[j]))
                    node.set_col_constraint(int(row_nums_string[j]))
                game.board[i][j] = node
    game.start()

main()