def border_array(x):
    """ O(n) time """
    n = len(x)
    ba = [0 for i in range(n)]
    for i in range(1, n):
        b = ba[i-1]
        while b > 0 and x[i] != x[b]:
            b = ba[b-1]
        ba[i] = (x[i] == x[b]) * (b + 1)
    return ba




if __name__ == '__main__':
    print(border_array('abaabbbbabaab'))