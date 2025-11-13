# Control Flow in Julia

println("=== If-Else Statements ===")
x = 10

if x > 0
    println("$x is positive")
elseif x < 0
    println("$x is negative")
else
    println("$x is zero")
end

# Ternary operator
result = x > 0 ? "positive" : "not positive"
println("Using ternary: $x is $result")

println("\n=== For Loops ===")
# Basic for loop
println("Counting 1 to 5:")
for i in 1:5
    println("  Count: $i")
end

# Loop over array
fruits = ["apple", "banana", "orange"]
println("Fruits:")
for fruit in fruits
    println("  I like $fruit")
end

# Loop with index
println("Fruits with index:")
for (i, fruit) in enumerate(fruits)
    println("  $i: $fruit")
end

# Nested loops
println("Multiplication table (3x3):")
for i in 1:3
    for j in 1:3
        print("$(i*j)\t")
    end
    println()
end

println("\n=== While Loops ===")
# While loop
count = 1
println("While loop counting:")
while count <= 5
    println("  Count: $count")
    count += 1
end

# Break and continue
println("Numbers 1-10, skipping 5:")
for i in 1:10
    if i == 5
        continue  # Skip this iteration
    end
    if i == 8
        break     # Exit the loop
    end
    println("  $i")
end

println("\n=== List Comprehensions ===")
# Create arrays using comprehensions
squares = [x^2 for x in 1:5]
println("Squares: $squares")

# Conditional comprehension
even_squares = [x^2 for x in 1:10 if x % 2 == 0]
println("Even squares: $even_squares")

# 2D comprehension
matrix = [i + j for i in 1:3, j in 1:3]
println("Matrix from comprehension:")
println(matrix)

println("\n=== Exception Handling ===")
# Try-catch blocks
function safe_divide(a, b)
    try
        result = a / b
        return result
    catch e
        if isa(e, DivideError)
            println("Error: Cannot divide by zero!")
            return nothing
        else
            println("Unexpected error: $e")
            return nothing
        end
    end
end

println("10 / 2 = ", safe_divide(10, 2))
println("10 / 0 = ", safe_divide(10, 0))

println("\n=== Pattern Matching (Simple) ===")
# Function with different behaviors based on input
function describe_number(n)
    if n == 0
        return "zero"
    elseif n == 1
        return "one"
    elseif n < 0
        return "negative"
    elseif n > 100
        return "large positive"
    else
        return "positive"
    end
end

test_numbers = [0, 1, -5, 42, 150]
for num in test_numbers
    println("$num is $(describe_number(num))")
end

println("\n=== Short-Circuit Evaluation ===")
# && (and) and || (or) operators
a = 5
b = 0

# This won't cause division by zero because of short-circuit evaluation
b != 0 && println("a/b = $(a/b)")  # Only executes if b != 0
b == 0 || println("This won't print")  # Only executes if b == 0 is false

println("Short-circuit evaluation prevented division by zero!")