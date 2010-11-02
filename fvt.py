#!/usr/bin/env python
# encoding: utf-8
"""
fvt.py

Copyright (c) 2010 Piick.com, Inc. All rights reserved.
"""

from lxml import etree


class Node(object):
  def __init__(self, el=None):
    if el is not None:
      self.value = el.tag
      self.children = []
      self.size = 1

      if el.text and el.text.strip():
        text_node = Node()
        text_node.value = el.text.strip()
        self.children.append(text_node)
        self.size += text_node.size

      for c in el:
        n = Node(c)
        self.children.append(n)
        self.size += n.size
        
        if c.tail and c.tail.strip():
          tail_node = Node()
          tail_node.value = c.tail.strip()
          self.children.append(tail_node)
          self.size += tail_node.size
    else:
      self.children = []
      self.value = None
      self.size = 1
    
  def __eq__(self, other):
    return self.value == other.value

  def __ne__(self, other):
    return not self.__eq__(other)
    
  def __iter__(self):
    for c in self.children:
      yield c
      
  def __len__(self):
    return len(self.children)

  def iter(self):
    yield self
    for c in self.children:
      for n in c.iter():
        yield n


def tree_matching(A,B):
  M = [[0.0 for j in xrange(len(B) + 1)] for i in xrange(len(A) + 1)]
  for i, a in enumerate(A, 1):
    for j, b in enumerate(B, 1):
      M[i][j] = max(M[i][j-1], M[i-1][j], M[i-1][j-1] + tree_matching(a, b))
  return M[len(A)][len(B)] + (1 if A == B else 0)

def fiva_tree_match_score(A, B):
  if A != B:
    return 0
  if not len(A) or not len(B) or len(A) == len(B):
    return 2 * tree_matching(A, B) / (A.size + B.size)

  score = 0.0
  for cA in A:
    node_score = 0.0
    match_no = 0
    for cB in B:
      tmp = 2 * tree_matching(cA, cB) / (cA.size + cB.size)
      if tmp > 0.5:
        node_score += tmp
        match_no += 1
    if match_no > 0:
      node_score = node_score / match_no
    score += node_score
  return (score / len(A)) + 2 / (A.size + B.size)

def recognize_peer_node(M):
  pass

def repeat_mining(child_list, N):
  return []
  
  
def is_aligned(M):
  return True
  
def matrix_alignment(M):
  return []

def merge_optional(child_list):
  pass

def multiple_tree_merge(T, P=None):
  M = [[None for i in xrange(len(T))] for j in xrange(max([len(t) for t in T]))]

  for i, t in enumerate(T):
    for j, c in enumerate(t):
      M[j][i] = c

  recognize_peer_node(M)
  child_list = repeat_mining(matrix_alignment(M), 1)
  merge_optional(child_list)
  
  for c in child_list:
    P.append(multiple_tree_merge(peer_node(c, M), tag(c)) if len(c) else c)

  return P



if __name__ == "__main__":
  H = ["<html><head></head><body> <b>Book Name</b> Databases<br/> <b>Author</b> John </body></html>",
       "<html><head></head><body> <b>Book Name</b> Operating Systems<br/> <b>Author</b> Jason </body></html>",
      ]
  T = [Node(etree.fromstring(h)) for h in H]

#  for a, b in zip(T[0].iter(), T[1].iter()): print "\t%s\t%s\t%s\t%d\t%d\t%d\t%d\t%f\t%f" % (a.value, b.value, str(a == b), len(a), len(b), a.size, b.size, fiva_tree_match_score(a, b), tree_matching(a,b))

  print tree_matching(T[0], T[1])
  print fiva_tree_match_score(T[0], T[1])
  print multiple_tree_merge(T)
  
