function create_note(user_id, film_id) {
  var note_data = document.getElementById("note_textarea").value;
  fetch("/note", {
    method: "POST",
    body: JSON.stringify({ user_id: user_id, film_id: film_id, note_data: note_data}),
  }).then((_res) => {
    window.location.href = "/film/" + film_id;
  });
}

function update_note(user_id, film_id) {
  var note_data = document.getElementById("note_textarea").value;
  fetch("/note", {
    method: "PATCH",
    body: JSON.stringify({ user_id: user_id, film_id: film_id, note_data: note_data}),
  }).then((_res) => {
    window.location.href = "/film/" + film_id;
  });
}

function delete_note(user_id, film_id) {
  fetch("/note", {
    method: "DELETE",
    body: JSON.stringify({ user_id: user_id, film_id: film_id}),
  }).then((_res) => {
    window.location.href = "/film/" + film_id;
  });
}

function create_comment(user_id, film_id) {
  var comment_data = document.getElementById("comment_textarea").value;
  fetch("/forum-comment", {
    method: "POST",
    body: JSON.stringify({ user_id: user_id, film_id: film_id, comment_data: comment_data}),
  }).then((_res) => {
    window.location.href = "/film/" + film_id;
  });
}

function delete_comment(comment_id, film_id) {
  fetch("/forum-comment", {
    method: "DELETE",
    body: JSON.stringify({comment_id: comment_id, film_id: film_id}),
  }).then((_res) => {
    window.location.href = "/film/" + film_id;
  });
}

function reply_comment(user_id, parent_comment_id, film_id) {
  var comment_data = document.getElementById("comment-reply-" + parent_comment_id + "").value;
  fetch("/forum-comment", {
    method: "PATCH",
    body: JSON.stringify({ parent_comment_id: parent_comment_id, film_id: film_id, comment_data: comment_data, user_id: user_id}),
  }).then((_res) => {
    window.location.href = "/film/" + film_id;
  });
}