# Gentili & Giacomello (2017) Balance Sheet Model (Julia)

This is a tiny Julia app that implements the linear algebra model of balance sheet dynamics described on pages 16–17 of Gentili & Giacomello (2017).

Model:
- State vector `S = [Cash, Equipment, AccDepreciation, CapitalStock]`.
- Transactions vector `c = [ca, cb, cc, cd]` for each period.
- Update rule: `S_next = M * (S + c)` where

```
M = [ -1  0  1  1
       1  0  0  0
       0  1  0  0
       0  0  1  0 ]
```

## Quick start

Run the script (uses built-in example `c = [80,20,100,30]` if no input given):

```bash
julia gentili_model.jl
```

Run with CSV input (one row per period, header must be `ca,cb,cc,cd`):

```bash
julia gentili_model.jl --input example_transactions.csv
```

Specify an initial state `S0` (comma-separated, order: Cash,Equipment,AccDepreciation,CapitalStock):

```bash
julia gentili_model.jl --input example_transactions.csv --s0 0,0,0,0
```

## Input format

- CSV with header `ca,cb,cc,cd` (case-insensitive)
- Each subsequent row is the transaction vector for a period.

Example (`example_transactions.csv`):

```
ca,cb,cc,cd
80,20,100,30
```

## Notes
- The script uses the standard library `DelimitedFiles` (no external dependencies).
- Output prints account names and balances after each period.
