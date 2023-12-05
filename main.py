# 0.IMPORT AND INSTALL
#(https://dreampuf.github.io/GraphvizOnline/) to visualize the DOT files as images. need to download it /add path to sys vars & import it later.
#pip install graphviz
from graphviz import Digraph

# 1. QUICK SORT
# Function to perform quicksort
def quicksort(arr, depth=0):
    if not arr:
        return "", []
    else:
        pivot = arr[0]
    left = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]

    tree_str = f'"{pivot}" [label="{pivot}"];\n'
    tree_str += quicksort(left, depth + 1)[0]
    tree_str += quicksort(right, depth + 1)[0]

    sorted_list = quicksort(left, depth + 1)[1] + [pivot] + quicksort(right, depth + 1)[1]

    return tree_str, sorted_list

def draw_quicksort_tree_dot(arr, depth=0):
    if not arr:
        return ""

    pivot = arr[0]
    left = [x for x in arr[1:] if x <= pivot]
    right = [x for x in arr[1:] if x > pivot]

    tree_str = "  " * depth + str(pivot) + "\n"
    tree_str += draw_quicksort_tree_dot(left, depth + 1)
    tree_str += draw_quicksort_tree_dot(right, depth + 1)

    return tree_str
# 2. BST
# Node class for binary search tree
class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

# Function to insert a node in the binary search tree
def insert(root, value):
    if root is None:
        return Node(value)
    if value < root.value:
        root.left = insert(root.left, value)
    else:
        root.right = insert(root.right, value)
    return root

# Function to draw the binary search tree
def draw_binary_tree_dot(root, dot, depth=0):
    if root is None:
        return ""

    tree_str = f'"{root.value}" [label="{root.value}"];\n'
    if root.left:
        tree_str += f'"{root.value}" -> "{root.left.value}";\n'
    if root.right:
        tree_str += f'"{root.value}" -> "{root.right.value}";\n'

    tree_str += draw_binary_tree_dot(root.left, dot, depth + 1)
    tree_str += draw_binary_tree_dot(root.right, dot, depth + 1)

    dot.node(f'{root.value}', label=str(root.value))

    if root.left:
        dot.edge(f'{root.value}', f'{root.left.value}')
    if root.right:
        dot.edge(f'{root.value}', f'{root.right.value}')

    return tree_str

# 3. IMPLIMENTATION
# Read the list from a text file
def read_list_from_file(filename):
    with open(filename, 'r') as file:
        return [int(line.strip()) for line in file]

# Specify the file name containing the list of numbers
file_name = 'numbers.txt'  # Change this to the actual file name

# Read the list from the file
original_list = read_list_from_file(file_name)

# Create binary search tree
binary_search_tree = None
for num in original_list:
    binary_search_tree = insert(binary_search_tree, num)

# Generate DOT source for quicksort tree and get the sorted list
quicksort_dot, quicksort_sorted_list = quicksort(original_list)

# Save DOT source to files for quicksort tree and binary search tree
with open('quicksort_tree.dot', 'w') as quicksort_file:
    quicksort_file.write(quicksort_dot)

binary_search_tree_dot = Digraph(comment='Binary Search Tree')
draw_binary_tree_dot(binary_search_tree, binary_search_tree_dot)
with open('binary_tree.dot', 'w') as binary_tree_file:
    binary_tree_file.write(binary_search_tree_dot.source)

# Render quicksort DOT file to a PNG image
quicksort_image_path = 'quicksort_tree'
dot_quicksort = Digraph(comment='Quicksort Tree')
dot_quicksort.render(quicksort_image_path, format='png', cleanup=True)

# Generate HTML content
html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tree Visualization</title>
</head>
<body>

<h1>Tree Visualization</h1>

<h2>Original List</h2>
<table border="1">
    <tr>
        <!-- Header Row -->
        {" ".join(f'<th>{i}</th>' for i in range(len(original_list)))}
    </tr>
    <tr>
        <!-- Values Row -->
        {" ".join(f'<td>{value}</td>' for value in original_list)}
    </tr>
</table>

<h2>Quicksort Tree Visualization</h2>
<img src="{quicksort_image_path}.png" alt="Quicksort Tree" style="max-width: 100%;">

<h2>Sorted List (Quicksort)</h2>
<table border="1">
    <tr>
        <!-- Header Row -->
        {" ".join(f'<th>{i}</th>' for i in range(len(quicksort_sorted_list)))}
    </tr>
    <tr>
        <!-- Values Row -->
        {" ".join(f'<td>{value}</td>' for value in quicksort_sorted_list)}
    </tr>
</table>

<h2>Binary Search Tree Visualization</h2>
<img src="{binary_search_tree_image_path}.png" alt="Binary Search Tree" style="max-width: 100%;">

</body>
</html>
'''

# 4.DISPLAYING
# Save HTML content to a file
with open('tree_visualization.html', 'w') as html_file:
    html_file.write(html_content)

# Open the HTML file in a web browser
import webbrowser
webbrowser.open('tree_visualization.html')
