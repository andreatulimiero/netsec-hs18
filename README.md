Netsec challenge proposal
===
Group ID:
>Team 2

Member names:
>Lorenz Merz
>Andrea Tulimiero
>Luca Di Bartolomeo

## Challenge title
### ***Say that again***

## Abstract
The hacker is given an encrypted conversation between a client and a server (a `.pcap` file), a private key (a `.pem` file), and the certificate of the server (an `X.509` file). 
Their **goal** is to find out the **password of the client**.

In order to do so, they have to leverage the messages included in the conversation to carry out a reply-attack and gain access to the server.

The **vulnerability** lies in the fact that the server is missing a control on the uniqueness of a message (e.g.: using a timestamp).

Once in the server, the hacker will find the private key of the server (another `.pem` file), and thus be able to decrypt the rest of the message in which there's the flag.

## Step-by-step instructions

#### 0. provided material

- `.pcap` file containing the TCP dump of the conversation between the client and the server
- `.pem` file containing the private key of the client
- `X.509` file, containing the certificate of the server to which the client connected during the conversation, and to which the hacker has to connect to solve the challenge.

#### 1. understand the content of the `.pcap` file

- there are several TCP messages exchanged between the client and the server
- in the first message (plaintext), the server asks the client to provide a RSA public key `Kc.pub`
- the rest of the messages sent by the server will have the payload encrypted with the provided public key
- the messages sent by they client are encrypted using the server public key `Ks.pub`, which can be retrieved by the provided certificate

<!--
```
SERVER has asymmetric RSA key pair (Ks, Ks.pub)
CLIENT has asymmetric RSA key pair (Kc, Kc.pub)

    1) SERVER -> CLIENT : hello, please provide your RSA public key
    2) CLIENT -> SERVER : Kc.pub
    3) SERVER -> CLIENT : { username: }Kc.pub
    4) CLIENT -> SERVER : { <username> }Ks.pub
    5) SERVER -> CLIENT : { password: }Kc.pub
    6) CLIENT -> SERVER : { <password> }Ks.pub
    7) SERVER -> CLIENT : { welcome.. }Kc.pub
```
-->

> $\texttt{1) SERVER}\rightarrow\texttt{CLIENT}: \texttt{ "Hello, please provide your RSA public key" }$
> $\texttt{2) CLIENT}\rightarrow\texttt{SERVER}: \texttt{ Kc.pub}$
> $\texttt{3) SERVER}\rightarrow\texttt{CLIENT}: \texttt{\{ "username:" \}}_\texttt{Kc.pub}$
> $\texttt{4) CLIENT}\rightarrow\texttt{SERVER}: \texttt{\{ <username> \}}_\texttt{Ks.pub}$
> $\texttt{5) SERVER}\rightarrow\texttt{CLIENT}: \texttt{\{ "password:" \}}_\texttt{Kc.pub}$
> $\texttt{6) CLIENT}\rightarrow\texttt{SERVER}: \texttt{\{ <password> \}}_\texttt{Ks.pub}$
> $\texttt{7) SERVER}\rightarrow\texttt{CLIENT}: \texttt{\{ Welcome ... \}}_\texttt{Kc.pub}$

#### 2. find out who is the owner of the provided private key (`.pem` file):
- use `openssl` to compute the corresponding public key
- the computed public key matches the public key of the client `Kc.pub`, therefore the `.pem` file contains the private key of the client `Kc`

#### 3. decrypt the messages sent from the server to the client
- use the private key to decrypt messages number `3` and `5`
- you see that the server is asking for username and password, so you guess that messages number `4` and `6` are respectively the actual username and password
- they are, however, encrypted with the public key of the server `Ks.pub` and you are therefore unable to decrypt them without the knowledge of the correspoding private key `Ks`


#### 4. connect and authenticate to the server
- the password cannot be bruteforced, you have to come up a way to authenticate without having to guess the password
- use a *replay attack* to authenticate by first establishing a connection and then repeating message `2`, `4` and `6` when prompted for the credentials


#### 5. get the password of the client
- you now have a remote shell that you can use to send commands to the server (encrypting them with the public key of the server `Ks.pub`)
- find the `.pem` file on the home directory of the server containing the private key of the server `Ks`
- use `Ks` to decrypt the client messages (`4`, `5`) of the authentication in the `.pcap` file.
- the flag of the client is in the message `6`, and corresponds to the password.

## Wargame information

You were able to capture the communication between a client and *[server IP]* : *[link to pcap file]*.

To avoid any kind of malicious sniffing, the server requires all messages sent to it to be encrypted with its public key: *[server certificate]*.

The messages are encrypted; however, one anonymous friend tells you that he managed to snatch a private key, although, he's not sure whether or not the key was used to ecnrypt the conversation.

Your goal is to find the password that the client used to authenticate to the server.
