class Matrix:
    def __init__(self, numbers):
        self.numbers = numbers
        self.height = len(numbers)
        self.width = len(numbers[0])

    def store_as_tuple(self, numbers):
        return tuple(tuple(x) for x in numbers)

    def __str__(self):
        return str(self.numbers)

    def __truediv__(self, other):
        result = []
        for i in range(self.height):
            result.append([])
            for j in range(self.width):
                result[i].append(self.numbers[i][j] / other)
        return Matrix(result)

    def __mul__(self, other):
        if type(other) in [float, int]:
            return self.__truediv__(1 / other)
        if other.height != self.width:
            return None
        result = [[0 for i in range(other.width)] for j in range(self.height)]
        for i in range(len(result)):
            for j in range(len(result[0])):
                # print(sum(self.numbers[i][k] * other.numbers[k][j] for k in range(self.width)))
                result[i][j] = sum(self.numbers[i][k] * other.numbers[k][j] for k in range(self.width))
        return Matrix(result)

    def get_submatrix(self, horizontal_removed, vertical_removed):
        #print("Before: ", self)
        copy = self.copy()
        result = [row for a, row in enumerate(copy.numbers) if a != vertical_removed]
        new_result = []
        for i in range(self.height - 1):
            new_result.append([])
            for j in range(self.width):
                if j != vertical_removed:
                    new_result[i].append(result[i][j])
            #new_result.append([result[i][j] for j in range(len(result[i])) if j != vertical_removed])
        #print("Parameters:", vertical_removed, horizontal_removed)
        #print("Result:", new_result)
        return Matrix(new_result)

    def get_determinant(self):
        if self.height == 1:
            return self.numbers[0][0]
        if self.height == 2:
            result = self.numbers[0][0] * self.numbers[1][1] - self.numbers[1][0] * self.numbers[0][1]
            #print(f"Determinant of {self} is {result}")
            return result
        result = 0
        for i in range(self.width):
            result += self.numbers[0][i] * self.get_submatrix(0, i).get_determinant() * (-2 * (i % 2) + 1)

        return result

    def transpose(self):
        result = []
        for i in range(self.height):
            result.append([self.numbers[j][i] for j in range(self.width)])
        return Matrix(result)

    def reverse_signs(self):
        result = []
        for i in range(self.height):
            result.append([])
            for j in range(self.width):
                if (i + j) % 2 == 1:
                    result[i].append(-self.numbers[i][j])
                else:
                    result[i].append(self.numbers[i][j])
        return Matrix(result)

    def copy(self):
        return Matrix([num for num in self.numbers])

    def invert(self):
        #print(self, "before inversion")
        determinant = self.get_determinant()
        if determinant == 0 or self.height != self.width:
            return None
        if self.height != 1:
            result = Matrix([[0 for i in range(self.width)] for j in range(self.height)])
            if self.height != 2:
                for i in range(self.height):
                    for j in range(self.width):
                        result.numbers[i][j] = self.get_submatrix(i, j).get_determinant()
                #print(result)
                result = result.transpose()
                #print(result)
                result = result.reverse_signs()
                #print(result)
            else:
                result = self.reverse_signs()
                result.numbers[0][0], result.numbers[1][1] = result.numbers[1][1], result.numbers[0][0]
            return result.__truediv__(determinant)
        return self


class EquationSystem:
    def __init__(self, equations, variables="abcdefghijklmnopqrstuvwxyz"):
        if len(equations) + 1 < len(equations[0]):
            print("Not enough equations!", equations)
            return
        self.variables = variables
        self.coefficients = Matrix([eq[:-1] for eq in equations])
        self.constants = Matrix([[eq[-1]] for eq in equations])
        print("equations are:", self)

    def __str__(self):
        info = ""
        for i, row in enumerate(self.coefficients.numbers):
            info += str(row[0]) + str(self.variables[0])
            for j, coef in enumerate(row[1:]):
                info += str(" + " if coef >= 0 else " - ") + str(abs(coef)) + self.variables[j + 1]
            info += f" = {self.constants.numbers[i][0]}\n"
        return info

    def solve(self):
        print(self.coefficients.invert(), "is inverse")
        return self.coefficients.invert() * self.constants

