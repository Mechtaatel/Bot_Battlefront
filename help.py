a = [1914,11,4,228,13,66,77,666,667,69,222,8,99]

def merge_sort(a):
  if len(a)<2: 
    return a[:] 
  else:
    median = int(len(a)/2)
    left = merge_sort(a[:median])
    right = merge_sort(a[median:])
    return merge(left,right)
def merge(left,right):
  res = []
  i,j = 0,0
  while i<len(left) and j<len(right):
    if left[i] < right[j]:
      res.append(left[i])
      i +=1
    else:
      res.append(right[j])
      j += 1
  while i < len(left):
    res.append(left[i])
    i += 1
  while j < len(right):
    res.append(right[j])
    j +=1
  return res


print(merge_sort(a))
