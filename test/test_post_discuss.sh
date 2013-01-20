curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"post_id":"'$(uuidgen)'",
          "title":"post by test_post_discuss script",
          "author":"peerxu",
          "email":"google@google.com",
          "content":"test"}' \
 http://localhost:10002/api/discuss
