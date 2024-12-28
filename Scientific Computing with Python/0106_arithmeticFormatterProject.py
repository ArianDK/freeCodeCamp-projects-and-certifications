def arithmetic_arranger(problems, show_answers=False):
    if len(problems) > 5:
        return "Error: Too many problems."
    first_line = []
    second_line = []
    dashes_line = []
    results_line = []
    for problem in problems:
        # check that the problems have the right format
        parts = problem.split()
        if len(parts) != 3:
            return "Error: Invalid problem format."
        
        first_num = problem.split()[0] # returns first number
        operator = problem.split()[1] # returns operator
        second_num = problem.split()[2] # returns second number

        # check that operator is + or -
        if operator not in ["+", "-"]:
            return "Error: Operator must be '+' or '-'."
        # check that first_num and second_num are both digits
        if not first_num.isdigit() or not second_num.isdigit():
            return "Error: Numbers must only contain digits."
        # check that the length of first_num and second_num are both less than 4
        if len(first_num) > 4 or len(second_num) > 4:
            return "Error: Numbers cannot be more than four digits."

        width = max(len(first_num), len(second_num)) + 2
        dashedLines = "-" * width

        first_line.append(f"{first_num:>{width}}")
        second_line.append(f"{operator} {second_num:>{width - 2}}")
        dashes_line.append(dashedLines)

        # calculate the answer of the arithmetic equation
        if show_answers:
            if operator == "+":
                result = int(first_num) + int(second_num)
            elif operator == "-":
                result = int(first_num) - int(second_num)
            results_line.append(f"{result:>{width}}")
        
        # append the problems
        problems = (
            "    ".join(first_line) + "\n" +
            "    ".join(second_line) + "\n" +
            "    ".join(dashes_line)
        )

        # add the answer if True is passed in to the function
        if show_answers:
            problems += "\n" + "    ".join(results_line)

    return problems

print(f'\n{arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49"])}')