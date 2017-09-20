(ql:quickload "cl-dot")


;; Conses
(defmethod cl-dot:graph-object-node ((graph (eql 'example)) (object cons))
  (make-instance 'cl-dot:node
                 :attributes '(:label "cell \\N"
                               :shape :box)))

(defmethod cl-dot:graph-object-points-to ((graph (eql 'example)) (object cons))
  (list (car object)
        (make-instance 'cl-dot:attributed
                       :object (cdr object)
                       :attributes '(:weight 3))))
;; Symbols
(defmethod cl-dot:graph-object-node ((graph (eql 'example)) (object symbol))
  (make-instance 'cl-dot:node
                 :attributes `(:label ,object
                               :shape :hexagon
                               :style :filled
                               :color :black
                               :fillcolor "#ccccff")))


(let* ((data '(a b c #1=(b z) c d #1#))
       (dgraph (cl-dot:generate-graph-from-roots 'example (list data))))
  (cl-dot:dot-graph dgraph "test.png" :format :png))

(let* ((data '(a b c #1=(b z) c d #1#))
       (dgraph (cl-dot:generate-graph-from-roots 'example (list data)
                                                 '(:rankdir "LR"))))
  (cl-dot:dot-graph dgraph "test-lr.png" :format :png))
