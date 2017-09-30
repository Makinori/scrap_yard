(ql:quickload :mcclim)
(ql:quickload :cl-fad)

(in-package :clim-user)

;;;; file-browser
;; ref : McClim PDF guide-tour
;; https://common-lisp.net/project/mcclim/static/documents/guided-tour.pdf
;; file-browser

;;;; frame/pane
(define-application-frame file-browser ()
  ((active-files :initform nil :accessor active-files))
  (:panes
   (file-browser :application
                 :display-function '(dirlist-display-files)
                 :display-time :command-loop)
   (interactor :interactor))
  (:layouts (default (vertically ()
                       file-browser
                       interactor)))
  (:menu-bar t))

(define-presentation-type dir-pathname ()
  :inherit-from 'pathname)

;; execute
(defun run-file-browser ()
  (run-frame-top-level (make-application-frame 'file-browser)))


;;;; command

(define-file-browser-command (com-edit-directory :menu t :name t)
    ((dir 'dir-pathname))
  (setf (active-files *application-frame*)
        (cl-fad:list-directory dir)))

(define-file-browser-command (com-quit :menu t :name t) ()
  (frame-exit *application-frame*))

;;;; UI of gadgets

(defmethod dirlist-display-files ((frame file-browser) pane)
  (clear-output-record (stream-output-history pane))
  (dolist (file (active-files frame))
    (present file
             (if (cl-fad:directory-pathname-p file) 'dir-pathname 'pathname)
             :stream pane)
    (terpri pane)))



(define-presentation-to-command-translator pathname-to-edit-command
    (dir-pathname
     com-edit-directory
     file-browser
     :gesture :select
     :documentation "edit this path")
    (object)
  (list object))


(defmethod adopt-frame :after (frame-manager (frame file-browser))
  (declare (ignore frame-manager))
  (execute-frame-command frame
                         `(com-edit-directory ,(make-pathname :directory '(:absolute)))))
     



