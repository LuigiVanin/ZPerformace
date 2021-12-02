from typing import Any, Optional, Union, List, Tuple

number = Union[int, float]

def array_mean(array: List[number]) -> number:
    sum: Union[int, float] = 0
    for i in array:
        sum+= i
    
    return sum/len(array)


def array_sum(array: List[number]) -> number:
    sum = 0
    for i in array:
        sum+=i
        
    return sum


def print_results(
    results:List[Tuple[Any]],
    header:Optional[List[str]]=None,  
)->None:
    row_len: int
    if header is None:
        row_len = len(results[0])
    else:
        row_len = len(header)
        for idx, item in enumerate(header):
            if idx < row_len - 1:
                print(item, end=", ")
            else:
                print(item, end=";\n")
        
    for row in results:
        for i, item in enumerate(row):
            if i < row_len - 1:
                print(item, end=", ")
            else:
                print(item, end=";\n")
