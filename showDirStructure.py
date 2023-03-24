import os

def list_folders(startpath):
    output = ""
    for root, dirs, _ in os.walk(startpath):
        if '.git' in dirs:
            dirs.remove('.git')  # Ignore .git folder

        # ignore .vscode, .svelte-kit, node_modules
        for d in dirs:
            if d.startswith('.'):
                dirs.remove(d)

        if "node_modules" in dirs:
            dirs.remove("node_modules")
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        output += '{}{}/\n'.format(indent, os.path.basename(root))
    return output

if __name__ == "__main__":
    start_path = os.getcwd()
    print("Directory structure of '{}':\n".format(start_path))
    print(list_folders(start_path))
