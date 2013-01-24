;;; config
(context 'config)

(set 'server "localhost")
(set 'port 10002)

(context MAIN)

;;; utils
(context 'utils)

(define (usage)
  (let (shell-name (first (rest $main-args)))
    (println (string "usages: " shell-name " ids"))
    (println (string "        " shell-name " all"))
    (println (string "        " shell-name " id <discuss-id>"))        
    (println (string "        " shell-name " post-id <post-id>"))
    (println (string "        " shell-name " help")))
  (exit 1))

(context MAIN)

;;; discuss
(context 'discuss)

(define (get)
  (letn (URL-SERVER (string "http://" config:server ":" config:port)
         second (lambda (L) (first (rest L)))
         argv (args)
         condition (first argv))
    (cond ((= condition "all")
           (set 'url (string URL-SERVER "/api/discuss/all")))
          ((= condition "ids")
           (set 'url (string URL-SERVER "/api/discuss/ids")))
          ((= condition "post-id")
           (let (post-id (second argv))
             (set 'url
                  (string "http://localhost:10002/api/discuss/post/" post-id))))
          ((= condition "id")
           (let (discuss-id (second argv))
             (set 'url
                  (string "http://localhost:10002/api/discuss/" discuss-id))))
          (true           
           (utils:usage)))
    (get-url url)))

(context MAIN)
