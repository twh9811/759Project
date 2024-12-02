import sys

def main():
    # We can determine arg1 is input_text and arg2 is user_input_var based on the order they appear in the action.
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    print(arg1)
    print(arg2)

if __name__ == "__main__":
    main()
