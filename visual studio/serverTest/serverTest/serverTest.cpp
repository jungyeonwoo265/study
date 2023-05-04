#pragma comment(lib, "ws2_32")
#pragma warning(disable:4996)
#include <stdio.h>
#include <iostream>
#include <vector>
#include <thread>
#include <WinSock2.h>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
#include <locale>
#include <codecvt>
#include <string>

#define BUFFERSIZE 1024

using namespace std;
using namespace rapidjson;

vector<SOCKET> socketlist;

void send_msg(SOCKET clientSock, string &json)
{
    size_t len = strlen(json.c_str());

    send(clientSock, json.c_str(), static_cast<int>(len), 0);

}

void Read_msg(SOCKET clientSock, SOCKADDR_IN clientAddr)
{
    cout << "Read msg start" << endl;

    vector<char> buffer(BUFFERSIZE);
    Document document;
    string json;
    string msg;
    int recvBytes = 0;
    int com;

    do {
        recvBytes = recv(clientSock, buffer.data(), buffer.size(), 0);
        if (recvBytes > 0)
        {
            json += string(buffer.data(), recvBytes);
        }
        if (recvBytes == buffer.size())
            continue;
        document.Parse(json.c_str());

        StringBuffer sb;
        Writer<StringBuffer> writer(sb);
        document.Accept(writer);

        cout << "recvBytes: " << recvBytes << "bytes" << endl;
        if (!document.HasParseError())
        {
            com = document["command"].GetInt();
            switch (com)
            {
            case 1:
                cout<< ntohs(clientAddr.sin_port) << endl;
                for (SOCKET csock : socketlist)
                    send_msg(csock, json);
                break;

            default:
                break;
            }
            json.clear();
            cout << "json.clear" << endl;
        }
        
    } while (recvBytes > 0);
}

void client(SOCKET clientSock, SOCKADDR_IN clientAddr, vector<thread*>* clientlist)
{
    cout << "Client connected IP address = " << inet_ntoa(clientAddr.sin_addr) << ":" << ntohs(clientAddr.sin_port) << endl;
    socketlist.push_back(clientSock);
    thread read_msg(Read_msg, clientSock, clientAddr);
    read_msg.join();

    closesocket(clientSock);
    cout << "Client disconnected IP address = " << inet_ntoa(clientAddr.sin_addr) << ":" << ntohs(clientAddr.sin_port) << endl;
    socketlist.erase(remove(socketlist.begin(), socketlist.end(), clientSock), socketlist.end());
    
    for (auto ptr = clientlist->begin(); ptr < clientlist->end(); ptr++)
    {
        if ((*ptr)->get_id() == this_thread::get_id())
        {
            clientlist->erase(ptr);
            break;
        }
    }
}

int main()
{
    vector<thread*> clientlist;
    
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
    {
        return 1;
    }
    SOCKET serverSock = socket(PF_INET, SOCK_STREAM, 0);
    SOCKADDR_IN addr;
    std::memset(&addr, 0, sizeof(addr));
    addr.sin_family = AF_INET;
    addr.sin_addr.s_addr = htonl(INADDR_ANY);
    addr.sin_port = htons(9090);
    if (bind(serverSock, (SOCKADDR*)&addr, sizeof(SOCKADDR_IN)) == SOCKET_ERROR)
    {
        cout << "bind error" << endl;
        return 1;
    }
    if (listen(serverSock, SOMAXCONN) == SOCKET_ERROR)
    {
        cout << "listen error" << endl;
        return 1;
    }
    cout << "Server Start" << endl;
    while (1)
    {
        int len = sizeof(SOCKADDR_IN);
        SOCKADDR_IN clientAddr;
        SOCKET clientSock = accept(serverSock, (SOCKADDR*)&clientAddr, &len);
        clientlist.push_back(new thread(client, clientSock, clientAddr, &clientlist));
    }
    if (clientlist.size() > 0)
    {
        for (auto ptr = clientlist.begin(); ptr < clientlist.end(); ptr++)
        {
            (*ptr)->join();
        }
    }
    closesocket(serverSock);
    WSACleanup();
    socketlist.clear();
    return 0;
}