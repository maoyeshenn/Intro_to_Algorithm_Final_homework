import random
import cProfile
 
#生成数独
class Sudoku:
	'''
	概率数独生成器
	'''
	def __init__(self):
		'''
		digits 属性里面保存着当前的数独矩阵
		'''
		self.digits = [[] for i in range(9)]
 
	def make_digits(self):
		'''
		尝试生成数独，返回值代表生成是否成功
		'''
		#  数独矩阵的列数组，即9个竖行
		col_lists = [[] for i in range(9)]
		#  数独矩阵的区域数组，即九宫格的几个区域
		area_lists = [[] for i in range(3)]
		#  1 - 9 的随机排列
		nine = self.random_nine()
		for i in range(9):
			col_lists[i].append(nine[i])
		area_lists[0] = nine[0:3]
		area_lists[1] = nine[3:6]
		area_lists[2] = nine[6:]
 
		for i in range(8):
			nine = self.random_nine()
			#  九宫格的当前格已变换，重置当前格的数字
			if i % 3 == 2:
				area_lists[0] = []
				area_lists[1] = []
				area_lists[2] = []
			for j in range(9):
				area_index = j // 3
				count = 0
				error = False
				while (nine[0] in col_lists[j]) or (nine[0] in area_lists[area_index]):
					count += 1
					if count >= len(nine):
						error = True
						break
					nine.append(nine.pop(0))
				if error:
					return False
				first = nine.pop(0)
				col_lists[j].append(first)
				area_lists[area_index].append(first)
		self.digits = col_lists
		return True
 
	def random_nine(self):

		nine = [i + 1 for i in range(9)]
		random.shuffle(nine)
		return nine
 
 



def Gen_Sudoku(num):
	'''num:需要几道数度题目 '''
	#生成数独
	sudoku = Sudoku()
	i=0
	Sudoku_List = []
	while i < num:
		if sudoku.make_digits():
			i=i+1
			Sudoku_List.append(sudoku.digits)
	return Sudoku_List



def random_zero(a, arr):
	# a>=数组的元素个数全0
	if a >= len(arr) * len(arr[0]):
		# 行
		for i in range(len(arr)):
			# 列
			for j in range(len(arr[i])):
				arr[i][j] = 0
	
	else:
		# 已选元素索引
		selected_indices = set()

		for _ in range(a):
			# 随机行
			i = random.randint(0, len(arr) - 1)
			# 随机列
			j = random.randint(0, len(arr[i]) - 1)
			
			while (i, j) in selected_indices:
				# 行
				i = random.randint(0, len(arr) - 1)
				# 列
				j = random.randint(0, len(arr[i]) - 1)
			# 将该索引添加到集合中
			selected_indices.add((i, j))
			# 将对应的元素赋值为零
			arr[i][j] = 0
	return arr

def Sudoku_Problem_set(a, b):
	'''a为数独挖空个数, b为数独题目个数'''
	import copy
    #完整数组
	answers = Gen_Sudoku(b)
    #用于生成题目的深拷贝
	problems = copy.deepcopy(answers)
	for problem in problems:
		problem = random_zero(a, problem)
	return answers, problems


def solve(sudoku):
    #第一个0
    firstEmpty(sudoku)
    #最后一个0
    last = lastEmpty(sudoku)
    m,n = last
    # 没0元素了结束while
    while  oneIsLegal(m,n, sudoku) != True or sudoku[m][n] == 0:
        #最后一个加进来的元素
        x,y = indexList[-1]
        #判断当前位置是否合法
        if (oneIsLegal(x,y,sudoku) == True) and (0<sudoku[x][y] <= 9):
            #寻找下一个空元素
            isEmpty(sudoku)
        else:
            #1-9元素试完了
            if sudoku[x][y] >= 9:
                Stack_Back(sudoku)
                Stack_Back_Add(sudoku)
            else: #1-9还没试完
                Stack_Back_Add(sudoku)
    return sudoku

def firstEmpty(sudoku):
    '''第一个0'''
    for i in range(0,9):
        for j in range(0,9):
            if sudoku[i][j] == 0: #'0'
                Stack_Push([i,j])
                return

def lastEmpty(sudoku):
    '''最后一个0'''
    for i in range(8,-1,-1):
        for j in range(8,-1,-1):
            if sudoku[i][j] == 0: #'0'
                return [i,j]


def isEmpty(sudoku):
    '''从最后一个开始找0，放进stack里'''
    a,b = indexList[-1]
    b += 1
    for i in range(a,9):
        if i != a:
            b = 0
        for j in range(b,9):
            if sudoku[i][j] == 0: #'0'
                Stack_Push([i,j])
                return

indexList=[]

def Stack_Push(coordinate):
    '''放进stack'''
    indexList.append(coordinate)

# --- 出栈 --- #
def Stack_Pop():
    '''弹出stack'''
    indexList.pop()


def Stack_Back_Add(sudoku):
    '''+1'''
    x,y = indexList[-1]
    sudoku[x][y] += 1


def oneIsLegal(x,y,sudoku):
    '''指定位置合法性'''
    temp = sudoku[x][y]
    #行重复
    for i in range(9):
        if sudoku[x][i] == temp and i != y:
            return False; 
    #列重复
    for i in range(9): 
        if sudoku[i][y] == temp and i != x:
            return False; 
    #宫重复
    xx = x // 3
    yy = y // 3
    for i in range(3):
        for j in range(3):
            if (sudoku[xx * 3 + i][yy * 3 + j] == temp) and ((xx * 3 + i) != x) and ((yy * 3 + j) != y):
                return False; 
    return True 


def Stack_Back(sudoku):
    '''弹出最后进来的，回到上一个位置'''
    #栈顶
    x,y = indexList[-1]
    sudoku[x][y] = 0
    Stack_Pop()

def main():
    import copy
    answers, problems = Sudoku_Problem_set(30, 900)
    i = 0
    list0 = []
    for index,problem in enumerate(problems):
        solution = copy.deepcopy(solve(problem))
        if solution==answers[index]:
            i += 1
        else:
            list0.append(solution) #
    print(i/300)
    return list0, len(list0)/300




cProfile.run('main()')