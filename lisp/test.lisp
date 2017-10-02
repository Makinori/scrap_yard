(defun flatten-tree (test-end next-tree-list tree &optional (stage 0))
  (show-param stage "=======================" "")
  (show-param stage "time" stage)
  (show-param stage "tree" tree)
  (unless (show-param stage "test" (funcall test-end tree))
    (show-param stage "naxt" (funcall next-tree-list tree)))
  (let ((retu
         (cond 
           ((null tree) nil)
           ((funcall test-end tree)  tree)
           (t (flatten (mapcar
                        #'(lambda (next-tree)
                            (flatten-tree test-end next-tree-list next-tree
                                          (+ stage 1)
                                          ))
                        (funcall next-tree-list tree)))))))
    (show-param stage "retu" retu)))
