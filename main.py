import os
import platform
from Objects import *
import re


# Main method
def main():
    # Make list of Attribute objects
    myAttributes = []
    myConstraints = []
    myPenalties = []
    myPossibilistics = []
    myQualitatives = []
    parse_attributes_file("Attributes.txt", myAttributes)
    parse_constraints_file("Constraints.txt", myAttributes, myConstraints)
    parse_logic_file("Logics.txt", myPenalties, myPossibilistics, myQualitatives, myAttributes)

    # Call Clasp and write to file
    os.system("clasp CNF.txt -n 0 > CLASPOutput.txt")


# Parses the Attributes file from Words to Binary Logic (Stored in list of Attribute objects)
def parse_attributes_file(file_name, attributes):
    # Open file pointer to read lines
    input_file = open(file_name, "r")
    Lines = input_file.readlines()

    # Start parsing Attribute File
    i = 0
    for line in Lines:
        # Initialize new Attribute object and add to list
        attributes.append(Attribute())
        # Use regex to parse lines into variables and assign to attribute object
        tokens = re.split(r"[:,\s\n]+", line)
        attributes[i].name = tokens[0]
        attributes[i].op1 = tokens[1]
        attributes[i].op2 = tokens[2]
        attributes[i].numop1 = i + 1
        attributes[i].numop2 = -i - 1

        # Iterate variable
        i += 1
    # Print attributes (From Objects.py)
    print_attributes(attributes)
    input_file.close()


# Writes Hard Constraints in CNF format to feed to Clasp
def write_to_cnf(constraints, file_name):
    output_file = open(file_name, "w")
    for line in constraints:
        output_file.write(line.output)
    output_file.close()


# Parses the Hard Constraints file from Words to Binary Logic(Stored in list of Constraint objects)
def parse_constraints_file(file_name, attributes, constraints):
    # Open file pointer to read lines
    input_file = open(file_name, "r")
    Lines = input_file.readlines()

    # Start parsing the file
    # Add "p cnf" header to CNF output
    constraints.append(Constraint())
    constraints[0].output = "p cnf " + str(len(attributes)) + " " + str(len(Lines)) + "\n"
    # Body of CNF file
    i = 0
    for line in Lines:
        # Initialize new constraint Object
        constraints.append(Constraint())

        # Split line into tokens
        constraints[i].input = line
        tokens = re.split(r"[\n\s]", line)

        # Parse tokens using attribute object (Compatible with any type of file)
        j = 0
        while j < len(tokens):
            if tokens[j] == "NOT":
                k = 0
                while (tokens[j+1] != attributes[k].op1) & (tokens[j+1] != attributes[k].op2):
                    k += 1
                if tokens[j+1] == attributes[k].op1:
                    constraints[i].output += " " + str(attributes[k].numop2)
                if tokens[j+1] == attributes[k].op2:
                    constraints[i].output += " " + str(attributes[k].numop1)
                j += 2
                continue
            # Case: OR condition
            elif tokens[j] == "OR":
                # Iterative variable
                j += 1
                continue
            # Case: for EOL and random empty blo
            elif tokens[j] == '':
                break
            else:
                k = 0
                while ((tokens[j] != attributes[k].op1) & (tokens[j] != attributes[k].op2)):
                    # Iterative variable
                    k += 1
                if tokens[j] == attributes[k].op1:
                    constraints[i].output += " " + str(attributes[k].numop1)
                if tokens[j] == attributes[k].op2:
                    constraints[i].output += " " + str(attributes[k].numop2)
            # Iterative variable
            j += 1
        # Add a new line to output
        constraints[i].output += " 0\n"

    # Print out constraints output
    write_to_cnf(constraints, "CNF.txt")

    # Close file stream
    input_file.close()

# Parses Logic file to save into Object lists
def parse_logic_file(file_name, penalties, possibilistics, qualitatives, attributes):
    # Open and read file lines
    input_file = open(file_name, "r")
    Lines = input_file.readlines()

    # Create str to hold Logic inputs
    pen_input = []
    possib_input = []
    qual_input = []

    # Split up File into respective Logic inputs
    # Penalty
    i = 0
    while(Lines[i] != "\n"):
        pen_input.append(Lines[i].split("\n"))
        i += 1
    i += 2
    # Possibilistic
    while (Lines[i] != "\n"):
        possib_input.append(Lines[i].split("\n"))
        i += 1
    # Qualitative Form
    i += 2
    while i < len(Lines):
        qual_input.append(Lines[i].split("\n"))
        i += 1

    # For Testing
    # print(pen_input)
    # print(possib_input)
    # print(qual_input)

    # Call parse functions to store Logics in respective Objects
    parse_penalty_logic(pen_input, penalties, attributes)
    parse_possibilistic_logic(possib_input, possibilistics, attributes)
    # parse_qualitative_logic(qual_input, qualitatives)

