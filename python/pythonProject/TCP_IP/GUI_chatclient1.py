# GUI 채팅 클라이언트

from socket import *
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from threading import *


class ChatClient:
    client_socket = None

    def __init__(self, a, b):
        self.initialize_socket(a, b)
        self.initialize_gui()
        self.listen_thread()

    def initialize_socket(self, a, b):
        self.client_socket = socket(AF_INET, SOCK_STREAM)
        remote_ip = a
        remote_port = b
        self.client_socket.connect((remote_ip, remote_port))

    def send_chat(self):
        senders_name = self.name_widget.get().strip()+':'
        data = self.enter_text_widget.get(1.0, 'end').strip()
        message = (senders_name + data).encode('utf-8')
        self.chat_transcript_area.insert('end', message.decode('utf-8')+'\n')
        self.chat_transcript_area.yview(END)
        self.client_socket.send(message)
        self.enter_text_widget.delete(1.0, 'end')
        return 'break'

    def initialize_gui(self):
        self.root = Tk()
        fr = []
        for i in range(0, 5):
            fr.append(Frame(self.root))
            fr[i].pack(fill=BOTH)
        self.name_label = Label(fr[0], text='사용자 이름')
        self.recv_label = Label(fr[1], text='수진 메시지:')
        self.send_label = Label(fr[3], text='송신 메시지:')
        self.send_btn = Button(fr[3], text='전송', command=self.send_chat)
        self.chat_transcript_area = ScrolledText(fr[2], height=5, width=60)
        self.enter_text_widget = ScrolledText(fr[4], height=5, width=60)
        self.name_widget = Entry(fr[0], width=15)

        self.name_label.pack(side=LEFT)
        self.name_widget.pack(side=LEFT)
        self.recv_label.pack(side=LEFT)
        self.send_btn.pack(side=RIGHT, padx=20)
        self.chat_transcript_area.pack(side=LEFT, padx=2, pady=2)
        self.send_label.pack(side=LEFT)
        self.enter_text_widget.pack(side=LEFT, padx=2, pady=2)

    def listen_thread(self):
        t = Thread(target=self.receive_message, args=(self.client_socket,))
        t.start()

    def receive_message(self, so):
        while True:
            buf = so.recv(256)
            if not buf:
                break
            self.chat_transcript_area.insert('end', buf.decode('utf-8')+'\n')
            self.chat_transcript_area.yview(END)
        so.close()


if __name__ == "__main__":
    ip = input('server IP addr:')
    if ip == "":
        ip = '10.10.21.108'
    port = 9000
    ChatClient(ip, port)
    mainloop()
