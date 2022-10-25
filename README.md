# cbzconv

A small Python script to convert comic book archives to PDF for easy portability.

Supports the following archive formats:

* .CBZ
* .CBR (you need to have "unrar" in your PATH)
* .CB7 (you need to have "7z" in your PATH)
* .CBT

## Dependencies and installation

* python >= 3.10
* python-pillow >= 9.2.0

Download the ```cbzconv.py``` file, remove the .py extension and move it somewhere in your PATH (ideally /usr/local/bin)

## Basic usage

```bash
cbzconv "A Comic Book.cbz" "Another Comic Book.cbz"
```

