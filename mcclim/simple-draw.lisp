(ql:quickload :mcclim)

(in-package :clim-user)



;;;; drawing-app
;; ref : McClim PDF guide-tour
;; https://common-lisp.net/project/mcclim/static/documents/guided-tour.pdf
;; draw-frame


;; frame/panel
(define-application-frame draw-frame ()
  ((lines :accessor lines :initform nil)
   (strings :accessor strings :initform nil))
  (:panes ;(draw-pane (make-pane 'draw-pane))
   
          (interactor :interactor))
  (:layouts (default-default (vertically ()
                               draw-pane
                               interactor)))
  (:menu-bar t)
  (:command-definer t)
  (:top-level (default-frame-top-level)))

(defclass draw-pane
    (standard-expanded-input-stream
     basic-pane
     permanent-medium-sheet-output-mixin)
  ())

(defmethod handle-repaint ((pane draw-pane) region)
  (with-application-frame (frame)
    (call-next-method)
    (dolist (line (lines frame))
      (draw-line pane (car line) (cdr line)))
    (dolist (pair (strings frame))
      (draw-text pane (cdr pair) (car pair)))))

;;command             
(define-draw-frame-command (com-draw-add-string :menu t :name t)
    ((string 'string) (x 'integer) (y 'integer))
  (push (cons (make-point x y) string)
        (strings *application-frame*))
  (update-draw-pane))

(define-draw-frame-command (com-draw-add-line :menu t :name t)
    ((x1 'integer) (y1 'integer) (x2 'integer) (y2 'integer))
  (with-slots (lines) *application-frame*
    (push (cons (make-point x1 y1) (make-point x2 y2))
          lines))
    (update-draw-pane))

(define-draw-frame-command (com-draw-clear :menu t :name t) 
    ()
  (with-slots (lines strings) *application-frame*
    (setf lines nil strings nil))
  (update-draw-pane))

(defun update-draw-pane ()
  (repaint-sheet (find-pane-named *application-frame* 'draw-pane) +everywhere+))

;; UI 

(defmethod handle-event ((pane draw-pane) (event pointer-button-press-event))
  (when (eql (pointer-event-button event) +pointer-left-button+)
    (track-line-drawing pane
                        (pointer-event-x event)
                        (pointer-event-y event))))

(defmethod handle-event ((pane draw-pane) (event key-press-event))
  (when (keyboard-event-character event)
    (multiple-value-bind (x y) (stream-pointer-position pane)
      (track-text-drawing pane "" x y)))
  (update-draw-pane))

(defun track-line-drawing (pane startx starty)
  (let ((lastx startx)
        (lasty starty))
    (with-drawing-options (pane )
      (draw-line* pane startx starty lastx lasty)
      (tracking-pointer (pane)
        (:pointer-motion 
         (&key x y)
         (draw-line* pane startx starty lastx lasty)
         (draw-line* pane startx starty x y)
         (setq lastx x lasty y))
        (:pointer-button-release 
         (&key event x y)
         (when (eql (pointer-event-button event) +pointer-left-button+)
           (draw-line* pane startx starty lastx lasty)
           (execute-frame-command *application-frame*
                                  `(com-draw-add-line ,startx ,starty ,x ,y))
           (return-from track-line-drawing nil)))
        )
      )))

(defun track-text-drawing (pane current-string current-x current-y)
  (tracking-pointer (pane)
    (:pointer-motion 
     (&key window x y)
     window
     (handle-repaint pane +everywhere+)
     (setq current-x x current-y y)
     (draw-text* pane current-string x y))
    (:keyboard 
     (&key gesture)
     (when (and (typep gesture 'key-release-event)
                (keyboard-event-character gesture))
       (setf current-string
             (concatenate 'string
                          current-string
                          (string (keyboard-event-character gesture))))
       (handle-repaint pane +everywhere+)
       (draw-text* pane current-string current-x current-y)))
    (:pointer-button-release 
     (&key event x y)
     x y
     (when (eql (pointer-event-button event) +pointer-left-button+)
       (execute-frame-command *application-frame*
                              `(com-draw-add-string ,current-string ,current-x ,current-y))
       (return-from track-text-drawing nil)))))

(defun run-draw-app ()
  (run-frame-top-level (make-application-frame 'draw-frame)))


