# telegraf-python

InfluxDB's Telegraf container with additional Python packages. A nightly GitHub Action checks for a new image tagged 'latest' in the official Telegraf Docker Hub repository and will build and push a new modified image as necessary.

This container solves a need for running Python scripts using Telegraf's `exec` input plugin.
