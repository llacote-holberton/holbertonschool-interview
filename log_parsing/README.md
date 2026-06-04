# Overview

This directory holds exercise on designing a script able to parse a log file
  to extract pertinent information.

# Exercise - Log parsing

## Goal
Write a script that reads `stdin` line by line and computes metrics.

## Business and technical requirements

### Input format
`&lt;IP Address&gt; - [&lt;date&gt;] &quot;GET /projects/260 HTTP/1.1&quot; &lt;status code&gt; &lt;file size&gt;`
(OR, with decoded HTML values: `<IP Address> - [<date>] "GET /projects/260 HTTP/1.1" <status code> <file size>`)

If the format is not this one, the line must be skipped!

### Script behaviour

After every 10 lines and/or a keyboard interruption (`CTRL + C`), print these statistics from the beginning: "Total file size" and "Number of lines for each status code"

#### Total file size: format and constraints

Total file size must follow this format: `File size: &lt;total size&gt;` (or: `File size: <total size>`)
Where `&lt;total size&gt;` is the sum of all previous `&lt;file size&gt;` (`<file size>`) (see input format above)

#### Number of lines by status code: format and constraints

- Supported status code are as follows:
  * Possible status code: `200`, `301`, `400`, `401`, `403`, `404`, `405` and `500`
  * If a status code doesn&#39;t appear or is not an integer, don&#39;t print anything for this status code
- Printing format: 
  * Each line must respect this formatting: `&lt;status code&gt;: &lt;number&gt;`
  * Status codes should be printed in ascending order

#### Additional note: behaviour as "self-executing script" ONLY

Your code should NOT be executed when imported - by using __import__, like the example below

**Warning:** In this sample, you will have random value - it&#39;s normal to not have the same output as this one.

<details><summary>Example details</summary>

```
alexa@ubuntu:~/log_parsing$ cat 0-generator.py
#!/usr/bin/python3
import random
import sys
from time import sleep
import datetime

for i in range(10000):
    sleep(random.random())
    sys.stdout.write("{:d}.{:d}.{:d}.{:d} - [{}] \"GET /projects/260 HTTP/1.1\" {} {}\n".format(
        random.randint(1, 255), random.randint(1, 255), random.randint(1, 255), random.randint(1, 255),
        datetime.datetime.now(),
        random.choice([200, 301, 400, 401, 403, 404, 405, 500]),
        random.randint(1, 1024)
    ))
    sys.stdout.flush()

alexa@ubuntu:~/log_parsing$ ./0-generator.py | ./0-stats.py 
File size: 5213
200: 2
401: 1
403: 2
404: 1
405: 1
500: 3
File size: 11320
200: 3
301: 2
400: 1
401: 2
403: 3
404: 4
405: 2
500: 3
File size: 16305
200: 3
301: 3
400: 4
401: 2
403: 5
404: 5
405: 4
500: 4
^CFile size: 17146
200: 4
301: 3
400: 4
401: 2
403: 6
404: 6
405: 4
500: 4
Traceback (most recent call last):
  File "./0-stats.py", line 15, in <module>
Traceback (most recent call last):
  File "./0-generator.py", line 8, in <module>
    for line in sys.stdin:
KeyboardInterrupt
    sleep(random.random())
KeyboardInterrupt
alexa@ubuntu:~/log_parsing$ 
```

</details>
