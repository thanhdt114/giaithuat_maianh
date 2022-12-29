# Online Python compiler (interpreter) to run Python online.
# Write Python 3 code in this online editor and run it.
import random
import math

_goal_state = [[1,2,3],
               [8,0,4],
               [7,6,5]]
_init_state = [[7,8,1],
               [0,4,3],
               [6,2,5]]
               
##################################################
# NOTE: trả về vị trí của item trong seq
# Nếu không tìm thấy sẽ trả về -1
##################################################
def index(item, seq):
    """Helper function that returns -1 for non-found index value of a seq"""
    if item in seq:
        return seq.index(item)
    else:
        return -1

class EightPuzzle:

    ##################################################
    # NOTE: khởi tạo các giá trị ban đầu
    # adj_matrix là ma trận ban đầu
    ##################################################
    def __init__(self):
        # heuristic value
        self._hval = 0
        # search depth of current instance
        self._depth = 0
        # parent node in search path
        self._parent = None
        self.adj_matrix = []
        for i in range(3):
            self.adj_matrix.append(_init_state[i][:])

    ##################################################
    # NOTE: So sánh ma trận hiện tại và ma trận orther
    ##################################################
    def __eq__(self, other):
        if self.__class__ != other.__class__:
            return False
        else:
            return self.adj_matrix == other.adj_matrix

    ##################################################
    # NOTE: gán ma trận vào chuỗi để in ra màn hình
    ##################################################
    def __str__(self):
        res = ''
        for row in range(3):
            res += ' '.join(map(str, self.adj_matrix[row]))
            res += '\r\n'
        return res

    ##################################################
    # NOTE: tạo ra ma trận bản sao
    ##################################################
    def _clone(self):
        p = EightPuzzle()
        for i in range(3):
            p.adj_matrix[i] = self.adj_matrix[i][:]
        return p

    ##################################################
    # NOTE: tìm ra tất cả vị trí có thể di chuyển của ô số 0
    # Tối đa có thể di chuyển theo bốn hướng: lên, xuống, trái phải
    ##################################################
    def _get_legal_moves(self):
        """Returns list of tuples with which the free space may
        be swapped"""
        # get row and column of the empty piece
        row, col = self.find(0)
        free = []
        
        # find which pieces can move there
        if row > 0:
            free.append((row - 1, col))
        if col > 0:
            free.append((row, col - 1))
        if row < 2:
            free.append((row + 1, col))
        if col < 2:
            free.append((row, col + 1))

        return free

    ##################################################
    # NOTE: Tạo ra các ma trận bản sao với 1 lần di chuyển ô số 0
    # Tối đa có 4 ma trận bản sao
    ##################################################
    def _generate_moves(self):
        free = self._get_legal_moves()
        zero = self.find(0)

        ##################################################
        # NOTE: Tạo ra ma trận bản sao và di chuyển 1 vị trí
        # Lưu lại ma trận cha
        ##################################################
        def swap_and_clone(a, b):
            p = self._clone()
            p.swap(a,b)
            p._depth = self._depth + 1
            p._parent = self
            return p

        return map(lambda pair: swap_and_clone(zero, pair), free)

    ##################################################
    # NOTE: tạo 1 mảng chứa tất cả ma trận kết quả
    ##################################################
    def _generate_solution_path(self, path):
        if self._parent == None:
            return path
        else:
            path.append(self)
            return self._parent._generate_solution_path(path)

    ##################################################
    # NOTE: Thực hiện biến đổi ma trận 
    # Trả về mảng ma trận kết quả và số lần di chuyển
    ##################################################
    def solve(self, h):
        """Performs A* search for goal state.
        h(puzzle) - heuristic function, returns an integer
        """
        
        ##################################################
        # NOTE: so sánh ma trận hiện tại và ma trận đích
        ##################################################
        def is_solved(puzzle):
            return puzzle.adj_matrix == _goal_state

        ##################################################
        # NOTE: thực hiện biến đổi ma trận hiện tại thành ma trận đích
        ##################################################
        openl = [self]
        closedl = []
        move_count = 0
        while len(openl) > 0:
            ##################################################
            # NOTE: so sánh ma trận hiện tại và ma trận đích
            # Nếu bằng nhau sẽ trả về mảng ma trận kết quả
            ##################################################
            x = openl.pop(0)
            move_count += 1
            if (is_solved(x)):
                if len(closedl) > 0:
                    return x._generate_solution_path([]), move_count
                else:
                    return [x]

            ##################################################
            # NOTE: tạo ra ma các ma trận co thể di chuyển với 1 bước
            # Gán ma trận có chi phí thấp nhất vào closedl
            # openl là ma trận đang xét
            ##################################################
            succ = x._generate_moves()
            idx_open = idx_closed = -1
            for move in succ:
                # have we already seen this node?
                idx_open = index(move, openl)
                idx_closed = index(move, closedl)
                hval = h(move)
                fval = hval + move._depth

                ##################################################
                # NOTE: 
                # Nếu ma trận đã di chuyển 1 bước khác ma trận hiện tại và không trùng với các ma trận đã xét thì thêm vào mảng ma trận hiện tại để xét
                # Nếu ma trận đã di chuyển 1 bước trùng với ma trận để xét, không trùng với ma trận kết quả và có chi phí thấp hơn chi phí của ma trận bị trùng thì thay ma trận  bị trùng đó bằng ma trận đã di chuyển 1 bước
                # Nếu ma trận đã di chuyển 1 bước trùng với ma trận kết quả, không trùng với ma trận đang xét và có chi phí thấp hơn ma trận bị trùng thì xóa ma trận bị trùng và thêm ma trận đã di chuyển 1 bước vào ma trận để xét 
                ##################################################
                if idx_closed == -1 and idx_open == -1:
                    move._hval = hval
                    openl.append(move)
                elif idx_open > -1:
                    copy = openl[idx_open]
                    if fval < copy._hval + copy._depth:
                        # copy move's values over existing
                        copy._hval = hval
                        copy._parent = move._parent
                        copy._depth = move._depth
                elif idx_closed > -1:
                    copy = closedl[idx_closed]
                    if fval < copy._hval + copy._depth:
                        move._hval = hval
                        closedl.remove(copy)
                        openl.append(move)

            closedl.append(x)
            openl = sorted(openl, key=lambda p: p._hval + p._depth)

        # if finished state not found, return failure
        return [], 0

    ##################################################
    # NOTE: tìm vị trí của giá trị đã cho
    # giá trị đã cho nằm trong khoảng từ 0 đến 8
    # hàm trả về vị trí dòng và vị trí cột
    ##################################################
    def find(self, value):
        """returns the row, col coordinates of the specified value
           in the graph"""
        if value < 0 or value > 8:
            raise Exception("value out of range")

        for row in range(3):
            for col in range(3):
                if self.adj_matrix[row][col] == value:
                    return row, col
    
    ##################################################
    # NOTE: lấy giá trị của ma trận tại dòng row, cột col
    ##################################################
    def peek(self, row, col):
        """returns the value at the specified row and column"""
        return self.adj_matrix[row][col]

    ##################################################
    # NOTE: gán giá trị cho ma trại tại dòng row, cột col bằng giá trị của value 
    ##################################################
    def poke(self, row, col, value):
        """sets the value at the specified row and column"""
        self.adj_matrix[row][col] = value

    ##################################################
    # NOTE: hoán đổi giá trị của 2 ô a và b
    ##################################################
    def swap(self, pos_a, pos_b):
        """swaps values at the specified coordinates"""
        temp = self.peek(*pos_a)
        self.poke(pos_a[0], pos_a[1], self.peek(*pos_b))
        self.poke(pos_b[0], pos_b[1], temp)

##################################################
# NOTE: Tính tổng chi phí để biến đổi ma trận hiện tại thành ma trận thành ma trận đích
################################################## 
def h_manhattan(puzzle):
    """
    the heuristic function
    """
    ##################################################
    # NOTE: Tìm vị trí của giá trị trong ma trận đích
    ##################################################
    def goal_find(val):
        """Find the target_row, target_col of the specified value in the goal"""
        if (val < 0 or val > 8):
            raise Exception("value out of range")
        for row in range(3):
            for col in range(3):
                if _goal_state[row][col] == val:
                    return row, col
                 
    ##################################################
    # NOTE: Tính tổng chi phí để biến đổi ma trận hiện tại thành ma trận thành ma trận đích
    ##################################################   
    t = 0
    for row in range(3):
        for col in range(3):
            val = puzzle.peek(row, col)
            target_row, target_col = goal_find(val)
            t += abs(target_row - row) + abs(target_col - col)

    return t

def main():
    p = EightPuzzle()
    print("Init state:")
    print (p)

    path, count = p.solve(h_manhattan)
    path.reverse()
    for i in path: 
        print (i)
        
    print ("Solved with Manhattan distance exploring", count, "states")
    
if __name__ == "__main__":
    main()