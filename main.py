from algorithms import bfs, ucs

def main():
    choice = input("Choose algorithm (bfs/ucs): ").strip().lower()
    if choice == "bfs":
        bfs.main()
    elif choice == "ucs":
        ucs.main()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
