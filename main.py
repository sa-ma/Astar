from algorithms import bfs, dfs, ucs, astar

def main():
    choice = input("Choose algorithm (bfs/dfs/ucs/astar): ").strip().lower()
    if choice == "bfs":
        bfs.main()
    elif choice == "dfs":
        dfs.main()   
    elif choice == "ucs":
        ucs.main()
    elif choice == "astar":
        astar.main()
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()
