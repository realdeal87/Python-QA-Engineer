"""Скрипт для выполнения HTTP запросов с помощью библиотеки socket"""
import argparse
import logging
import socket
import ssl


def request_formatter(args, log):
    """Функция для формирования запроса к ресурсу"""
    host = args.host
    request = args.method + " " + args.url + " HTTP/1.1\nHost: " + args.host
    for header in args.headers:
        request = request + "\n" + header
    request = request + "\n\n"
    log.info("\n" + request)
    return host, request


def connection(host, request, log):
    """Функция для установки соединения и отправки запроса"""
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()

    log.info("Server IP: " + socket.gethostbyname(host))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock = context.wrap_socket(sock, server_hostname=host)

    sock.connect((host, 443))

    sock.send(request.encode())
    result = sock.recv(4096)

    response = ""

    while result:
        response += result.decode()
        result = sock.recv(4096)

    sock.close()
    return response


def response_parser(response, log):
    """Функция для разделения ответа на код ответв, хедеры и тело ответа"""
    log.info("\n" + response)
    response = response.split("\r\n")
    i = 0
    for i, n in enumerate(response):
        if response[i] == "":
            break
    code = response[0].split(" ")[1]
    headers = response[1:i]
    body = "\r\n".join(response[i:])
    return code, headers, body


if __name__ == "__main__":

    logger = logging.getLogger("ssh_client")
    logger.setLevel(logging.DEBUG)
    shr = logging.StreamHandler()
    shr.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
    shr.setFormatter(formatter)
    logger.addHandler(shr)

    parser = argparse.ArgumentParser()

    parser.add_argument("--method", "-m",
                        action="store",
                        help="Method of HTTP request",
                        choices=["GET"],
                        required=True)

    parser.add_argument("--host", "-s",
                        action="store",
                        help="Host address",
                        required=True)

    parser.add_argument("--url", "-u",
                        action="store",
                        help="Resource url",
                        default="/")

    parser.add_argument("--headers", "-d",
                        action="store",
                        nargs="*",
                        help="Headers of HTTP requests. Use quotations to devide headers",
                        default="")

    arguments = parser.parse_args()
    hostname, http_request = request_formatter(arguments, logger)
    http_response = connection(hostname, http_request, logger)
    http_code, http_headers, Http_body = response_parser(http_response, logger)
    print(http_code, http_headers, Http_body)
