# SAFire
A working Python 3 draft script that prints an aria2 compatible input file to download all your SAF courses' material.
Uses `requests`, `BeautifulSoup4` and `click`.

## Usage
### Using a virtualenv is recomended
`python3 -m venv venv`

`source ./venv/bin/activate`
### Install requirements
`pip install -r requirements.txt`
### Get all links and save it in a file
`python saf_scrapet.py -c <SAF's session_id_ing cookie value> > out.txt`
To get the cookie you can use your browser's dev tools or an extension like `cookies.txt` (chromium)
#### Example
`python saf_scrapet.py -c 192.169.1.1-afff7a47-aa8d-3b2f-beb5-021f9312e2f6 > out.txt`
### Download using [aria2](https://aria2.github.io)
`aria2c -i out.txt --load-cookies cookies.txt`
#### cookies.txt example
```
saf.uandes.cl	FALSE	/	TRUE	0	session_id_admin	192.169.1.1-afff7a47-aa8d-3b2f-beb5-021f9312e2f6
```

PROFIT!