# Data Structures in Julia

println("=== Arrays ===")
# Arrays (1-indexed, like MATLAB and R)
numbers = [1, 2, 3, 4, 5]
println("Array: ", numbers)
println("First element: ", numbers[1])  # 1-indexed!
println("Last element: ", numbers[end])
println("Length: ", length(numbers))

# Array operations
push!(numbers, 6)  # Add element to end
println("After push: ", numbers)
pop!(numbers)      # Remove last element
println("After pop: ", numbers)

# Array slicing
println("Elements 2-4: ", numbers[2:4])
println("Every other element: ", numbers[1:2:end])

# 2D Arrays (Matrices)
matrix = [1 2 3; 4 5 6; 7 8 9]
println("\n=== Matrices ===")
println("Matrix:")
println(matrix)
println("Element at (2,3): ", matrix[2, 3])
println("Second row: ", matrix[2, :])
println("Third column: ", matrix[:, 3])

# Array comprehensions
squares = [x^2 for x in 1:5]
println("\nSquares using comprehension: ", squares)

# Conditional comprehensions
even_squares = [x^2 for x in 1:10 if x % 2 == 0]
println("Even squares: ", even_squares)

println("\n=== Tuples ===")
# Tuples (immutable)
point = (3, 4)
println("Point: ", point)
println("X coordinate: ", point[1])
println("Y coordinate: ", point[2])

# Named tuples
person = (name="Alice", age=30, city="Zurich")
println("Person: ", person)
println("Name: ", person.name)
println("Age: ", person.age)

println("\n=== Dictionaries ===")
# Dictionaries
ages = Dict("Alice" => 30, "Bob" => 25, "Charlie" => 35)
println("Ages dictionary: ", ages)
println("Alice's age: ", ages["Alice"])

# Add new entry
ages["Diana"] = 28
println("After adding Diana: ", ages)

# Check if key exists
if haskey(ages, "Bob")
    println("Bob is in the dictionary")
end

# Iterate over dictionary
println("All entries:")
for (name, age) in ages
    println("  $name: $age years old")
end

println("\n=== Sets ===")
# Sets (unique elements)
fruits = Set(["apple", "banana", "apple", "orange"])
println("Fruits set: ", fruits)
println("Contains apple: ", "apple" in fruits)

# Set operations
vegetables = Set(["carrot", "potato", "tomato"])
all_food = union(fruits, vegetables)
println("All food: ", all_food)

println("\n=== Ranges ===")
# Ranges
range1 = 1:10
println("Range 1-10: ", range1)
println("Collect to array: ", collect(range1))

range2 = 1:2:20  # start:step:stop
println("Odd numbers 1-20: ", collect(range2))

# String operations
println("\n=== String Operations ===")
text = "Hello, Julia World!"
println("Original: ", text)
println("Length: ", length(text))
println("Uppercase: ", uppercase(text))
println("Split by comma: ", split(text, ","))
println("Replace Julia with Python: ", replace(text, "Julia" => "Python"))