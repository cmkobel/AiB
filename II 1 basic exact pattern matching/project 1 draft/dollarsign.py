# Exact pattern matching with the 'dollar sign algorithm'.
# Time and space: O(n+m)

from border_array_n import border_array

def dollarsign_matches(string, pattern):
    """ Generator.
        Yields the position(s), where pattern occurs in string. 
    """
    m = len(pattern)
    pdx = pattern + '$' + string # Concatenate pattern and string.

    for _i, i in enumerate(border_array(pdx)):
        if i == m:
            yield _i-2*m +1

if __name__ == '__main__':
    # Test:
    x = 'hvoreremiliemiliedejligeemiliehenne?'
    p = 'emilie'

    print(f'find <{p}> in')    
    print()
    print(x)
    matches = []
    for match in dollarsign_matches(x, p):
        print((match-1) * ' ', '~'*len(p), sep = '') 
        matches.append(match)
    print(matches)

