# computing border array


def compute_border_array(S):
    """ O(n^2) time """
    n = len(S)
    B = [0 for j in range(n)]
    for j in range(1, n): # gennemløb strengen fra anden position
        
        for i in range(j-1): # minus one: only proper borders.
            if S[0:i+1] == S[j-i:j+1]:
                B[j] = i+1


    return B






if __name__ == '__main__':
    print(compute_border_array("abaabbbbabaab"))

