import System
import clr
clr.AddReference("Grasshopper")
import Grasshopper
import ghpythonlib.treehelpers as th
import Grasshopper.Kernel.Data.GH_Path as GH_Path
import Grasshopper.DataTree as DataTree
import Rhino.Geometry as rg


def create_datatree_from_list_of_lists(list_of_lists):
    """Create a Grasshopper DataTree from a list of lists."""
    tree = DataTree[System.Object]()
    for i, l in enumerate(list_of_lists):
        path = GH_Path(i)
        tree.AddRange(l, path)
    return tree

def merge_datatrees(tree1, tree2):
    """Merge two Grasshopper DataTrees."""
    tree = DataTree[System.Object]()
    for i, branch in enumerate(tree1.Branches):
        path = GH_Path(i)
        tree.AddRange(branch, path)
    for i, branch in enumerate(tree2.Branches):
        path = GH_Path(i + tree1.BranchCount)
        tree.AddRange(branch, path)
    return tree

def merge_datatrees(tree1, tree2):
    """Merge two Grasshopper DataTrees."""
    tree = DataTree[System.Object]()
    for i, branch in enumerate(tree1.Branches):
        path = GH_Path(i)
        tree.AddRange(branch, path)
    for i, branch in enumerate(tree2.Branches):
        path = GH_Path(i + tree1.BranchCount)
        tree.AddRange(branch, path)
    return tree