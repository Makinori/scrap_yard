


(ql:quickload :clack)
(ql:quickload :cl-dbi)
(ql:quickload :jsown)
(ql:quickload :kmrcl)

(ql:quickload :png)

#|
;; structure of url

domain.com/path/to/file&data-typetype@show-type

path/to/file :: path to file registered in database
$data-type :: [root:content | log:log | comment:comment] of file
@show-type :: [view:view in template | file:request content of file | down:donload] 
#command :: lunch command

abbreviation:
if server got omittable url from client, server say client to that "303:see other" and let to link omitted url
> path/to/file&data-type&show-type/ => path/to/file$data-type@show-type
> $data-type = content => omittable
> @show-type = view => omittable
|#

(defun rotate (input-pathname output-pathname)
  "Read a PNG image, rotate it 90 degrees, and write it to a new file."
  (let* ((old (with-open-file (input input-pathname
                                     :element-type '(unsigned-byte 8))
                (png:decode input)))
         (new (png:make-image (png:image-width old)
                              (png:image-height old)
                              (png:image-channels old)
                              (png:image-bit-depth old)))
         (m (png:image-width old)))
      (dotimes (i (png:image-height new))
        (dotimes (j (png:image-width new))
          (dotimes (k (png:image-channels new))
            (setf (aref new i j k) (aref old j (- m i 1) k)))))
      (with-open-file (output output-pathname :element-type '(unsigned-byte 8)
                              :direction :output :if-exists :supersede)
        (png:encode new output))))

(defun read-png (pathname)
  "Read a PNG image, rotate it 90 degrees, and write it to a new file."
  (with-open-file (input pathname
                         :element-type '(unsigned-byte 8))
    (png:decode input)))



(defun encode-url (url-list)
  )

(defun parse-url (url-str)
  )

(defun *data-type-list* ()
  (list (list
         :key "root"
         :func #'(lambda (req) req))
        ))


(defun decode-url (url-str)
  (list
   :pre url-str
   :data-type nil
   :show-type nil
   :extension (pathname-type url-str)
   :omit nil
   ))

(defun json-parse (json-str)
  (ignore-errors
    (jsown:parse json-str)))

  
(defmacro concat-str (&body strings)
  `(concatenate 'string ,@strings))


(defun read-file-into-string (path)
  (ignore-errors
    (with-open-file (s path
                       :direction :input
                       :element-type '(unsigned-byte 8)
                       :external-format :utf8)
      (let ((buf (make-array (file-length s) :element-type '(unsigned-byte 8))))
        (read-sequence buf s)
        (sb-ext:octets-to-string buf :external-format :utf-8)))))

(defun read-binary-file (path)
  (ignore-errors 
    (with-open-file (in path
                        :element-type 'flex:octet)
      (let ((bin (make-array (file-length in)
                             :element-type 'flex:octet)))
        (read-sequence bin in)
        bin))))

(defun file-length-int (pathname)
  (with-open-file (f pathname)
    (file-length f)))

(defun directory-content (path)
  (mapcar #'(lambda (path)
              (enough-namestring path *file-path-root*))
          (directory (pathname (format nil "~A/*.*" path)) :resolve-symlinks nil)))


(defun updated-date (path)
  ;; decode-universal-time
  (let ((time (ignore-errors (file-write-date path))))
    (format nil "~{~A~^-~}"
            (reverse (butlast (multiple-value-list 
                               (ignore-errors
                                 (decode-universal-time time)))
                              3)))))

(defun content-type (extension-str)
  (cond ((string= "css" extension-str)
         "text/css")
        ((string= "html" extension-str)
         "text/html")
        ((string= "png" extension-str)
         "image/png")
        ((string= "jpeg" extension-str)
         "image/jpeg")
        (t "text")))




(defparameter *file-path-root* "/home/makinori/program/test/server/files/")



(defun app (req)
  (let* ((method (getf req :request-method))
         (url (decode-url (getf req :path-info)))
         (headers (getf req :headers))
         
         (file-path (pathname (concat-str *file-path-root*
                                          (getf url :pre))))
         (path-exist (probe-file file-path))
         
         (file-content (read-file-into-string file-path))
         (content-type (content-type (getf url :extension)))
         (directory-content (directory-content file-path))
         (updated-date (updated-date file-path))
         (binary-content (read-binary-file file-path))
         )
    (print path-exist)
    (print updated-date)
    
    (cond      
      ;; 404 not found
      ((not path-exist)
       `(404 nil nil))
      ;; 304 you have seen its file
      ((string= (gethash "if-modified-since" headers) updated-date)
       `(304 ,(list :last-modified updated-date) nil))
      ;; 200 file find - text
      (file-content
       (print "text")
       `(200 ,(list :last-modified updated-date
                    :content-type content-type)
             (,file-content)))
      ;; 200 file find - binary
      (binary-content
       (print "bin")
       `(200 ,(list :last-modified updated-date
                    :content-type content-type
                    :content-length (file-length-int file-path)
                    )
             (,binary-content)))
      ;; 200 directory found
      (directory-content
       `(200 ,(list :last-modified updated-date
                    :content-type "text/plain")
             (,(format nil "~A" directory-content))))
      ;; error
      (t
       `(500 nil nil)))
    ))




;;;; to run server

(let ((running-app nil))
  (defun run-app (app &key (port 5056))
    (unless (eq running-app nil)
      (clack:stop running-app))
    (setf running-app (clack:clackup app :port port))))


(defun application (req)
  (app req))

(run-app #'application)



;;;; trash

#|

(defun db-run (db-connection query-string)
  (handler-case
      (dbi:fetch-all (dbi:execute
                      (dbi:prepare db-connection
                                   (format nil "~A" query-string))))
    (DBI.ERROR:<DBI-PROGRAMMING-ERROR> (c)
      (declare (ignore c))
      (warn (format nil "dbi-error: dbi-programming query-string: ~A~%"
                    query-string))
      nil
    )))

(defun get-first-data (list)
  (cadar list))


(defun get-path-from-url (db-connection url-list)
  (pathname (concat-str
              *file-path-root*
              (get-first-data
               (db-run db-connection
                       (format nil (concat-str
                                     "select json_extract(data, '$.path')"
                                     "from test "
                                     "where json_extract(test.data, '$.url')='~A';")
                               (getf url-list :omit)))))))

(let* ((db-connection
        (dbi:connect
         :sqlite3
         :database-name "./test.sqlite3")))
  (defun run-in-connection (str)
    (db-run db-connection str))
  (defun app (req)
    (let* ((method (getf req :request-method))
           (url (decode-url (getf req :path-info)))
           (file-path
            (get-path-from-url db-connection url))
           (file-content (read-file-into-string file-path)))

      (cond
        ((string/= (getf url :pre) (getf url :omit))
         `(303 (:location ,(getf url :omit)) nil))
        ((not (null file-content))
         `(200 (:content-type "text/html")
               (,file-content)))
        (t
         `(404 nil nil)))
      )))


|#
