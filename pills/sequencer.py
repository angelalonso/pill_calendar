#/usr/bin/env python3                                                                                                        
"""
Generates a sequence of 1s and 2s that fit into an amount per week
E.g.:
given an amount on 1.75, it will generate a sequence that can be divided into weeks:
1, 2, 2, 2, 1, 2, 2,
2, 1, 2, 2, 2, 1, 2, 
2, 2, 1, 2, 2, 2, 1, 
2, 2, 2, 1, 2, 2, 2, 
1, 2, 2, 2, 1, 2, 2, 
2, 1, 2, 2, 2, 1, 2, 
2, 2, 1, 2, 2, 2, 1, 
2, 2, 2, 1, 2, 2, 2 

, but if the amount were 1.7142857142857142, it'd only generate
1, 2, 2, 1, 2, 2, 2
, and we'd have to tell it to generate a minimum of 5,6 weeks

"""
def generate_sequence(amount, days, previous_sequence):
    if len(previous_sequence) == 0:
        sequence = [1]
    else:
        sequence = previous_sequence
    current_amount = sum(i for i in sequence) / len(sequence)

    for day in range(days - 1):
        if current_amount < amount:
            sequence.append(2)
        else:
            sequence.append(1)
        current_amount = sum(i for i in sequence) / len(sequence)
    return sequence


