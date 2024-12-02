import sys

def main():
    # We can determine arg1 is input_text and arg2 is user_input_var based on the order they appear in the action.
    
    # Taint Propagation
    arg1 = sys.argv[1]
    # Taint Propagation
    arg2 = sys.argv[2]
    
    # Taint Sink
    print(arg1)
    # Taint Sink
    print(arg2)

if __name__ == "__main__":
    main()
