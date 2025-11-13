# Functions in Julia

# Simple function definition
function greet(name)
    return "Hello, $(name)!"
end

# Compact function definition
square(x) = x^2

# Function with multiple arguments
function add_numbers(a, b)
    return a + b
end

# Function with optional arguments (default values)
function power(base, exponent=2)
    return base^exponent
end

# Function with keyword arguments
function create_person(name; age=0, city="Unknown")
    return "Name: $name, Age: $age, City: $city"
end

# Multiple dispatch - same function name, different argument types
function describe(x::Int)
    return "This is an integer: $x"
end

function describe(x::Float64)
    return "This is a float: $x"
end

function describe(x::String)
    return "This is a string: $x"
end

# Anonymous functions (lambdas)
multiply_by_two = x -> x * 2

# Higher-order functions
numbers = [1, 2, 3, 4, 5]
squared_numbers = map(x -> x^2, numbers)

# Test the functions
println("=== Function Examples ===")
println(greet("World"))
println("Square of 7: ", square(7))
println("Add 3 + 5: ", add_numbers(3, 5))

println("\nPower function:")
println("2^3 = ", power(2, 3))
println("5^2 (default) = ", power(5))

println("\nKeyword arguments:")
println(create_person("Alice"))
println(create_person("Bob", age=25, city="Zurich"))

println("\nMultiple dispatch:")
println(describe(42))
println(describe(3.14))
println(describe("Hello"))

println("\nAnonymous functions:")
println("Multiply 6 by 2: ", multiply_by_two(6))
println("Original numbers: ", numbers)
println("Squared numbers: ", squared_numbers)

# Function returning multiple values
function stats(numbers)
    return sum(numbers), length(numbers), sum(numbers)/length(numbers)
end

total, count, average = stats([1, 2, 3, 4, 5])
println("\nMultiple return values:")
println("Total: $total, Count: $count, Average: $average")