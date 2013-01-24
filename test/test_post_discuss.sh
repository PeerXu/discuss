POST_ID=9575160f-40ef-421d-9e8e-c7507649a589
curl -X POST \
     -H "Content-Type: application/json" \
     -d '{"post_id":"'$POST_ID'",
          "title":"post by test_post_discuss script",
          "author":"peerxu",
          "email":"google@google.com",
          "content":"test"}' \
 http://localhost:10002/api/discuss
