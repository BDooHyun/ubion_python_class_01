# for 문
def custom_mean(*args) :
    result = args[0]
    x = 0
    for i in args :
        x += i
        result = x / len(args)
    
    return result

def custom_max(*args) :
    result = args[0]
    # 첫번째 원소 출력
    # 첫번째 원소와 두번째 원소의 값을 비교하여 큰 값을 result 에 대입
    # if result > args[1] :
    #     result = args[0]
    # else :
    #    result = args[1]
    # if result < args[1] :
    #     result = args[1]

    # result 와 세번째 원소를 비교
    # if result > args[2] :
    #     result = result
    # else :
    #     result = args[2]
    # if result < args[2] :
    #     result = args[2]

    # for i in range(1, len(args), 1) :
    #     if result < args[i] :
    #         result = args[i]        
    for i in args :
        if result < i :
            result = i

    return result