# Parses penalty logic into Object Penalty format
def parse_penalty_logic(pen_input, penalties, attributes):
    i = 1
    penalties.append(Penalty())
    while i < len(pen_input):
        # Add new Penalty object to list
        penalties.append(Penalty())

        # Split line into tokens
        penalties[i].input = pen_input[i]
        tokens = re.split(r'[,]+', pen_input[i][0])
        penalties[i].penalty = tokens[1]
        tokens = tokens[0].split(" ")
        print(tokens)

        j = 0
        while j < len(tokens):
            # Case: NOT condition
            if tokens[j] == "NOT":
                k = 0
                while (tokens[j + 1] != attributes[k].op1) & (tokens[j + 1] != attributes[k].op2):
                    k += 1
                if tokens[j + 1] == attributes[k].op1:
                    penalties[i].output += str(attributes[k].numop2) + " "
                if tokens[j + 1] == attributes[k].op2:
                    penalties[i].output += str(attributes[k].numop1) + " "
                j += 2
                continue
            # Case: OR condition
            elif tokens[j] == "OR":
                # Iterative variable
                j += 1
                continue
            # Case: for EOL and random empty block
            elif tokens[j] == '':
                break
                # Case: AND condition
            elif tokens[j] == "AND":
                penalties[i].output += "\n"
                j += 1
                continue
            else:
                k = 0
                while (tokens[j] != attributes[k].op1) & (tokens[j] != attributes[k].op2):
                    # Iterative variable
                    k += 1
                if tokens[j] == attributes[k].op1:
                    penalties[i].output += str(attributes[k].numop1) + " "
                if tokens[j] == attributes[k].op2:
                    penalties[i].output += str(attributes[k].numop2) + " "
            # Iterative variable
            j += 1
        i += 1

   # for pen in penalties:
       # print(pen.output + pen_pen)



def parse_possibilistic_logic(possib_input, possibilistics, attributes):
    i = 1
    possibilistics.append(Possibilistic())
    while i < len(possib_input):
        # Add new Penalty object to list
        possibilistics.append(Possibilistic())

        # Split line into tokens
        possibilistics[i].input = possib_input[i]
        tokens = re.split(r'[,]+', possib_input[i][0])
        possibilistics[i].tol = tokens[1]
        tokens = tokens[0].split(" ")
        print(tokens)

        j = 0
        while j < len(tokens):
            # Case: NOT condition
            if tokens[j] == "NOT":
                k = 0
                while (tokens[j + 1] != attributes[k].op1) & (tokens[j + 1] != attributes[k].op2):
                    k += 1
                if tokens[j + 1] == attributes[k].op1:
                    possibilistics[i].output += str(attributes[k].numop2) + " "
                if tokens[j + 1] == attributes[k].op2:
                    possibilistics[i].output += str(attributes[k].numop1) + " "
                j += 2
                continue
            # Case: OR condition
            elif tokens[j] == "OR":
                # Iterative variable
                j += 1
                continue
            # Case: for EOL and random empty block
            elif tokens[j] == '':
                break
                # Case: AND condition
            elif tokens[j] == "AND":
                possibilistics[i].output += "\n"
                j += 1
                continue
            else:
                k = 0
                while (tokens[j] != attributes[k].op1) & (tokens[j] != attributes[k].op2):
                    # Iterative variable
                    k += 1
                if tokens[j] == attributes[k].op1:
                    possibilistics[i].output += str(attributes[k].numop1) + " "
                if tokens[j] == attributes[k].op2:
                    possibilistics[i].output += str(attributes[k].numop2) + " "
            # Iterative variable
            j += 1
        i += 1

    for possib in possibilistics:
        print(possib.output)

# TODO: Last thing that we will do
# def parse_qualitative_logic(qual_input, poissibilistics)


# Call main
main()
