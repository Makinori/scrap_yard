def list_tree_to_list(list_tree):
  # make nested list flatten 
  # <ex>
  #list_tree_to_list([[1,2,3], 4, [5,6, [7, 8, [[],[9,10]], 11]], 12])
  # >> [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
  if list_tree == []:
    return []
  if isinstance(list_tree, list):
    caar = list_tree_to_list(list_tree[0])
    cdar = list_tree_to_list(list_tree[1:])
    return caar + cdar
  else :
    return [list_tree]
