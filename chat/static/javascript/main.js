function updateChatContent(leftData, rightData) {
    updateLeftPanelContent(leftData);
    updateRightPanelContent(rightData);
}

function updateLeftPanelContent(data) {
    // Получаем контейнер для левой панели чата
    var leftPanel = document.querySelector('.left-chat-message');

    // Очищаем содержимое контейнера
    leftPanel.innerHTML = '';

    // Перебираем сообщения из полученных данных и добавляем их в контейнер
    data.messages.forEach(function(message) {
        var messageHTML = `
            <div class="left-chat-message fs-13 mb-2">
                <p class="mb-0 mr-3 pr-4">${message.content}</p>
                <div class="message-options">
                    <div class="message-time">${message.time}</div>
                    <div class="message-arrow"><i class="text-muted la la-angle-down fs-17"></i></div>
                </div>
            </div>
        `;
        leftPanel.insertAdjacentHTML('beforeend', messageHTML);
    });

    // Прокручиваем контейнер чата до самого низа
    leftPanel.scrollTop = leftPanel.scrollHeight;
}

function updateRightPanelContent(data) {
    // Получаем контейнер для правой панели чата
    var rightPanel = document.querySelector('.right-chat-message');

    // Очищаем содержимое контейнера
    rightPanel.innerHTML = '';

    // Перебираем сообщения из полученных данных и добавляем их в контейнер
    data.messages.forEach(function(message) {
        var messageHTML = `
            <div class="right-chat-message fs-13 mb-2">
                <div class="mb-0 mr-3 pr-4">
                    <div class="d-flex flex-row">
                        <div class="pr-2">${message.content}</div>
                        <div class="pr-4"></div>
                    </div>
                </div>
                <div class="message-options dark">
                    <div class="message-time">
                        <div class="d-flex flex-row">
                            <div class="mr-2">${message.time}</div>
                            <div class="svg15 double-check"></div>
                        </div>
                    </div>
                    <div class="message-arrow"><i class="text-muted la la-angle-down fs-17"></i></div>
                </div>
            </div>
        `;
        rightPanel.insertAdjacentHTML('beforeend', messageHTML);
    });

    // Прокручиваем контейнер чата до самого низа
    rightPanel.scrollTop = rightPanel.scrollHeight;
}

function updateChatContent(leftData, rightData) {
    updateLeftPanelContent(leftData);
    updateRightPanelContent(rightData);
}

function fetchDataAndRenderChat() {
    // Отправляем запрос на сервер для получения данных сообщений слева
    fetch('/api/left-chat-messages')
        .then(response => response.json())
        .then(leftData => {
            // Отправляем запрос на сервер для получения данных сообщений справа
            return fetch('/api/right-chat-messages')
                .then(response => response.json())
                .then(rightData => {
                    // После получения обоих наборов данных обновляем обе панели чата
                    updateChatContent(leftData, rightData);
                });
        })
        .catch(error => {
            console.error('Error fetching chat messages:', error);
        });
}

// Вызываем функцию для загрузки данных и отображения чата при загрузке страницы
fetchDataAndRenderChat();
