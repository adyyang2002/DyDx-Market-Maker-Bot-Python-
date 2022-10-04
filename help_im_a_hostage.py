str = "abc"

def dfs(str, index, sub):
    if index > len(str):
        return sub
    dfs(str, index + 1, sub)
    dfs(str, index + 1, sub + str[index])

def main(str):
    dfs(str, 0, "")

"""
            ""
        a       b
    |    |     |        
    ab   ac     bc
|       
abc

            ""
              abc
            |        |       
            ab       bc
          |    |     |
         a      b    c

            "abc" 0, ""
            |       |
            a,1         "", 1
            |   |        |   |
        ab, 2   a, 2    b,2   "", 2  
"""         