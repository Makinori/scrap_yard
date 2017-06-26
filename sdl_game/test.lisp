;;;; package
(ql:quickload :lispbuilder-sdl)
(ql:quickload :lispbuilder-sdl-ttf)

(defpackage #:sdl-test
  (:use :common-lisp )
  (:export :main))

(in-package :sdl-test)




;;;; util
(defun 2darray-apply-func-coord (func array)
  (loop for i from 0 below (array-dimension array 0)
     do (loop for j from 0 below (array-dimension array 1)
           do
             (funcall func j i))))


;;;; world

(defparameter *cell-height* 16)
(defparameter *cell-width* 32)



(defparameter *world*
  #2A((1 1 1 1 1 1 1 1 1 1)
      (1 1 2 1 1 1 1 1 1 1)
      (1 1 2 1 1 1 1 1 1 1)
      (1 1 2 2 2 1 1 1 1 1) 
      (1 1 1 1 1 1 1 1 1 1)
      (1 1 1 1 1 1 1 1 1 1)
      (1 1 1 1 1 1 1 1 1 1)
      (1 1 1 1 1 1 1 1 1 1)
      (1 1 1 1 1 1 1 1 1 1)
      (1 1 1 1 1 1 1 1 1 1)
      ))

(defun id-to-color (id)
  (cond ((= id 0) (sdl:color :r 0 :g 0 :b 0))
        ((= id 1) (sdl:color :g 128))
        ((= id 2) (sdl:color :r 128))
        (t (sdl:color :r 0 :g 0 :b 0) )))


;;; isometric
(defun draw-tile (x y color)
  (let ((half-cell-h (/ *cell-height* 2))
        (half-cell-w (/ *cell-width* 2)))
    (sdl:draw-filled-polygon
     (list (sdl:point :x x :y (- y half-cell-h))
           (sdl:point :x (- x half-cell-w) :y y)
           (sdl:point :x x :y (+ y half-cell-h))
           (sdl:point :x (+ x half-cell-w) :y y)
           (sdl:point :x x :y (- y half-cell-h)))
     :color color
     )
    (sdl:draw-polygon
     (list (sdl:point :x x :y (- y half-cell-h))
           (sdl:point :x (- x half-cell-w) :y y)
           (sdl:point :x x :y (+ y half-cell-h))
           (sdl:point :x (+ x half-cell-w) :y y)
           (sdl:point :x x :y (- y half-cell-h)))
     :color (sdl:color :r 128 :g 128 :b 128)
     )
    ))



;; isometric mathmatics
(let* ((sin45 (sin (/ pi 4)))
       (sin-45 (- sin45))
       (cos45 (cos (/ pi 4)))
       
       (half-width (/ *cell-width* 2))
       (half-height (/ *cell-height* 2))
       
       (camera-x 0) (camera-y 0) (camera-zoom 1.00)
       )
  (defun isometric-reset-camera (x y zoom)
    (setf camera-x x)
    (setf camera-y y)
    (setf camera-zoom zoom))
  (defun coord-to-isometric-x (x y)
    (+ camera-x
       (* half-width (+ x (- y)))
       ))
  (defun coord-to-isometric-y (x y)
    (+ camera-y
       (* half-height (+ y x))))
  )




;; isometric draw
(defun draw-isometric-map (map)
  (isometric-reset-camera 100 100 0.90)
  (2darray-apply-func-coord
   #'(lambda (x y)
       (draw-tile (coord-to-isometric-x x y)
                  (coord-to-isometric-y x y)
                  (id-to-color (aref map y x))))
   map))



;;;; game loop
(defun main()
  (sdl:with-init ()
    (sdl:window 640 480 :title-caption "test")
    (setf (sdl:frame-rate) 30)
    (sdl:initialise-default-font sdl:*font-7x13*)
    
    (let ((current-key nil))

        
      (sdl:update-display)
      
      (sdl:with-events ()
        (:quit-event () t)
        (:key-down-event
         (:key key) 
         (if (sdl:key= key :sdl-key-space)
           (sdl:push-quit-event))
         (setf current-key key)
         (format t "pressed : ~A~%" key))           
        (:key-up-event
         (:key key)
         (setf current-key nil)
         (format t "reresed : ~A~%" key))
        
        
        (:idle
         ()
         (sdl:clear-display sdl:*black*)
         (draw-isometric-map *world*)

         (sdl:draw-string-solid-* (format nil "~A" current-key) 10 10 )
         
         (sdl:update-display))))))
