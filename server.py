from flask import Flask, redirect, url_for, render_template, render_template_string, flash
import os
import requests

app = Flask(__name__)

# Where the file for accumulative SYN packets should be?
synflooding_count_file_path = "./synfloodlog"

# flag
@app.route('/sh0wMYFLAGGGGGGGGGGGGG')
def give_flag():

    # verify
    # Don't forget to synchronize this threshold variable with counter_template.js's!!
    threshold = 30000000
    syn_packets_qty = requests.get(url_for('statistics', _external = True))
    syn_packets_qty = int(syn_packets_qty.text)
    print(syn_packets_qty)
    
    # not enough accumulative syn packets. cheat detected!
    if syn_packets_qty < threshold:
        action =  "<script type=\"text/javascript\">"
        action += f"alert(\"Don't try to cheat UwU~♬, you just gained {syn_packets_qty} of {threshold} SYN packets. Sorry, your log will be reset :)\");"
        action += "window.location.href = '/'"
        action += "</script>"
        return render_template_string(action)

    # flag
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path, "./secret/flag.txt")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return str(content)
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# print current accumulative size
@app.route('/synflood_statistics')
def statistics():
    # Only prints the pure size of the synflooding log file.
    # 1 Bytes(character 'S') means 1 successful SYN Arrival.
    syn_pkt_accumulative_count = os.popen(f"stat --printf=\"%s\" {synflooding_count_file_path}").read()
    return str(syn_pkt_accumulative_count)

# main
@app.route('/')
def server():
    
    # Ready to count incoming TCP SYN packets (accumulative)
    #   Be aware that this tcpdump mode receives SYN packets from lo(loopback) interface
    #   because I made this for only internal experiment. So you may have to change.
    #   (Also, you may need to adjust other options to fit your custom environment too.)
    #   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #                           |
    #                           V
    os.popen(f"sudo tcpdump -i lo -l -n -Q in dst port 5000 | grep -o 'S' > {synflooding_count_file_path} &")
                                                            # Every syn connection will be equivalent with 1 byte
                                                            # If you refresh, the log will be cleared to zero
    # If this "/" gets reloaded, the tcpdump tool will restart and the accumulative SYN packet statistics will be 0 again.
    
    # Render current SYN packet count statistics from /synflood_statistics
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path, "./counter_template.html")

    with open(file_path, 'r') as file:
        counter_template = file.read()
        return render_template_string(counter_template)

if __name__ == '__main__':
    app.run()
