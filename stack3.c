#include <stdio.h>
#include <stdlib.h>

int makeodd(int number){
    int odd = 1;
    if(number % 2 == 0){
        return number + odd;
    }
    else{
        return number;
    }
}

int main(int argc, char* argv[]){
    int result = 0; // 변수의 초기화
    /*
    printf("argc: %d\n", argc); //argc와 argv가 어떤것인지 보기위한 부분(주석처리된 부분)
    for(int i=0; i < argc; i++){
        printf("argv[%d] = %s\n", i, argv[i]);
    }
    if(argc != 2){                                 // argc가 2가 아닐 경우에 인자를 전달 해야된다고 알려줌
        printf("usage: %s number\n", argv[0]);     
        exit(-1);                                   
    }
    printf("number + 1 = %d\n", atoi(argv[1]) + 1); // argv는 문자열이기 때문에 1을 더해도 이상한 값이 나온다. 때문에 atoi 함수를 사용(그래도 문제가 있음)
    */
    if(argc != 2){                                 // <==처럼 예외 처리를 안 할 경우 프로그램이 실행이 안됨
        printf("usage: %s number\n", argv[0]);     
        exit(-1);                                   
    }

    result = makeodd(atoi(argv[1]));
    printf("makeodd %d\n", result);
    return 0;
}