// This function makes an ajax post request to the server to update a posts 'score'; also changes vote button color
function upVote(post) {
    // Ajax request posts to server
    $.ajax({
        type: "POST",
        url: "/vote",
        //post.className keeps track of a posts id in the web page so we can update the proper value in the db
        data: JSON.stringify(post.className, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            // After a successful post, this updates the user's web page to see changes
            // ...(post.className)[0] -> the [0] element is 'score' value, [1] element is the upvote button
            var score = document.getElementsByClassName(post.className)[0];
            score.innerHTML = result['score'];
            document.getElementsByClassName(post.className)[1].style.color = 'grey';
        }
    });
}

// Delete a post, and reloads page to reflect post removal
function deletePost(post) {
    $.ajax({
        type: "POST",
        url: "/remove",
        data: JSON.stringify(post.className, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: function(result) {
            window.location.reload(forceGet=true)
        }
    });
}
