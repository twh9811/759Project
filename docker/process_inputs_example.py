import sys

def main():
    # Taint Propagation
    arg1 = sys.argv[1]
    
    # Taint Sink
    print(arg1)

if __name__ == "__main__":
    main()
