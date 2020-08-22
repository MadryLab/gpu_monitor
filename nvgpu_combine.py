import urllib.request

AGENTS = ["http://deep-gpu-1.csail.mit.edu:1080/",
          "http://deep-gpu-2.csail.mit.edu:1080/",
          "http://deep-gpu-3.csail.mit.edu:1080/",
          "http://deep-gpu-4.csail.mit.edu:1080/",
          "http://deep-gpu-5.csail.mit.edu:1080/",
          "http://deep-gpu-6.csail.mit.edu:1080/",
          "http://deep-gpu-7.csail.mit.edu:1080/",
          "http://deep-gpu-8.csail.mit.edu:1080/",
          "http://deep-gpu-9.csail.mit.edu:1080/",
          "http://deep-gpu-10.csail.mit.edu:1080/"]

with open('html_head.txt', 'r') as fp:
    HEAD = [fp.read()]

TAIL = ["</body> \n </html>"]

while True:
    combined_htmls = []

    for agent in AGENTS:
        fp = urllib.request.urlopen(agent)
        mybytes = fp.read()
        html = mybytes.decode("utf8")
        fp.close()

        html = html.split('\n')
        ind = sum([i if '<body' in elt else 0 for i, elt in enumerate(html)]) + 1
        html = html[ind:-4]

        combined_htmls.extend(html)
        combined_htmls.extend(["<br>", "<br>"])

    combined_html = '\n'.join(HEAD + combined_htmls + TAIL)

    with open('gpu_monitor.html', 'w') as fp:
        fp.write(combined_html)

