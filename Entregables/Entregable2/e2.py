import sys
from typing import TextIO, Iterable
from algoritmia.schemes.dac_scheme import IDivideAndConquerProblem, div_solve

Reservation = tuple[int, int, int]
Problem = tuple[int, list[Reservation]]
Forecast = list[int]


def read_data(f: TextIO) -> Problem:
    reservas = []
    maximo = int(f.readline().strip("\n"))
    for line in f.readlines():
        reserva = line.strip("\n").split(" ")
        tup = (int(reserva[0]),int(reserva[1]),int(reserva[2]))
        reservas.append(tup)
    return (maximo,reservas)

def process(problem: Problem) -> Forecast:
    class PrediccionOcupacion(IDivideAndConquerProblem):
        def __init__(self, v: list[Reservation], m: int):
            self.v = v
            self.m = m
        def is_simple(self) -> bool:
            return len(self.v) <=1
        def trivial_solution(self) -> list[int]:

            sol=[]
            sol.append(self.v[0][0])
            sol.append(self.v[0][1])
            sol.append(self.v[0][0] + self.v[0][2])
            return sol
        def divide(self) -> Iterable[IDivideAndConquerProblem]:
            mid = len(self.v) //2
            yield PrediccionOcupacion(self.v[:mid], self.m)
            yield PrediccionOcupacion(self.v[mid:], self.m)
        def combine(self, solutions: Iterable[list[int]]) -> list[int]:
            left,right = solutions
            monta_left = []
            monta_right = []
            if len(left)==3:
                for elem in range(left[0],left[2]):
                    monta_left.append(elem)
                    monta_left.append(left[1])
                monta_left.append(left[2])
                monta_left.append(0)
            else:
                monta_left = left
            if len(right) == 3:
                for elem in range(right[0],right[2]):
                    monta_right.append(elem)
                    monta_right.append(right[1])
                monta_right.append(right[2])
                monta_right.append(0)
            else:
                monta_right = right
            i,j = 0,0
            sol=[]


            while i<len(monta_left) and j<len(monta_right):
                if monta_left[i]< monta_right[j]:
                    sol.append(monta_left[i])
                    sol.append(monta_left[i+1])
                    i+=2
                elif monta_left[i] == monta_right[j]:
                    sol.append(monta_left[i])
                    suma = monta_left[i+1] + monta_right[j+1]
                    if suma > self.m:
                        suma = self.m
                    sol.append(suma)
                    i+=2
                    j+=2
                elif monta_left[i]> monta_right[j]:
                    sol.append(monta_right[j])
                    sol.append(monta_right[j+1])
                    j+=2
                if i<len(monta_left) and j>= len(monta_right):
                    while i<len(monta_left):
                        sol.append(monta_left[i])
                        sol.append(monta_left[i+1])
                        i+=2
                if j<len(monta_right) and i>= len(monta_left):
                    while j<len(monta_right):
                        sol.append(monta_right[j])
                        sol.append(monta_right[j+1])
                        j+=2
            return sol

    po_problem = PrediccionOcupacion(problem[1],problem[0])
    solution = div_solve(po_problem)
    sol_limpia = []
    k = 0
    while k < len(solution):
        if solution[k + 1] != solution[k - 1]:
            sol_limpia.append(solution[k])
            sol_limpia.append(solution[k + 1])
        k += 2
    del sol_limpia[-1]
    return sol_limpia


#
# def process(problem: Problem) -> Forecast:
#     class PrediccionOcupacion(IDivideAndConquerProblem):
#         def __init__(self, v: list[Reservation], m: int):
#             self.v = v
#             self.m = m
#         def is_simple(self) -> bool:
#             return len(self.v) <=1
#         def trivial_solution(self) -> list[int]:
#
#             sol=[0]*(self.v[0][0] + self.v[0][2])
#             i=0
#             while i <len(sol):
#                 if i+1>= self.v[0][0] and i+1<(self.v[0][2]+self.v[0][0]):
#                     sol[i] = self.v[0][1]
#                 i+=1
#             return sol
#         def divide(self) -> Iterable[IDivideAndConquerProblem]:
#             mid = len(self.v) //2
#             yield PrediccionOcupacion(self.v[:mid], self.m)
#             yield PrediccionOcupacion(self.v[mid:], self.m)
#         def combine(self, solutions: Iterable[list[int]]) -> list[int]:
#             left,right = solutions
#             peque = right
#             sol = left
#             if len(left)<len(right):
#                 peque = left
#                 sol = right
#
#             i=0
#
#             while i<len(peque):
#                 suma = sol[i]+peque[i]
#                 if suma>=self.m:
#                     suma = self.m
#                 sol [i] = suma
#                 i+=1
#             return sol
#
#
#
#
#     po_problem = PrediccionOcupacion(problem[1],problem[0])
#     solution = div_solve(po_problem)
#     sol = []
#     i=0
#     while i<len(solution)-1:
#         if solution[i-1]==solution[i]:
#             i+=1
#         else:
#             sol.append(i+1)
#             sol.append(solution[i])
#             i+=1
#     sol.append(len(solution))
#
#     return sol
#


def show_results(forecast: Forecast) -> None:
    print(" ".join(map(str, forecast)))


if __name__ == "__main__":
    problem = read_data(sys.stdin)
    forecast = process(problem)
    show_results(forecast)
