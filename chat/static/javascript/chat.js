document.addEventListener('DOMContentLoaded', async function() {
    // Получение всех элементов чата
    const chatItems = document.querySelectorAll('.chat-item');

    // Устанавливаем обработчик события клика на каждый элемент чата
    chatItems.forEach(chatItem => {
        chatItem.addEventListener('click', handleChatItemClick);
    });

    let currentChatItemId = null; // Хранит ID текущего чата
    let chatSocket = null; // WebSocket-соединение
    let isWebSocketConnected = false;
    let currentUser = parseInt(document.getElementById('currentUserId').value);

    // Устанавливаем соединение с WebSocket сервером
    chatSocket = new WebSocket('ws://127.0.0.1:8000/ws/chat/');

    chatSocket.onopen = function(event) {
        var chatItems = document.querySelectorAll('.chat-item');

        // Создаем пустой объект для хранения пар значений user_id - chatId
        var chatUserMap = {};

        // Итерируемся по всем элементам chat-item и получаем их значения атрибутов data-user-id и id
        chatItems.forEach(function(item) {
            var userId = item.getAttribute('data-user-id');
            var chatId = item.getAttribute('id');

            // Записываем пару значений в объект chatUserMap
            chatUserMap[userId] = chatId;
        });

        // Отправляем данные на сервер
        chatSocket.send(JSON.stringify({
            'type': 'user_status',
            'status': 'online',
            'chat_user_map': chatUserMap
        }));
    };

    chatSocket.onmessage = function(event) {
        var chatItems = document.querySelectorAll('.chat-item');

        // Создаем пустой массив для хранения значений data-user-id
        var userIds = [];

        // Итерируемся по всем элементам chat-item и получаем их значения атрибута data-user-id
        chatItems.forEach(function(item) {
            var userId = item.getAttribute('data-user-id');
            userIds.push(userId);
        });

        var data = JSON.parse(event.data);
        var user_id = data.user_id;

        if (data.type == 'user.isonline') {
            console.log('User is online');
            var element = document.querySelector('[data-user-id="' + user_id + '"]');

            if (element) {
            var chatStatusDiv = element.querySelector('.chat_status');
            chatStatusDiv.textContent = "Online"
            }
        }else if (data.type == 'user.isoffline') {
            console.log('User is offline');
            var element = document.querySelector('[data-user-id="' + user_id + '"]');

            if (element) {
                var chatStatusDiv = element.querySelector('.chat_status');
                chatStatusDiv.textContent = "Offline";
            }
        }

    };

    chatSocket.onclose = function(event) {
        console.log('Соединение с чатом закрыто');
        isWebSocketConnected = false;
    };

    // Обработчик события клика на элемент чата
    async function handleChatItemClick() {
        const chatItemId = this.getAttribute('id');
        const paragraph = document.getElementById('ChatUserName');
        const image_div = document.getElementById('chat-user_image');
        const last_seen = document.getElementById('last_seen');
        // Отображение панели чата, если она скрыта
        toggleChatPanelVisibility(true);

        // Запрос информации о пользователе чата
        const other_user = await fetch(`/api/chat/other-user/${chatItemId}/`);
        const ChatUserInfo = await other_user.json();

        // Отображение информации о пользователе чата
        paragraph.textContent = ChatUserInfo.nickname;
        image_div.textContent = ChatUserInfo.nickname[0];
        last_seen.textContent = 'Last seen ' + formatLastSeen(ChatUserInfo.last_login);

        // Очистка текущего чата
        clearChat();

        // Запрос сообщений нового чата
        try {
            const response = await fetch(`/api/chat/messages/${chatItemId}/`);

            if (!response.ok) {
                throw new Error('Ошибка при получении данных');
            }
            const UsersMessages = await response.json();

            // Отображение сообщений нового чата
            displayMessages(UsersMessages);


            scrollToBottom();

        } catch (error) {
            console.error('Ошибка:', error);
        }
    }

    // Функция для отображения или скрытия панели чата
    function toggleChatPanelVisibility(show) {
        const chatPanel = document.querySelector('.chat-panel');
        if (show) {
            chatPanel.classList.remove('hidden_visibility');
        } else {
            chatPanel.classList.add('hidden_visibility');
        }
    }

    // Функция для очистки текущего чата
    function clearChat() {
        const chatContainer = document.querySelector('.dialog_panel');
        chatContainer.innerHTML = '';
        currentChatItemId = null;
    }

    // Функция для отображения сообщений в чате
    function displayMessages(UsersMessages) {
        // Объединяем оба массива сообщений

        // Сортируем объединенный массив по времени отправления
        UsersMessages.sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

        // Получаем ссылку на контейнер чата
        const chatContainer = document.querySelector('.dialog_panel');

        // Выводим отсортированные сообщения внутрь контейнера чата
        UsersMessages.forEach(message => {
            displayMessage(chatContainer, message);
        });
    }

    // Функция для отображения одного сообщения чата
    async function displayMessage(chatContainer, message) {
        // Создание элемента сообщения
        const messageDiv = document.createElement('div');
        // Установка класса сообщения в зависимости от отправителя
        if (message.sender.id === currentUser) {
            messageDiv.className = 'd-flex flex-row-reverse mb-2';
        } else {
            messageDiv.className = 'left-chat-message fs-13 mb-2';
        }

        // Добавление содержимого сообщения в зависимости от отправителя
        if (message.sender.id === currentUser) {
            messageDiv.innerHTML = `
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
                                <div class="mr-2">${formatTime(message.timestamp)}</div>
                                <div class="svg15 double-check"></div>
                            </div>
                        </div>
                        <div class="message-arrow"><i class="text-muted la la-angle-down fs-17"></i></div>
                    </div>
                </div>
            `;
        } else {
            messageDiv.innerHTML = `
                <p class="mb-0 mr-3 pr-4">${message.content}</p>
                <div class="message-options">
                    <div class="message-time">${formatTime(message.timestamp)}</div>
                    <div class="message-arrow"><i class="text-muted la la-angle-down fs-17"></i></div>
                </div>
            `;
        }

        // Добавление сообщения в контейнер чата
        chatContainer.appendChild(messageDiv);
    }

    // Функция для форматирования времени
    function formatTime(timestamp) {
        const date = new Date(timestamp);
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        return `${hours}:${minutes}`;
    }

    // Функция для форматирования последнего входа
    function formatLastSeen(lastLoginString) {
        const date = new Date(lastLoginString);
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const year = date.getFullYear();
        return `${hours}:${minutes} ${day}.${month}.${year}`;
    }
//    // Функция для подключения к WebSocket-серверу
//    function connectToChat(chatItemId) {
//        if (isWebSocketConnected) {
//            console.log('Соединение с чатом уже установлено');
//            chatSocket.close();
//        }
//        // Устанавливаем соединение с WebSocket сервером
//        chatSocket = new WebSocket('ws://127.0.0.1:8000/ws/chat/');
//
//        // Обработчик события открытия соединения
//        chatSocket.onopen = function(event) {
//            console.log('Соединение с чатом установлено');
//            isWebSocketConnected = true; // Устанавливаем флаг подключения
//        };
//
//        // Обработчик события закрытия соединения
//        chatSocket.onclose = function(event) {
//            console.log('Соединение с чатом закрыто');
//            isWebSocketConnected = false; // Сбрасываем флаг подключения
//        };
//
//        // Обработчик события получения сообщения
//        chatSocket.onmessage = function(event) {
//            var data = JSON.parse(event.data);
//
//            if (data.message && data.is_online !== undefined && data.nickname) {
//                console.log(data)
//            } else if (data.message && data.is_online == undefined) {
//                console.log(data)
//
//                // Получение значения поля "message"
//                var message = data.message;
//
//                // Добавление нового сообщения в чат
//                displayMessages([message]);
//            } else {
//                console.log('else')
//            }
//        };
//
//        // Обработчик события ошибки
//        chatSocket.onerror = function(error) {
//            console.error('Ошибка сокета:', error);
//            isWebSocketConnected = false; // Сбрасываем флаг подключения
//        };
//    }

    // Функция для отправки сообщения через WebSocket
    async function sendMessage(message) {
        chatSocket.send(JSON.stringify({
            'type': 'new_message',
            'message': message,
            'user_id': currentUser,
        }));
    }

    function scrollToBottom() {
        var containerHeight = $('.scrollable-chat-panel').height();
        $('.scrollable-chat-panel').scrollTop(containerHeight + 10000);
    }

    // Обработчик события нажатия клавиши "Enter" в поле ввода сообщения
    document.getElementById("messageInput").addEventListener("keyup", function(event) {
        if (event.key === "Enter") {
            // Проверяем, подключено ли WebSocket-соединение
            if (!chatSocket || chatSocket.readyState !== WebSocket.OPEN) {
                console.log('Соединение с чатом не установлено');
                return;
            }

            // Получаем текст сообщения из поля ввода
            var messageInput = document.getElementById("messageInput");
            var messageText = messageInput.value.trim();

            // Отправляем сообщение через WebSocket, если текст не пустой
            if (messageText !== '') {
                sendMessage(messageText);
                // Очищаем поле ввода после отправки сообщения
                messageInput.value = '';
            }
        }
    });
});
