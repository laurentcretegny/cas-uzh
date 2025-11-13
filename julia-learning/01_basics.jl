# Julia Basics - Variables, Types, and Operations

# Variables - no need to declare types explicitly
x = 10              # Integer
y = 3.14           # Float64
name = "Julia"     # String
is_awesome = true  # Boolean

println("Hello from Julia!")
println("x = $x, y = $y, name = $name")

# Julia has excellent type inference
println("Type of x: ", typeof(x))
println("Type of y: ", typeof(y))
println("Type of name: ", typeof(name))

# Mathematical operations
a = 5
b = 2

println("\nBasic Math:")
println("$a + $b = ", a + b)
println("$a - $b = ", a - b)
println("$a * $b = ", a * b)
println("$a / $b = ", a / b)
println("$a ^ $b = ", a ^ b)
println("$a % $b = ", a % b)

# Special mathematical constants
println("\nMath constants:")
println("π = ", π)
println("e = ", ℯ)

# String operations
first_name = "Julia"
last_name = "Lang"
full_name = first_name * " " * last_name  # String concatenation
println("\nString operations:")
println("Full name: ", full_name)
println("Length: ", length(full_name))
println("Uppercase: ", uppercase(full_name))

# Type conversion
str_number = "42"
num = parse(Int, str_number)
println("\nType conversion:")
println("String '$str_number' as number: $num")
println("Number $num as string: $(string(num))")

# Unicode support (Julia loves Unicode!)
α = 0.1
β = 0.2
γ = α + β
println("\nUnicode variables:")
println("α = $α, β = $β, γ = α + β = $γ")