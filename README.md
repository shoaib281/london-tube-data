# Vaticle London Tube CLI

_Command Line Interface to learn about the London Underground_

## Overview

This application first takes in a JSON file of London Underground Tube data and loads it into a PostgreSQL database. From here, the user can learn about the London Underground

## Schema

3 tables are created before this process occurs
- Station table containing station name, id and longitude and latitude
- Line table containing line name and id
- A join table containing the foreign keys for each station and line.

## Usage

Once the tables are created and the data is parsed and loaded, the user inputs a particular station name or line name
- Inputting a station reveals all the lines that station is part of
- Inputting a line reveals all the stations that are part of the line
