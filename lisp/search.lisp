
;;;; search graph

(defparameter *graph*
  '((a b c d )
    (b c )
    (c d )
    (d a)))


(defvar *graph2*
  '((A B C)
    (B A C D)
    (C A B E)
    (D B E F)
    (E C D G)
    (F D)
    (G E)))

(defun search-all-path (goal stack graph)
  (let* ((now-path (car stack))
         (now-node (car now-path))
         (next-nodes (remove-if #'(lambda (node) (member node now-path))
                                (find-if #'(lambda (nodes) (equal (car nodes) now-node))
                                         graph)))
         (next-stack (concatenate 
                      'list
                      (cdr stack)
                      (mapcar #'(lambda (node) (cons node now-path))
                              next-nodes))))
    (cond ((equal now-node goal) 
           (concatenate 'list 
                        (list (reverse now-path))
                        (search-all-path goal next-stack graph)))
          (next-stack (search-all-path goal next-stack graph))
          (t nil))))
         

(defun search-path (goal stack graph)
  (let* ((now-node (caar stack))
         (next-nodes (cdr (find-if #'(lambda (node) (equal (car node) now-node))
                                   graph)))
         (next-graph (remove-if #'(lambda (node) (equal (car node) now-node))
                                graph)))
    (cond ((equal now-node goal) (reverse (car stack)))
          ((null next-nodes) nil)
          ((null next-nodes) nil)
          (t (search-path 
              goal 
              (concatenate 'list 
                           (cdr stack)
                           (mapcar #'(lambda (node)
                                       (cons node (car stack)))
                                   next-nodes))
              next-graph)))))

