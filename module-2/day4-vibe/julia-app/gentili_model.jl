#!/usr/bin/env julia

# Small Julia app implementing the Gentili & Giacomello (2017) page 16–17 model
# Balance sheet dynamics as a linear map applied to prior state plus transactions.

using DelimitedFiles

const ACCOUNT_NAMES = [
    "Cash",
    "Equipment",
    "AccDepreciation",
    "CapitalStock",
]

# Posting matrix M derived from the scalar equations in the paper:
# Cashₙ   = −(Cashₙ₋₁+caₙ) + (AccDepₙ₋₁+ccₙ) + (CapStkₙ₋₁+cdₙ)
# Equipₙ  =  (Cashₙ₋₁+caₙ)
# AccDepₙ =  (Equipₙ₋₁+cbₙ)
# CapStkₙ =  (AccDepₙ₋₁+ccₙ)
const M = [
    -1.0  0.0  1.0  1.0;
     1.0  0.0  0.0  0.0;
     0.0  1.0  0.0  0.0;
     0.0  0.0  1.0  0.0;
]

"""
    step(S_prev::Vector{<:Real}, c::Vector{<:Real}) -> Vector{Float64}

Compute next-period balance sheet S = M * (S_prev + c).
Vectors must be of length 4: [Cash, Equipment, AccDepreciation, CapitalStock].
"""
function step(S_prev::Vector{<:Real}, c::Vector{<:Real})
    length(S_prev) == 4 || error("S_prev must have length 4")
    length(c) == 4 || error("transactions vector c must have length 4")
    v = Float64.(S_prev) .+ Float64.(c)
    return M * v
end

"""
    parse_s0(s::AbstractString) -> Vector{Float64}

Parse a comma-separated list like "0,0,0,0" to a 4-vector.
"""
function parse_s0(s::AbstractString)
    parts = split(strip(s), [',', ';', ' '])
    parts = filter(!isempty, parts)
    length(parts) == 4 || error("--s0 must have 4 numbers (Cash,Equipment,AccDepreciation,CapitalStock)")
    return [parse(Float64, x) for x in parts]
end

"""
    read_transactions_csv(path::AbstractString) -> Vector{Vector{Float64}}

Read a CSV with header containing four columns (case-insensitive):
ca, cb, cc, cd. Returns a vector of 4-vectors (one per row/period).
"""
function read_transactions_csv(path::AbstractString)
    open(path, "r") do io
        header_line = readline(io)
        headers = lowercase.(split(strip(header_line), ','))
        # Accept minor variations/spaces
        headers = strip.(headers)
        # Expected canonical order
        expected = ["ca", "cb", "cc", "cd"]
        length(headers) == 4 || error("CSV must have exactly 4 columns: ca,cb,cc,cd")
        # Map current column positions to expected order
        idxmap = Dict{String,Int}()
        for (i,h) in enumerate(headers)
            idxmap[h] = i
        end
        all(h -> haskey(idxmap, h), expected) || error("CSV header must include: ca, cb, cc, cd")
        rows = Vector{Vector{Float64}}()
        for (k, line) in enumerate(eachline(io))
            lineno = k + 1  # account for header line
            line = strip(line)
            isempty(line) && continue
            cols = split(line, ',')
            length(cols) >= 4 || error("Line $lineno: expected 4 values, got $(length(cols))")
            vals = Vector{Float64}(undef, 4)
            for (j, key) in enumerate(expected)
                val = strip(cols[idxmap[key]])
                vals[j] = parse(Float64, val)
            end
            push!(rows, vals)
        end
        return rows
    end
end

function print_state(S::AbstractVector{<:Real}; prefix::AbstractString="")
    @assert length(S) == 4
    println(prefix, join(("$(ACCOUNT_NAMES[i])=$(round(S[i]; digits=6))" for i in 1:4), ", "))
end

function usage()
    println("Usage: julia gentili_model.jl [--input transactions.csv] [--s0 a,b,c,d]")
    println("  --input/-i: CSV with header ca,cb,cc,cd; each row is a period")
    println("  --s0: initial balances (Cash,Equipment,AccDepreciation,CapitalStock); default 0,0,0,0")
    println("If no input is provided, runs the paper's example: c = [80,20,100,30]")
end

function main()
    # Defaults
    input_path::Union{Nothing,String} = nothing
    S0 = [0.0, 0.0, 0.0, 0.0]

    i = 1
    while i <= length(ARGS)
        arg = ARGS[i]
        if arg == "--help" || arg == "-h"
            usage(); return
        elseif arg == "--input" || arg == "-i"
            i += 1; i <= length(ARGS) || error("--input requires a path")
            input_path = ARGS[i]
        elseif arg == "--s0"
            i += 1; i <= length(ARGS) || error("--s0 requires a value like 0,0,0,0")
            S0 = parse_s0(ARGS[i])
        else
            error("Unknown argument: $arg")
        end
        i += 1
    end

    println("Posting matrix M:")
    show(stdout, "text/plain", M); println()
    println("Initial state S₀:")
    print_state(S0, prefix="  ")

    if input_path === nothing
        println("No input provided; running paper example with c = [80,20,100,30]")
        c = [80.0, 20.0, 100.0, 30.0]
        S1 = step(S0, c)
        println("Resulting state S₁:")
        print_state(S1, prefix="  ")
    else
        println("Reading transactions from: $input_path")
        transactions = read_transactions_csv(input_path)
        S = copy(S0)
        for (t, c) in enumerate(transactions)
            S = step(S, c)
            println("After period $t:")
            print_state(S, prefix="  ")
        end
    end
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
