class Folder:
    def __init__(self, name):
        self.name = name
        self.files = []
        self.subfolders = []

    # Add a file
    def add_file(self, file_name):
        self.files.append(file_name)
        print(f"Added file '{file_name}' to folder '{self.name}'.")

    # Add a subfolder (unique names enforced in menu)
    def add_subfolder(self, folder_obj):
        self.subfolders.append(folder_obj)
        print(f"Added subfolder '{folder_obj.name}' under '{self.name}'.")

    # Select folder by name (search entire tree)
    def select_folder(self, name):
        if self.name == name:
            return self
        for sf in self.subfolders:
            found = sf.select_folder(name)
            if found:
                return found
        return None

    # Private method to count files recursively
    def __count_files(self):
        total = len(self.files)
        for sf in self.subfolders:
            total += sf.__count_files()
        return total

    # Total number of files including subfolders
    def __len__(self):
        return self.__count_files()

    # Compare folder to string by name
    def __eq__(self, other):
        return isinstance(other, str) and self.name == other

    # String representation with indentation
    def __str__(self, indent=0):
        space = "    " * indent
        result = f"{space}📁 {self.name}\n"
        for f in self.files:
            result += f"{space}    - {f}\n"
        for sf in self.subfolders:
            result += sf.__str__(indent + 1)
        return result


# Helper to check global folder name uniqueness
def name_exists(root, name):
    return root.select_folder(name) is not None

# Helper to get depth of a folder from root
def get_depth(root, folder_name):
    path = []

    def helper(node):
        path.append(node.name)
        if node.name == folder_name:
            return True
        for child in node.subfolders:
            if helper(child):
                return True
        path.pop()
        return False

    if helper(root):
        return len(path) - 1
    return None


# ------------------ MENU ------------------
def main():
    root_name = input("Enter root folder name (default 'root'): ").strip() or "root"
    root = Folder(root_name)
    current = root

    while True:
        print("\n--- MENU ---")
        print(f"Current folder: {current.name}")
        print("1) Add file")
        print("2) Add subfolder")
        print("3) Select folder")
        print("4) Print current folder structure")
        print("5) Print entire tree from root")
        print("6) Count total files in current folder")
        print("0) Exit")
        choice = input("Choose: ").strip()

        if choice == "1":
            fname = input("File name: ").strip()
            if fname:
                current.add_file(fname)
            else:
                print("Cancelled: empty file name.")

        elif choice == "2":
            fname = input("Subfolder name: ").strip()
            if not fname:
                print("Cancelled: empty folder name.")
                continue
            if name_exists(root, fname):
                print(f"A folder named '{fname}' already exists in the tree.")
                continue
            cur_depth = get_depth(root, current.name)
            if cur_depth is None:
                print("Error finding current folder depth.")
                continue
            if cur_depth + 1 > 3:
                print("Cannot add subfolder: would exceed max depth 3.")
                continue
            new_folder = Folder(fname)
            current.add_subfolder(new_folder)

        elif choice == "3":
            fname = input("Folder name to select: ").strip()
            found = root.select_folder(fname)
            if found:
                current = found
                print(f"Current folder is now '{current.name}'.")
            else:
                print("Folder not found.")

        elif choice == "4":
            print("\nCurrent folder structure:")
            print(current)

        elif choice == "5":
            print("\nEntire tree from root:")
            print(root)

        elif choice == "6":
            print(f"Total files in '{current.name}': {len(current)}")

        elif choice == "0":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
