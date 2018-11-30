$(document).ready(function () {
    $.getJSON("/api/todos")
        .then(addTodos)

    $('#todoInput').keypress(function (event) {
        if (event.which === 13 && $(this).val().length > 0){  // event.which === 13  —> enter key
            createTodo();
        }
    })
    
    $('.list').on('click', 'span', function (event) {
        event.stopPropagation(); // does not trigger listener above
        removeTodo($(this).parent());
    })

    $('.list').on('click', 'li', function () {
        updateTodo($(this));
    })
});

function addTodos(todos) {
    todos.forEach(function (todo) {
        addTodo(todo);
    })
}

function addTodo(todo) {
    var newTodo = $('<li class="task">'+todo.name + '<span>X</span></li>');
    newTodo.data('id', todo.id); // store todo.id in memory with the key "id" to use it later
    newTodo.data('completed', todo.completed);
    if(todo.completed){
        newTodo.addClass('done')
    }
    $(".list").append(newTodo)
}

function removeTodo(todo) {
    var id = todo.data('id');
    var deleteUrl = '/api/todos/' + id;
    $.ajax({
        method: 'DELETE',
        url: deleteUrl,
    })
    .then(function (data) {
        todo.remove();
    })
}

function createTodo() {
    var usrInput = $('#todoInput').val();
    $.post('/api/todos/', {name: usrInput})
        .then(function (newTodo) {
            $('#todoInput').val('');  // set input field to blank again
            addTodo(newTodo);
        })
        .catch(function (err) {
            console.log(err);
        })
}

function updateTodo(todo) {
    var updateUrl = '/api/todos/' + todo.data('id') + '/';
    var isDone = !todo.data('completed');
    var updateData = {"completed": isDone};
    console.log(updateData);
    $.ajax({
        method: "PUT",
        url: updateUrl,
        data: updateData
    })
    .then(function() {
        todo.toggleClass('done');
        todo.data('completed', isDone);
    })
}






// some stuff to make ajax post work with django csrf token, just copy it
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});
// end of some stuff