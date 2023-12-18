import random
import cProfile
import copy
 
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


import networkx as nx
import itertools
#解数独
def find_candidates(grid, row, col):
    # 如果单元格已经有数字，就返回空集合
    if grid[row][col] != 0:
        return set()
    else:
        candidates = set(range(1, 10))
        for i in range(9):
            candidates.discard(grid[row][i]) #列
            candidates.discard(grid[i][col]) #行
        row_start = (row // 3) * 3
        col_start = (col // 3) * 3
		#方块
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                candidates.discard(grid[i][j])
        return candidates

def build_graph(grid):
    # 创建一个空的图
    graph = nx.Graph()
    # 遍历每个单元格，把它们作为顶点加入到图中，顶点的属性包括行号、列号和候选数字
    for i in range(9):
        for j in range(9):
            candidates = find_candidates(grid, i, j)
            graph.add_node((i, j), row=i, col=j, box=(i//3, j//3), candidates=candidates)
    # 遍历每两个顶点，如果它们在同一行、同一列或同一个小方块中，就在它们之间添加一条边
    for u, v in itertools.combinations(graph.nodes, 2):
        if (graph.nodes[u]['row'] == graph.nodes[v]['row']) or (graph.nodes[u]['col'] == graph.nodes[v]['col']) or (graph.nodes[u]['box'] == graph.nodes[v]['box']):
            graph.add_edge(u, v)
    return graph

def find_max_cliques(graph):
    # 创建一个空的列表，用来存储最大团
    max_cliques = []
    # 遍历图中的每个顶点
    for node in graph.nodes:
        # 找出和该顶点相邻的所有顶点，构成一个子图
        neighbors = list(graph.neighbors(node))
        subgraph = graph.subgraph(neighbors)
        # 在子图中找出所有的团，用一个集合来存储
        cliques = set()
        for clique in nx.find_cliques(subgraph):
            # 把每个团转换成一个元组，方便比较和排序
            clique = tuple(sorted(clique))
            cliques.add(clique)
        # 对每个团，判断它是否是最大的，即它的顶点数是否等于它的候选数字的个数
        for clique in cliques:
            # 首先，把该顶点加入到团中，构成一个候选的最大团
            clique = clique + (node,)
            # 然后，找出该最大团中所有顶点的候选数字的并集
            candidates = set()
            for i, j in clique:
                candidates = candidates.union(graph.nodes[(i, j)]['candidates'])
            # 最后，如果最大团的顶点数和候选数字的个数相等，就把它加入到最大团的列表中
            if len(clique) == len(candidates):
                max_cliques.append(clique)
    # 返回最大团的列表 
    return max_cliques


def eliminate_candidates(graph, max_cliques):
    # 遍历每个最大团
    for clique in max_cliques:
        # 找出该最大团中所有顶点的候选数字的并集
        candidates = set()
        for i, j in clique:
            candidates = candidates.union(graph.nodes[(i, j)]['candidates'])
        # 遍历该最大团中的每个顶点
        for i, j in clique:
            # 找出该顶点所在的行、列和小方块
            row = graph.nodes[(i, j)]['row']
            col = graph.nodes[(i, j)]['col']
            box = graph.nodes[(i, j)]['box']
            # 遍历图中的每个顶点
            for u, v in graph.nodes:
                # 如果该顶点和最大团中的顶点在同一行、同一列或同一个小方块中，但不属于最大团，就把候选数字的并集从它的候选数字中去掉
                if (u, v) not in clique and (graph.nodes[(u, v)]['row'] == row or graph.nodes[(u, v)]['col'] == col or graph.nodes[(u, v)]['box'] == box):
                    graph.nodes[(u, v)]['candidates'] = graph.nodes[(u, v)]['candidates'].difference(candidates)

def is_solved(grid):
    # 遍历每个单元格，如果有空格，就返回False
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                return False
    # 否则，返回True
    return True

def solve(grid):
	graph = build_graph(grid)
	while not is_solved(grid):
		#空格数
		empty_cells = sum(row.count(0) for row in grid)
		# 找出图中的所有最大团
		max_cliques = find_max_cliques(graph)
		# 根据最大团来消除候选数字
		eliminate_candidates(graph, max_cliques)
		for i, j in graph.nodes: # 一个候选数字，填入数独 
			if len(graph.nodes[(i, j)]['candidates']) == 1: 
				grid[i][j] = list(graph.nodes[(i, j)]['candidates'])[0]
				for u, v in graph.neighbors((i, j)):
					graph.nodes[(u, v)]['candidates'].discard(grid[i][j])
				graph.nodes[(i, j)]['candidates'].discard(grid[i][j])
		
		if sum(row.count(0) for row in grid) == empty_cells: 
			break

	for i, j in graph.nodes:
		if len(graph.nodes[(i, j)]['candidates'])!=0:
			grid[i][j] = list(graph.nodes[(i, j)]['candidates'])[0]
			for u, v in graph.neighbors((i, j)):
				graph.nodes[(u, v)]['candidates'].discard(grid[i][j])
			graph.nodes[(i, j)]['candidates'].discard(grid[i][j])
	return grid




def main():
    import copy
    answers, problems = Sudoku_Problem_set(30, 10000)
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