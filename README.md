# SYNFloodingPlayground
> A simple web-based playground where you can freely test SYN Flooding with hping3! Written in Flask, Python3.
<span>
    <img src="https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue">
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
    <img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white">
</span>
<br>
<br>

 **Welcome to [KnightChaser](https://github.com/KnightChaser)'s SYN Flooding experiment playground!** (You don't know what `SYN FLOODING ATTACK` mean yet? Then, check [Wikipedia's detailed explanation](https://en.wikipedia.org/wiki/SYN_flood). This would be helpful for understanding.)

 The main goal of this playground is to generate lots of SYN packets(As default, 30 million accumulative SYN packets) with lots of tools dedicated to network attacks such as `hping3`, which is very popular. With any tool you prefer, try to attack the playground freely! You can watch the rapid increment of SYN packets you sent. (This playground shows how much did you send in the session.)

 If you send more SYN packets than specific threshold amounts, the playground will show you a secret flag(actually, it's stored in `/secret/flag.txt`. But Let's suppose you don't know where is the flag.). To get a flag, you conduct a SYN Flooding attack. It's like CTF(Capture The Flag), isn't it?


## Build

 The program was written on Ubuntu 22.04. LTS on WSL2. This code likely does not work on Windows or other operating systems. I wrote this playground under the assumption of you are going to run this in a localhost environment(So, the attack and the victim reside on the same device.). If you are going to separate the attack role and server(victim), you may have to adjust some code. But don't worry, the code isn't complicated.

- On Ubuntu(You must be able to run basic Linux commands, command `stat`, and command `tcpdump`.), Install **Python3** and **PIP(Package Installer for Python)** to install required Python packages.
- With PIP, Install every component specified in `requirements.txt`.
- Run `server.py` with the proper FLASK command. (ex. `flask run`)

## How does it work?

 If the server(`server.py`) runs and the attacker enters `/`(`@app.route('/')`), The following command will run on the victim's system automatically. The command based on `tcpdump` will print a single line like `03:17:01.085514 IP 192.168.0.1.52756 > 127.0.1.1.5000: Flags [S], seq 1821047614, win 512, length 0` per every single incoming SYN packet. So, each line of the command output is equivalent of 1 SYN packet arrival. 
```sh
sudo tcpdump -i lo -l -n -Q in dst port 5000
```

 To reduce the output size, I appended the `grep -o "S"` option with the pipeline(`|`). If I do so, the output from every SYN packet arrival will be just `S`. So, 200 SYN packets mean 200 `S` characters. I store the output in the file `./tcpdumplog`. Thus, the file size in Bytes will be the same as the total arrived SYN packets. That's how I measure how much SYN Flooding attack has been reached to the server in the session.
```sh
sudo tcpdump -i lo -l -n -Q in dst port 5000 | grep -o "S" > ./tcpdumplog
```

 For reference, only `./tcpdumplog`'s file size can be extracted by this simple command. `server.py` runs this command whenever it needs to fetch the accumulative SYN packet arrival count.
```sh
stat --printf="%s" ./synfloodlog
```

## How can I exploit and get the content of `flag.txt`?

 Just do a SYN Flooing attack! If `server.py` runs on `127.0.0.1:5000` and you are going to use `hping3`, the attack payload will be:
```sh
sudo hping3 -S 127.0.1.1 -p 5000 -a 192.168.0.1 --flood
```
 In my environment, only a single execution of that command can generate 500k ~ 1M SYN packets per second. If you run the command in multiple instances simultaneously, the attack speed will increase. (And highly likely they will consume more CPU and memory resources too.)

 You don't need to adhere to `hping3` only. Try to write a Python script, or use other tools too if you are interested!

## Adjustable parts

#### `server.py`
You can manually alter SYN Flooding log from `tcpdump`.
```py
# Where the file for accumulative SYN packets should be?
synflooding_count_file_path = "./synfloodlog"
```

You can manually alter the location of `flag.txt`, and also can change `flag.txt`'s contents, too.
```py
# flag
@app.route('/sh0wMYFLAGGGGGGGGGGGGG')
def give_flag():
    # ...
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path, "./secret/flag.txt")
```

#### threshold
`threshold` means how much accumulative SYN packets have to arrive at the server to reveal `flag`. Adjust the threshold value according to your device's capability, time, or other variables. When you change the threshold, Don't forget to synchronize the value both in `server.py` and `counter_template.html`.
```py
# server.py
# flag
@app.route('/sh0wMYFLAGGGGGGGGGGGGG')
def give_flag():

    # verify
    # Don't forget to synchronize this threshold variable with counter_template.js's!!
    threshold = 30000000
    # ...
```
```js
// counter_template.html (JS in HTML file)
var count = document.getElementById("count");
var threshold = 30000000;                       // Don't forget to synchronize this threshold variable with server.py's!!
```

## Issues

If you have any questions, suggestions, improvements, typos, errors, problems, or something else, Do not hesitate to make issues! I'll be glad to check them out.
