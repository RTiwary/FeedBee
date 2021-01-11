let choices = {
    a: "Feature Suggestion",
    b: "Small Bug",
    c: "Large Bug",
    d: "Other"
}

let choice = '';

document.addEventListener('DOMContentLoaded', () => {
    // does something for each option clicked
    document.querySelectorAll('.option').forEach(element => {
        element.addEventListener('click', (event) => {
            const clicked_option = event.target.dataset.category;
            console.log(clicked_option);

            if (clicked_option === 'a') {
                clicked_a();
            } else if (clicked_option === 'b') {
                clicked_b();
            }
            else if (clicked_option === 'c') {
                clicked_c();
            }
            else if (clicked_option === 'd') {
                clicked_d();
            }
        })
    });

    document.querySelector('.submit-btn').addEventListener('click', (event) => {
        if (choice !== '') {
            submit_suggestion();
        } else {
            console.log('Sorry try again');
            return false;
        }
    })
});

function clicked_a() {
    const options = document.querySelectorAll('.choice');
    for (let i = 0; i < options.length; i++) {
        if (i === 0) {
            options[i].className = 'option-selected choice';
            choice = 'a';
        } else {
            options[i].className = 'option choice';
        }
    }
}

function clicked_b() {
    const options = document.querySelectorAll('.choice');
    for (let i = 0; i < options.length; i++) {
        if (i === 1) {
            options[i].className = 'option-selected choice';
            choice = 'b';
        } else {
            options[i].className = 'option choice';
        }
    }
}

function clicked_c() {
    const options = document.querySelectorAll('.choice');
    for (let i = 0; i < options.length; i++) {
        if (i === 2) {
            options[i].className = 'option-selected choice';
            choice = 'c';
        } else {
            options[i].className = 'option choice';
        }
    }
}

function clicked_d() {
    const options = document.querySelectorAll('.choice');
    for (let i = 0; i < options.length; i++) {
        if (i === 3) {
            options[i].className = 'option-selected choice';
            choice = 'd';
        } else {
            options[i].className = 'option choice';
        }
    }
}

function submit_suggestion() {
    console.log('Submitting feedback');

    // get the csrf token
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    // make sure to include csrf token when fetching
    const request = new Request(
        'submit/',
        {headers: {'X-CSRFToken': csrftoken}}
    );

    const commentsInput = document.querySelector(`#comments-form-input`);

    if (choice !== '' && commentsInput.value.trim() !== '') {
        console.log('Submitting feedback');
        fetch(request, {
            method: 'POST',
            credentials: 'include',
            body: JSON.stringify({
                category: choices[choice],
                comment: commentsInput.value
            })
        })
        .then(response => response.json(), error => console.log(error))
        .then(result => {
            console.log(result);
            displayToast();
        });
    } else {
        console.log('Sorry. Try again.');
    }
}