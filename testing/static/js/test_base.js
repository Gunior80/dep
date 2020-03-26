var next_link = document.getElementById("next_url").value;
var main_container = document.getElementById('progress-screen');
var back = document.getElementById('back');
var next = document.getElementById('next');

var questions = main_container.children.length;
var current_question = 1;

document.getElementById("num_1").classList.add("bg-warning", "text-white");
        function LoadURL() {
            document.location.replace(next_link);
        }

        for (let i = 2; i <= questions; i++){
            let child = document.getElementById(i);
            child.style.display = "none";
        }
        back.disabled = true;

        function checked(question){
            let el = document.getElementById(question);
            let elements = el.querySelectorAll('.check');
            if (elements.length > 0){
                for (let i = 0; i < elements.length; i++){
                    if (elements[i].checked === true) {
                        return true;
                    }
                }
            }
            elements = el.querySelectorAll('.radio');
            if (elements.length > 0){
                for (let i = 0; i < elements.length; i++){
                    if (elements[i].checked === true) {
                        return true;
                    }
                }
            }
            return false;
        }

        function overchecked(element){
            let score_elem = element.getElementsByClassName("count");
            if (score_elem.length > 0){
                let score = score_elem.item(0).innerHTML;
                let count = 0;
                let elements = element.querySelectorAll('.check');
                for (let i = 0; i < elements.length; i++){
                    if (elements[i].checked === true) {
                        count = count + 1;
                    }
                }
                if (count > score){
                    return false;
                }
            }
            return true;
        }

        function reDraw(curr, next) {
            document.getElementById("num_" + curr).classList.remove("bg-warning");
            if (checked(curr) === true){
                document.getElementById("num_" + curr).classList.add("bg-success");
            }
            else{
                document.getElementById("num_" + curr).classList.remove("text-white", "bg-success");
            }
            document.getElementById("num_" + next).classList.add("bg-warning", "text-white");
        }

        function isNumber(n) { return !isNaN(parseFloat(n)) && !isNaN(n - 0) }

        function clk(nav){
            let el = document.getElementById(current_question);
            if (overchecked(el) === true) {
                if (nav === 'finish') {
                    done();
                }
                if (isNumber(nav)) {
                    el.style.display = "none";
                    let el_next = document.getElementById(nav);
                    el_next.style.display = "block";
                    reDraw(current_question, nav);
                    if (nav === 1) {
                        back.disabled = true;
                        next.disabled = false;
                    }
                    else if (nav === questions) {
                        back.disabled = false;
                        next.disabled = true;
                    }
                    else {
                        back.disabled = false;
                        next.disabled = false;
                    }
                    current_question = nav;
                }
                if (nav === 'next') {
                    if (current_question < questions) {
                        el.style.display = "none";
                        let el_next = document.getElementById(current_question + 1);
                        el_next.style.display = "block";
                        reDraw(current_question, current_question + 1);
                        if (current_question === 1) {
                            back.disabled = false;
                        }
                        if (current_question + 1 === questions) {
                            next.disabled = true;
                        }
                    }
                    current_question = current_question + 1;
                }
                if (nav === 'back') {
                    if (current_question > 1) {
                        el.style.display = "none";
                        let el_prev = document.getElementById(current_question - 1);
                        el_prev.style.display = "block";
                        reDraw(current_question, current_question - 1);
                    }
                    if (current_question === questions) {
                        next.disabled = false;
                    }
                    if ((current_question - 1) === 1) {
                        back.disabled = true;
                    }
                    current_question = current_question - 1;
                }
            }
        }

        let finnaly = false;

        function done()
        {
            finnaly = true;
            let msg = $('#testform').serialize();
            $.ajax({
                type: 'POST',
                url: document.location.href,
                data: msg,
                success: function(data) {
                    clearTimeout(timer);
                    $('#result').modal('show');
                    let response_p = document.getElementById("response");
                    response_p.innerText = data;
                },
                error:  function(xhr, str){
                    alert('Возникла ошибка: ' + xhr.responseCode);
                }
            });
        }

        function sync(){
            let token = document.getElementsByName("csrfmiddlewaretoken")[0].value;
            let msg = { csrfmiddlewaretoken: token };
            $.ajax({
                type: 'POST',
                url: document.getElementById("sync_url").value,
                data: msg,
                success: function(data) {
                    min = data["min"];
                    sec = data["sec"];
                },
                error:  function(xhr, str){}
            });
        }

        var minutes = document.getElementById("min");
        var seconds = document.getElementById("sec");
        let timer; // пока пустая переменная
        let min = document.getElementById("min").innerText; // стартовое значение обратного отсчета
        let sec = 0;
        let tick = 0;
        countdown(); // вызов функции
        function countdown(){  // функция обратного отсчета
            if (min < 10){
                minutes.innerHTML = '0' + min;
            }
            else {
                minutes.innerHTML = '' + min;
            }
            if (sec < 10){
                seconds.innerHTML = '0' + sec;
            }
            else {
                seconds.innerHTML = '' + sec;
            }
            if (min > 0){
                if (sec === 0){
                    min--;
                    sec = 59;
                }
                else{
                    sec--;
                }
                timer = setTimeout(countdown, 1000);
            }
            else{
                if (sec < 1){
                    clearTimeout(timer); // таймер остановится на нуле
                    minutes.innerHTML = '00';
                    seconds.innerHTML = '00';
                    done();
                }
                else{
                    sec--;
                    timer = setTimeout(countdown, 1000);
                }
            }
            if (tick < 10){
                tick++;
            }
            else{
                sync();
                tick = 0;
            }
        }

        (function (global) {
            if(typeof (global) === "undefined") {
                throw new Error("window is undefined");
            }

            var _hash = "!";
            var noBackPlease = function () {
                global.location.href += "#";

                // making sure we have the fruit available for juice (^__^)
                global.setTimeout(function () {
                    global.location.href += "!";
                }, 50);
            };

            global.onhashchange = function () {
                if (global.location.hash !== _hash) {
                    global.location.hash = _hash;
                }
            };

            global.onload = function () {
                if (finnaly === false){
                    noBackPlease();

                    // disables backspace on page except on input fields and textarea..
                    document.body.onkeydown = function (e) {
                        var elm = e.target.nodeName.toLowerCase();
                        if (e.which === 8 && (elm !== 'input' && elm  !== 'textarea')) {
                            e.preventDefault();
                        }
                        // stopping event bubbling up the DOM tree..
                        e.stopPropagation();
                    };
                }
            }

        })(window);

        window.onbeforeunload = function (e) {
            if (finnaly === false) {
                // Ловим событие для Interner Explorer
                var event = e || window.event;
                var myMessage = "Вы действительно хотите завершить тест?";
                // Для Internet Explorer и Firefox
                if (event) {
                    event.returnValue = myMessage;
                }
                // Для Safari и Chrome
                return myMessage;
            }
        };