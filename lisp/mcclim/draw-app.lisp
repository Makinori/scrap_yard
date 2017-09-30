(ql:quickload :mcclim)

(in-package :clim-user)


;;;; frame / pane

(define-application-frame draw-frame ()
  ((lines :accessor lines :initform nil))
  (:panes (draw-pane (make-pane 'draw-pane))
          (interactor :interactor))
  (:layouts (default-default (vertically ()
                               draw-pane
                               interactor)))
  (:menu-bar t)
  (:command-definer t)
  (:top-level (default-frame-top-level)))

(defclass draw-pane
    (standard-extended-input-stream
     basic-pane
     permanent-medium-sheet-output-mixin)
  ())

(defmethod handle-repaint ((pane draw-pane) region)
  (with-application-frame (frame)
    (call-next-method)
    (dolist (line (lines frame))
      (draw-line pane (car line) (cdr line)))))

;; execute
(defun run-draw-app ()
  (run-frame-top-level (make-application-frame 'draw-frame)))


;;;; commands
(define-draw-frame-command (com-draw-add-line :menu t :name t)
    ((x1 'integer) (y1 'integer) (x2 'integer) (y2 'integer))
  (with-slots (lines) *application-frame*
    (push (cons (make-point x1 y1) (make-point x2 y2))
          lines))
  (update-draw-pane))

(define-draw-frame-command (com-draw-clear :menu t :name t)
    ()
  (with-slots (lines) *application-frame*
    (setf lines nil))
  (update-draw-pane))

(defun update-draw-pane ()
  (repaint-sheet (find-pane-named *application-frame* 'draw-pane) +everywhere+))

;;;; event-UI
  

