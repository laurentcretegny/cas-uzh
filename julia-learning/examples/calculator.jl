# Simple Calculator Example

function calculator()
    println("=== Simple Calculator ===")
    println("Available operations: +, -, *, /, ^, sqrt")
    println("Type 'quit' to exit")
    
    while true
        print("\nEnter operation (e.g., '5 + 3' or 'sqrt 16'): ")
        input = readline()
        
        if lowercase(input) == "quit"
            println("Goodbye!")
            break
        end
        
        try
            # Handle sqrt separately
            if startswith(lowercase(input), "sqrt")
                number_str = strip(replace(input, r"sqrt\s*" => ""))
                number = parse(Float64, number_str)
                result = sqrt(number)
                println("√$number = $result")
                continue
            end
            
            # Parse regular operations
            parts = split(input)
            if length(parts) != 3
                println("Invalid format. Use: number operator number")
                continue
            end
            
            a = parse(Float64, parts[1])
            operator = parts[2]
            b = parse(Float64, parts[3])
            
            result = if operator == "+"
                a + b
            elseif operator == "-"
                a - b
            elseif operator == "*"
                a * b
            elseif operator == "/"
                if b == 0
                    println("Error: Division by zero!")
                    continue
                end
                a / b
            elseif operator == "^"
                a ^ b
            else
                println("Unknown operator: $operator")
                continue
            end
            
            println("$a $operator $b = $result")
            
        catch e
            println("Error: Invalid input. Please try again.")
        end
    end
end

# Uncomment the line below to run the calculator interactively
# calculator()

# Example calculations for demonstration
println("=== Calculator Demo ===")
println("5 + 3 = ", 5 + 3)
println("10 - 4 = ", 10 - 4)
println("6 * 7 = ", 6 * 7)
println("15 / 3 = ", 15 / 3)
println("2 ^ 8 = ", 2 ^ 8)
println("√16 = ", sqrt(16))