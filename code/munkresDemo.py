from munkres import Munkres, print_matrix
#package for Hungarian algorithm

INF=99999
matrix=[
        [5,12],
        [12,INF]
       ]

m = Munkres()
indexes = m.compute(matrix)
#print_matrix(matrix, msg='Lowest cost through this matrix:')
total = 0
print indexes
'''
for row, column in indexes:
    value = matrix[row][column]
    total += value
    print '(%d, %d) -> %d' % (row, column, value)
'''
print 'total cost: %d' % total
