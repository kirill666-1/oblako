if command == 'shutdown':
                # Завершение работы сервера
                print("Завершение работы сервера...")
                logging.info("Сервер завершает работу по команде shutdown.")
                server_running = False
                server_paused = False  # На случай, если сервер был на паузе
                sock.close()  # Закрываем сокет, чтобы выйти из accept()
                break
            elif command == 'pause':
                if not server_paused:
                    server_paused = True
                    print("Сервер поставлен на паузу. Новые подключения не принимаются.")
                    logging.info("Сервер поставлен на паузу по команде pause.")
                else:
                    print("Сервер уже находится на паузе.")
            elif command == 'resume':
                if server_paused:
                    server_paused = False
                    print("Сервер возобновил прием подключений.")
                    logging.info("Сервер возобновил работу по команде resume.")
                else:
                    print("Сервер и так работает.")
            elif command == 'show logs':
                # Показываем содержимое файла логов
                if os.path.exists('server.log'):
                    with open('server.log', 'r') as log_file:
                        print("\n=== Содержимое логов ===")
                        print(log_file.read())
                        print("=== Конец логов ===\n")
                else:
                    print("Лог-файл отсутствует.")
            elif command == 'clear logs':
                # Очищаем файл логов
                if os.path.exists('server.log'):
                    open('server.log', 'w').close()
                    print("Логи очищены.")
                    logging.info("Логи были очищены по команде clear logs.")
                else:
                    print("Лог-файл отсутствует.")
            elif command == 'clear id':
                # Очищаем файл идентификации
                if os.path.exists(IDENTIFICATION_FILE):
                    open(IDENTIFICATION_FILE, 'w').close()
                    print("Файл идентификации очищен.")
                    logging.info("Файл идентификации был очищен по команде clear id.")
                else:
                    print("Файл идентификации отсутствует.")
            else:
                print("Неизвестная команда. Доступные команды: shutdown, pause, resume, show logs, clear logs, clear id.")

    except KeyboardInterrupt:
        # Обработка сигнала Ctrl+C
        print("\nЗавершение работы сервера...")
        logging.info("Сервер завершает работу по сигналу Ctrl+C.")
        server_running = False
        server_paused = False
        sock.close()

    # Ожидаем завершения потока прослушивания
    listener_thread.join()

    # Ожидаем завершения всех клиентских потоков
    for t in client_threads:
        t.join()

    print("Сервер остановлен.")
    logging.info("Сервер остановлен.")

if name == "main":
    main()