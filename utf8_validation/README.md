# Overview

This directory holds exercise on how check that a string (or actually chain of numbers supposedly representing characters)
  can be interpreted as an UTF-8 string.
  
# Exercise - UTF-8 validation

File 0-validate_utf8.py

## Instructions

Write a method that determines if a given data set represents a valid UTF-8 encoding.\r\n\r\n- Prototype: `def validUTF8(data)`\r\n- Return: `True` if data is a valid UTF-8 encoding, else return `False`\r\n- A character in UTF-8 can be 1 to 4 bytes long\r\n- The data set can contain multiple characters\r\n- The data will be represented by a list of integers\r\n- Each integer represents 1 byte of data, therefore you only need to handle the 8 least significant bits of each integer\r\n\r\n```\r\ncarrie@ubuntu:~/utf8_validation$ cat 0-main.py\r\n#!/usr/bin/python3\r\n\"\"\"\r\nMain file for testing\r\n\"\"\"\r\n\r\nvalidUTF8 = __import__('0-validate_utf8').validUTF8\r\n\r\ndata = [65]\r\nprint(validUTF8(data))\r\n\r\ndata = [80, 121, 116, 104, 111, 110, 32, 105, 115, 32, 99, 111, 111, 108, 33]\r\nprint(validUTF8(data))\r\n\r\ndata = [229, 65, 127, 256]\r\nprint(validUTF8(data))\r\n\r\ncarrie@ubuntu:~/utf8_validation$\r\n```\r\n```\r\ncarrie@ubuntu:~/utf8_validation$ ./0-main.py\r\nTrue\r\nTrue\r\nFalse\r\ncarrie@ubuntu:~/utf8_validation$\r\n```"</script><div class="task-description-content">Write a method that determines if a given data set represents a valid UTF-8 encoding.

- Prototype: `def validUTF8(data)`
- Return: `True` if data is a valid UTF-8 encoding, else return `False`
- A character in UTF-8 can be 1 to 4 bytes long
- The data set can contain multiple characters
- The data will be represented by a list of integers
- Each integer represents 1 byte of data, therefore you only need to handle the 8 least significant bits of each integer

```
carrie@ubuntu:~/utf8_validation$ cat 0-main.py
#!/usr/bin/python3
&quot;&quot;&quot;
Main file for testing
&quot;&quot;&quot;

validUTF8 = __import__(&#39;0-validate_utf8&#39;).validUTF8

data = [65]
print(validUTF8(data))

data = [80, 121, 116, 104, 111, 110, 32, 105, 115, 32, 99, 111, 111, 108, 33]
print(validUTF8(data))

data = [229, 65, 127, 256]
print(validUTF8(data))

carrie@ubuntu:~/utf8_validation$
```
```
carrie@ubuntu:~/utf8_validation$ ./0-main.py
True
True
False
carrie@ubuntu:~/utf8_validation$
```

# Interesting resources

- https://lokalise.com/blog/what-is-character-encoding-exploring-unicode-utf-8-ascii-and-more/
- https://en.wikipedia.org/wiki/UTF-8
